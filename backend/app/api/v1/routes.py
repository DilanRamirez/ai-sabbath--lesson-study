from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.responses import FileResponse
from typing import Literal
import logging
from pydantic import BaseModel, Field
from app.indexing.search_service import search_lessons, IndexStore
from app.services.llm_service import generate_llm_response
from app.services.cms_service import (
    load_lesson_by_path,
    load_metadata_by_path,
    get_lesson_pdf_path,
    list_all_lessons,
)

router = APIRouter()
logger = logging.getLogger(__name__)


class QARequest(BaseModel):
    question: str
    top_k: int = Field(default=3, ge=1, le=20,
                       description="Must be between 1 and 20")
    lang: Literal["en", "es"] = "es"


@router.get("/ping")
def ping():
    status = {
        "faiss_index_loaded": IndexStore.index is not None,
        "metadata_loaded": isinstance(IndexStore.metadata, list)
        and len(IndexStore.metadata) > 0,
    }
    return (
        {"status": "ok", **status}
        if all(status.values())
        else {"status": "error", **status}
    )


@router.get("/lessons/{year}/{quarter}/{lesson_id}")
def get_lesson(year: str, quarter: str, lesson_id: str):
    """
    Returns the full lesson.json file for a given year, quarter, and lesson ID.
    Example: /api/v1/lessons/2025/Q2/lesson_06
    """
    try:
        return load_lesson_by_path(year, quarter, lesson_id)
    except FileNotFoundError:
        logger.error(f"Lesson not found: {year}/{quarter}/{lesson_id}")
        raise HTTPException(status_code=404, detail="Lesson not found")


@router.get("/lessons/{year}/{quarter}/{lesson_id}/metadata")
def get_lesson_metadata(year: str, quarter: str, lesson_id: str):
    """
    Returns the metadata.json file for a given year, quarter, and lesson ID.
    Example: /api/v1/lessons/2025/Q2/lesson_06/metadata
    """
    try:
        return load_metadata_by_path(year, quarter, lesson_id)
    except FileNotFoundError:
        logger.error(f"Metadata not found: {year}/{quarter}/{lesson_id}")
        raise HTTPException(status_code=404, detail="Metadata not found")
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(
            status_code=500, detail="Unexpected error loading metadata")


@router.get("/lessons/{year}/{quarter}/{lesson_id}/pdf")
def get_lesson_pdf(year: str, quarter: str, lesson_id: str):
    """
    Returns the PDF file for a given year, quarter, and lesson ID.
    Example: /api/v1/lessons/2025/Q2/lesson-06/pdf
    """
    try:
        pdf_path = get_lesson_pdf_path(year, quarter, lesson_id)
        return FileResponse(
            pdf_path, media_type="application/pdf", filename=f"{lesson_id}.pdf"
        )
    except FileNotFoundError:
        logger.error(f"PDF not found: {year}/{quarter}/{lesson_id}")
        raise HTTPException(status_code=404, detail="PDF file not found")
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(
            status_code=500, detail="Unexpected error loading PDF")


@router.get("/lessons")
def list_lessons():
    """
    Returns a list of all lessons available in the system.
    Example: /api/v1/lessons
    """
    try:
        return list_all_lessons()
    except Exception:
        logger.error("Error listing lessons", exc_info=True)
        raise HTTPException(status_code=500, detail="Unable to list lessons")


@router.post("/llm")
def process_llm(
    text: str = Body(..., embed=True),
    mode: Literal["explain", "reflect", "apply", "summarize", "ask"] = Body(
        ..., embed=True
    ),
    lang: str = Query(
        "en", description="Response language, e.g. 'en' or 'es'"),
):
    if not text or not text.strip():
        raise HTTPException(
            status_code=400, detail="Text input cannot be empty.")
    try:
        result = generate_llm_response(text, mode, lang)
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing LLM request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
def semantic_search(
    q: str = Query(..., description="Search query text"),
    type: str = Query(
        "all", description="Filter by document type: 'lesson', 'book', or 'all'"
    ),
    top_k: int = Query(
        5, ge=1, le=20, description="Number of top results to return"),
):
    """
    Semantic search through lessons and books using FAISS.
    """
    if not q or not q.strip():
        raise HTTPException(
            status_code=422, detail="Query string cannot be empty.")

    try:
        raw_results = search_lessons(q, top_k=top_k)

        if type.lower() in ["lesson", "book"]:
            filtered = [r for r in raw_results if r.get(
                "type") == type.lower()]
        else:
            filtered = raw_results

        filtered = sorted(
            filtered, key=lambda x: x.get("normalized_score", 0), reverse=True
        )
        return {"query": q, "results": filtered, "count": len(filtered), "filter": type}

    except Exception as e:
        logger.error(f"Error during semantic search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def build_prompt_from_context(
    question: str, lang: str, context_chunks: list[dict]
) -> str:
    if not question or not question.strip():
        logger.error("Empty question input")
        raise HTTPException(
            status_code=400, detail="Question input cannot be empty.")
    if not context_chunks:
        logger.error("Empty context chunks")
        raise HTTPException(
            status_code=400, detail="Context chunks cannot be empty.")
    if not isinstance(context_chunks, list):
        logger.error("Invalid context chunks format")
        raise HTTPException(
            status_code=400, detail="Context chunks must be a list.")

    context_text = "\n\n".join(
        f"[{chunk.get('type')}] {chunk.get('text', '')}" for chunk in context_chunks
    )
    instructions = (
        "Responde exclusivamente en español. Sé conciso, claro y pastoral. Basa tu respuesta únicamente en el contenido proporcionado en el contexto. "
        "Si el contexto no contiene suficiente información, dilo con honestidad."
        if lang == "es"
        else "Respond exclusively in English. Be concise, clear, and Christ-centered. Use only the provided context. If insufficient, state it honestly."
    )
    return f"""
        Usa el siguiente contexto para responder la pregunta de forma clara, espiritual y pastoral. Si el contexto no es suficiente, dilo con honestidad.

        <Contexto>
        {context_text}
        </Contexto>

        <Pregunta>
        {question}
        </Pregunta>

        <Instrucciones>
        {instructions}
        </Instrucciones>
    """


@router.post("/llm/answer")
def generate_answer(payload: QARequest):
    if not payload.question or not payload.question.strip():
        raise HTTPException(
            status_code=400, detail="La pregunta no puede estar vacía.")

    try:
        context_chunks = search_lessons(payload.question, top_k=payload.top_k)
        if not context_chunks:
            raise HTTPException(
                status_code=404,
                detail="No se encontró contexto relevante para esta pregunta.",
            )

        prompt = build_prompt_from_context(
            payload.question, payload.lang, context_chunks
        )
        answer = generate_llm_response(prompt, mode="reflect")

        return {
            "question": payload.question,
            "answer": answer,
            "context_used": len(context_chunks),
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(
            status_code=400, detail=f"Error de validación: {str(ve)}")
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

from fastapi import APIRouter, Body, HTTPException, Query
from typing import Literal
from app.indexing.search_service import search_lessons
from app.services.llm_service import generate_llm_response
from app.services.cms_service import (
    load_lesson_by_path,
    load_metadata_by_path,
    get_lesson_pdf_path,
    list_all_lessons,
)


router = APIRouter()


@router.get("/lessons/{year}/{quarter}/{lesson_id}")
def get_lesson(year: str, quarter: str, lesson_id: str):
    """
    Returns the full lesson.json file for a given year, quarter, and lesson ID.
    Example: /api/v1/lessons/2025/Q2/lesson_06
    """
    try:
        return load_lesson_by_path(year, quarter, lesson_id)
    except FileNotFoundError:
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
        raise HTTPException(status_code=404, detail="Metadata not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error loading metadata")


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
        raise HTTPException(status_code=404, detail="PDF file not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error loading PDF")


@router.get("/lessons")
def list_lessons():
    """
    Returns a list of all lessons available in the system.
    Example: /api/v1/lessons
    """
    try:
        return list_all_lessons()
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to list lessons")


@router.post("/llm")
def process_llm(
    text: str = Body(..., embed=True),
    mode: Literal["explain", "reflect", "apply", "summarize"] = Body(..., embed=True),
    lang: str = Query("en", description="Response language, e.g. 'en' or 'es'"),
):
    try:
        result = generate_llm_response(text, mode, lang)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
def semantic_search(
    q: str = Query(..., description="Search query text"),
    type: str = Query(
        "all", description="Filter by document type: 'lesson', 'book', or 'all'"
    ),
    top_k: int = Query(5, ge=1, le=20, description="Number of top results to return"),
):
    """
    Semantic search through lessons and books using FAISS.
    """
    try:
        raw_results = search_lessons(q, top_k=top_k)

        if type.lower() in ["lesson", "book"]:
            filtered = [r for r in raw_results if r.get("type") == type.lower()]
        else:
            filtered = raw_results

        return {"query": q, "results": filtered, "count": len(filtered), "filter": type}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

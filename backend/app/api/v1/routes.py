from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.cms_service import (
    load_lesson_by_path,
    load_metadata_by_path,
    get_lesson_pdf_path
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
        raise HTTPException(
            status_code=500, detail="Unexpected error loading metadata")


@router.get("/lessons/{year}/{quarter}/{lesson_id}/pdf")
def get_lesson_pdf(year: str, quarter: str, lesson_id: str):
    """
    Returns the PDF file for a given year, quarter, and lesson ID.
    Example: /api/v1/lessons/2025/Q2/lesson_06/pdf
    """
    try:
        pdf_path = get_lesson_pdf_path(year, quarter, lesson_id)
        return FileResponse(pdf_path, media_type='application/pdf', filename=f"{lesson_id}.pdf")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="PDF file not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error loading PDF")

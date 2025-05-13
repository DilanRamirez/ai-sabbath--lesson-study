import faiss
import json
import numpy as np
from pathlib import Path
from app.indexing.embeddings import embed_text

# Path setup
BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "lesson_index.faiss"
METADATA_FILE = BASE_DIR / "lesson_index_meta.json"


def search_lessons(query: str, top_k: int = 5) -> list[dict]:
    # Load index and metadata
    index = faiss.read_index(str(INDEX_FILE))
    with open(str(METADATA_FILE), "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(f"🔍 Searching for '{query}'...")
    # Embed the query
    query_vector = embed_text(query)
    D, I = index.search(np.array([query_vector], dtype="float32"), top_k)

    results = []
    for score, idx in zip(D[0], I[0]):
        if idx < 0 or idx >= len(metadata):
            continue

        meta = metadata[idx]
        result = meta.copy()
        result["score"] = float(score)
        result["text"] = ""
        try:
            with open(meta["source"], "r", encoding="utf-8") as f:
                data = json.load(f)

                if meta["type"] == "lesson-section":
                    # your existing lesson logic
                    section = data.get("lesson", {}).get("daily_sections", [])[
                        meta["day_index"]
                    ]
                    result["text"] = " ".join(section.get("content", []))

                elif meta["type"] == "book-section":
                    # support De_la_Ciudad_al_Campo metadata which uses section_number and item_title
                    sections = data.get("sections", [])
                    # determine section index (metadata may use section_index or section_number)
                    section_idx = meta.get("section_index", meta.get("section_number"))

                    if section_idx is not None and 0 <= section_idx < len(sections):
                        section_item = next(
                            (
                                sec
                                for sec in sections
                                if sec.get("section_number") == section_idx
                            ),
                            None,
                        )
                        items = (
                            section_item.get("items", [])
                            if section_item is not None
                            else []
                        )
                        # try to find the item by book-section-id first
                        book_section_id = meta.get("book-section-id")
                        found_item = None
                        if book_section_id:
                            for item in items:

                                if item.get("book-section-id") == book_section_id:
                                    found_item = item
                                    break
                        if not found_item:
                            # fallback: find by title if no explicit id match
                            page_number = meta.get("page_number")
                            for item in items:
                                if item.get("page") == page_number:
                                    found_item = item
                                    break
                        if found_item:
                            result["text"] = found_item.get("content", "")
                        else:
                            result["text"] = ""
                    else:
                        result["text"] = ""

                else:
                    # fallback: load entire flat text
                    result["text"] = data.get("content") or data.get("text", "")

        except Exception as e:
            result["error"] = f"Error loading content: {e}"

        results.append(result)

    return results

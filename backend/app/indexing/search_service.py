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

    # Embed the query
    query_vector = embed_text(query)
    D, I = index.search(np.array([query_vector]).astype("float32"), top_k)

    results = []
    for score, idx in zip(D[0], I[0]):
        if idx >= len(metadata):
            continue

        meta = metadata[idx]
        result = meta.copy()
        result["score"] = float(score)  # lower = more similar
        result["text"] = ""  # will load below

        try:
            with open(meta["source"], "r", encoding="utf-8") as f:
                data = json.load(f)

                # 🔍 Load exact chunk content
                if meta["type"] == "lesson-section":
                    section = data.get("lesson", {}).get("daily_sections", [])[
                        meta["day_index"]
                    ]
                    result["text"] = " ".join(section.get("content", []))
                elif meta["type"] == "book-chapter":
                    chapter = data.get("chapters", [])[meta["chapter_index"]]
                    result["text"] = chapter.get("content", chapter.get("text", ""))
        except Exception as e:
            result["error"] = f"Error loading content: {e}"

        results.append(result)

    return results

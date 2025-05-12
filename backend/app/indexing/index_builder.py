import os
import json
import faiss
import numpy as np
from pathlib import Path
from app.indexing.embeddings import embed_text

# Output locations
OUTPUT_DIR = Path(__file__).resolve().parent
INDEX_FILE = OUTPUT_DIR / "lesson_index.faiss"
METADATA_FILE = OUTPUT_DIR / "lesson_index_meta.json"

# Input directories
LESSON_DIR = OUTPUT_DIR.parent / "data"
BOOK_DIR = LESSON_DIR / "books"


def build_index():
    print("🔍 Building index...")
    texts = []
    metadata = []

    # --- Index Lessons (by daily section) ---
    for root, dirs, files in os.walk(LESSON_DIR):
        for file in files:
            if file != "lesson.json":
                continue

            path = os.path.join(root, file)

            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    lesson = data.get("lesson", {})
                    sections = lesson.get("daily_sections", [])

                    for i, section in enumerate(sections):
                        content_list = section.get("content", [])
                        text = " ".join(content_list).strip()
                        if not text:
                            continue

                        texts.append(text)
                        metadata.append(
                            {
                                "type": "lesson-section",
                                "lesson_id": lesson.get("id"),
                                "lesson_number": lesson.get("lesson_number"),
                                "title": lesson.get("title"),
                                "week_end_date": lesson.get("week_end_date"),
                                "day_index": i,
                                "day_title": section.get("title", f"Section {i+1}"),
                                "source": path,
                            }
                        )

            except Exception as e:
                print(f"⚠️ Skipping lesson {path}: {e}")

    # --- Index Books (by chapter) ---
    if BOOK_DIR.exists():
        # BOOK CHUNKING
        for file in os.listdir(BOOK_DIR):
            if not file.endswith(".json"):
                continue

            path = BOOK_DIR / file
            print(f"📖 Indexing book: {file}")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    book = json.load(f)
                    title = book.get("name", file)
                    chapters = book.get("verses")

                    if chapters and isinstance(chapters, list):
                        for i, chapter in enumerate(chapters):
                            text = chapter.get("text") or ""
                            text = text.strip()
                            if not text:
                                continue

                            texts.append(text)
                            metadata.append(
                                {
                                    "type": "book-chapter",
                                    "book_title": title,
                                    "chapter_index": i,
                                    "chapter_title": chapter.get(
                                        "title", f"Chapter {i+1}"
                                    ),
                                    "source": str(path),
                                }
                            )
                    else:
                        # Fallback for flat book content
                        flat_text = book.get("content") or book.get("text") or ""
                        if flat_text.strip():
                            texts.append(flat_text.strip())
                            metadata.append(
                                {
                                    "type": "book",
                                    "book_title": title,
                                    "source": str(path),
                                }
                            )

            except Exception as e:
                print(f"⚠️ Skipping book {file}: {e}")

    # --- Final check ---
    if not texts:
        print("⚠️ No documents found to index. Exiting.")
        return

    print(f"✅ Found {len(texts)} content chunks. Embedding...")

    vectors = [embed_text(t) for t in texts]
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors).astype("float32"))

    print("💾 Writing index and metadata...")
    faiss.write_index(index, str(INDEX_FILE))
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ Successfully indexed {len(texts)} chunks.")
    print(f"📁 Index: {INDEX_FILE}")
    print(f"📁 Metadata: {METADATA_FILE}")


if __name__ == "__main__":
    build_index()

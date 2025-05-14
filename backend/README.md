## folder structure

```
backend/
├── app/
│ ├── core/
│ │ ├── config.py # Env/settings loader (ADMIN_KEY, ADMIN_USERNAME)
│ │ └── security.py # X‑API‑Key dependency, auth helpers
│ │
│ ├── indexing/
│ │ ├── embeddings.py # embed_text, vector conversion
│ │ ├── search_service.py # IndexStore, preload, search_lessons
│ │ └── index_builder.py # build_index script
│ │
│ ├── api/
│ │ └── v1/
│ │ ├── routes.py # Public endpoints (/search, /llm, /llm/answer, lessons)
│ │ └── admin_routes.py # Protected admin endpoints (/admin/reindex, /admin/status)
│ │
│ ├── services/
│ │ ├── llm_service.py # generate_llm_response wrapper
│ │ └── cms_service.py # load_lesson_by_path, metadata, PDF helper
│ │
│ ├── data/ # Raw lesson/book JSON and PDFs
│ │ ├── 2025/
│ │ │ └── Q2/
│ │ │ ├── lesson-06/
│ │ │ │ ├── lesson.json
│ │ │ │ ├── metadata.json
│ │ │ │ └── lesson.pdf
│ │ │ └── …
│ │ └── books/
│ │ ├── el_camino_a_cristo.json
│ │ └── …
│ │
│ ├── main.py # FastAPI app instantiation, lifespan, router includes
│ ├── Dockerfile
│ └── docker-compose.yml
│
├── tests/
│ ├── test_search_service.py
│ ├── test_llm_modes.py
│ ├── test_llm_answer_service.py
│ ├── test_lessons_routes.py
│ └── test_llm_service.py
│
├── requirements.txt
└── Makefile
```

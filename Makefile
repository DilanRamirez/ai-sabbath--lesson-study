# Makefile

# Run backend unit tests
test-backend:
	cd backend && pytest tests --maxfail=1 --disable-warnings -q

# Format backend using black
format-backend:
	cd backend && black .

# Check formatting (used in GHA)
check-format-backend:
	cd backend && black --check .

# Run the GitHub Actions workflow locally
test-gha:
	act -j backend-tests -W .github/workflows/backend.yml --container-architecture linux/amd64

# Full local CI simulation
ci:
	make check-format-backend
	make test-backend

# Build or rebuild the semantic FAISS index for lessons + books
index:
	PYTHONPATH=backend python backend/app/indexing/index_builder.py

api-server:
	cd backend && uvicorn app.main:app --reload


up:
	docker compose up --build
down:
	docker compose down
stop:
	docker compose stop
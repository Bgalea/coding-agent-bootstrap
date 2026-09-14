# Automation Makefile with Local Vector Memory & Quality Gates

.PHONY: help setup-memory index-memory search-memory lint test

VENV = .agents/.venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "=================================================="
	@echo "           PROJECT AUTOMATION TASKS               "
	@echo "=================================================="
	@echo "  make setup-memory        Install local vector memory & pre-fetch model"
	@echo "  make index-memory        Index codebase into local Qdrant vector database"
	@echo "  make search-memory q=... Instant semantic search (< 1s, sandbox-safe)"
	@echo "  make lint                Run project linters and style checks"
	@echo "  make test                Run test suite locally"
	@echo "=================================================="

setup-memory:
	@echo "Setting up isolated vector memory environment in $(VENV)..."
	@python3 -m venv $(VENV)
	@$(PIP) install --quiet --upgrade pip
	@$(PIP) install --quiet -r .agents/requirements-memory.txt
	@echo "Pre-fetching FastEmbed model to .agents/data/fastembed_cache/ (Sandbox-Safe)..."
	@$(PYTHON) -c "from fastembed import TextEmbedding; import os; os.makedirs('.agents/data/fastembed_cache', exist_ok=True); TextEmbedding(model_name='sentence-transformers/all-MiniLM-L6-v2', cache_dir='.agents/data/fastembed_cache')"
	@echo "Vector memory ready! Run 'make index-memory' to index your codebase."

index-memory:
	@if [ ! -f $(PYTHON) ]; then \
		echo "Memory environment not found. Running 'make setup-memory' first..."; \
		$(MAKE) setup-memory; \
	fi
	@$(PYTHON) .agents/scripts/index_codebase.py

search-memory:
	@if [ ! -f $(PYTHON) ]; then \
		echo "Memory environment not found. Please run 'make setup-memory' first."; \
		exit 1; \
	fi
	@if [ -z "$(q)" ]; then \
		echo "Error: Please specify query parameter. Example:"; \
		echo "  make search-memory q=\"user authentication handler\""; \
		exit 1; \
	fi
	@$(PYTHON) .agents/scripts/search_codebase.py "$(q)"

lint:
	@if command -v ruff >/dev/null 2>&1; then \
		ruff check . && ruff format --check .; \
	elif command -v npx >/dev/null 2>&1; then \
		npx eslint .; \
	else \
		echo "No linter detected (ruff or eslint)."; \
	fi

test:
	@if command -v pytest >/dev/null 2>&1; then \
		pytest; \
	elif command -v npm >/dev/null 2>&1; then \
		npm test; \
	else \
		echo "No test runner detected (pytest or npm test)."; \
	fi

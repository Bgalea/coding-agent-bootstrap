#!/usr/bin/env python3
"""
Semantic Codebase Search for Autonomous Agents.
Performs fast (< 1s), local vector search over the codebase without requiring external API calls or network access.
"""

import os
import sys

try:
    from fastembed import TextEmbedding
    from qdrant_client import QdrantClient
except ImportError:
    print("Error: Missing memory dependencies.")
    print("Run 'make setup-memory' or install from '.agents/requirements-memory.txt'")
    sys.exit(1)

# Base Paths (Relative to repository root)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AGENTS_DIR = os.path.join(ROOT_DIR, ".agents")
DATA_DIR = os.path.join(AGENTS_DIR, "data")
CACHE_DIR = os.path.join(DATA_DIR, "fastembed_cache")
DB_PATH = os.path.join(DATA_DIR, "qdrant_db")
COLLECTION_NAME = "codebase_memory"


def search(query, limit=5):
    if not os.path.exists(DB_PATH):
        print(f"Error: Local vector database not found at {DB_PATH}.")
        print("Please run 'make index-memory' first to index your codebase.")
        sys.exit(1)

    client = QdrantClient(path=DB_PATH)
    
    # Check if collection exists
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        print(f"Error: Collection '{COLLECTION_NAME}' not found.")
        print("Please run 'make index-memory' to build the index.")
        sys.exit(1)

    embedder = TextEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_dir=CACHE_DIR
    )

    query_vector = list(embedder.embed([query]))[0].tolist()

    # Search in Qdrant
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit
    )

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python search_codebase.py \"<query>\" [limit]")
        print("Example: python search_codebase.py \"user authentication JWT\" 5")
        sys.exit(1)

    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    print(f"Searching local codebase memory for: '{query}' (limit={limit})...\n")
    results = search(query, limit)

    if not results:
        print("No matching code chunks found.")
        return

    print(f"Found {len(results)} relevant matches:\n")
    for idx, hit in enumerate(results, 1):
        payload = hit.payload
        file_path = payload.get("file_path", "unknown")
        start_line = payload.get("start_line", "?")
        end_line = payload.get("end_line", "?")
        score = hit.score
        text = payload.get("text", "")

        print("=" * 60)
        print(f"Match #{idx} (Score: {score:.4f}) -> {file_path} [Lines {start_line}-{end_line}]")
        print("-" * 60)
        print(text)
        print("")


if __name__ == "__main__":
    main()

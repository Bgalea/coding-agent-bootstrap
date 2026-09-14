#!/usr/bin/env python3
"""
Codebase Indexer for Local Vector Memory.
Embeds source files using local FastEmbed (ONNX) and stores vectors into an embedded Qdrant database.
Fully autonomous, sandbox-confined, and runs without external network dependencies once cached.
"""

import os
import sys
import time
import uuid

try:
    from fastembed import TextEmbedding
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
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

# Ignored directories and files
IGNORED_DIRS = {
    ".git", ".venv", "venv", "env", ".agents/.venv", ".agents/data", "data",
    "node_modules", "__pycache__", "dist", "build", ".pytest_cache",
    ".ruff_cache", ".mypy_cache", ".next", ".nuxt", ".turbo", "target",
    "bin", "obj", ".idea", ".vscode"
}

ALLOWED_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java",
    ".cpp", ".c", ".h", ".cs", ".rb", ".php", ".swift", ".kt",
    ".sql", ".sh", ".bash", ".md", ".json", ".yml", ".yaml", ".toml"
}

ALLOWED_FILENAMES = {
    "Makefile", "Dockerfile", "Containerfile", "Procfile", ".cursorrules", "CLAUDE.md"
}

CHUNK_SIZE_LINES = 40
CHUNK_OVERLAP_LINES = 10
MAX_FILE_SIZE_BYTES = 500 * 1024  # 500 KB


def should_index_file(rel_path):
    """Check whether a file should be indexed."""
    parts = rel_path.split(os.sep)
    for part in parts[:-1]:
        if part in IGNORED_DIRS or part.startswith('.'):
            if part not in {".agents", ".cursor"}:
                return False

    filename = os.path.basename(rel_path)
    if filename in ALLOWED_FILENAMES:
        return True
    
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS


def chunk_file(filepath, rel_path):
    """Split a file into overlapping line chunks."""
    try:
        if os.path.getsize(filepath) > MAX_FILE_SIZE_BYTES:
            return []
        
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return []

    if not lines:
        return []

    chunks = []
    total_lines = len(lines)
    start = 0

    while start < total_lines:
        end = min(start + CHUNK_SIZE_LINES, total_lines)
        chunk_lines = lines[start:end]
        text_content = "".join(chunk_lines).strip()

        if text_content:
            chunks.append({
                "file_path": rel_path,
                "start_line": start + 1,
                "end_line": end,
                "text": f"File: {rel_path} (Lines {start + 1}-{end})\n\n{text_content}"
            })

        if end >= total_lines:
            break
        start += (CHUNK_SIZE_LINES - CHUNK_OVERLAP_LINES)

    return chunks


def update_agents_code_map(indexed_files_count, total_chunks, domains):
    """Update the <!-- START_CODE_MAP --> block in .agents/AGENTS.md."""
    agents_md = os.path.join(AGENTS_DIR, "AGENTS.md")
    if not os.path.exists(agents_md):
        return

    start_tag = "<!-- START_CODE_MAP -->"
    end_tag = "<!-- END_CODE_MAP -->"

    try:
        with open(agents_md, "r", encoding="utf-8") as f:
            content = f.read()

        if start_tag not in content or end_tag not in content:
            return

        map_lines = [
            f"\n### Local Vector Index Overview (Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')})",
            f"* **Total Indexed Files**: {indexed_files_count}",
            f"* **Total Code Chunks**: {total_chunks}",
            f"* **Embedded Qdrant Store**: `.agents/data/qdrant_db/` (FastEmbed `all-MiniLM-L6-v2`)",
            "",
            "| Domain / Directory | Files Count |",
            "|---|---|"
        ]

        for domain, count in sorted(domains.items()):
            map_lines.append(f"| `{domain}` | {count} |")
        map_lines.append("")

        replacement = f"{start_tag}\n" + "\n".join(map_lines) + f"\n{end_tag}"
        before = content.split(start_tag)[0]
        after = content.split(end_tag)[1]
        new_content = before + replacement + after

        with open(agents_md, "w", encoding="utf-8") as f:
            f.write(new_content)
    except Exception as e:
        print(f"Warning: Could not update AGENTS.md code map: {e}")


def main():
    print("==================================================")
    print("     INDEXING CODEBASE INTO LOCAL VECTOR STORE    ")
    print("==================================================")
    print(f"Repository Root : {ROOT_DIR}")
    print(f"Embedding Cache : {CACHE_DIR}")
    print(f"Qdrant Storage  : {DB_PATH}")

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    start_time = time.time()

    # 1. Discover files
    print("\n1. Scanning project files...")
    all_chunks = []
    indexed_files = 0
    domains = {}

    for root, dirs, files in os.walk(ROOT_DIR):
        # Exclude directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith('.')]
        
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, ROOT_DIR)
            
            if should_index_file(rel_path):
                chunks = chunk_file(full_path, rel_path)
                if chunks:
                    all_chunks.extend(chunks)
                    indexed_files += 1
                    domain = rel_path.split(os.sep)[0]
                    domains[domain] = domains.get(domain, 0) + 1

    print(f"   Found {indexed_files} files, split into {len(all_chunks)} semantic chunks.")

    if not all_chunks:
        print("No indexable code files found. Skipping indexing.")
        return

    # 2. Initialize embedding model
    print("\n2. Initializing local FastEmbed model (sentence-transformers/all-MiniLM-L6-v2)...")
    embedder = TextEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_dir=CACHE_DIR
    )

    # 3. Initialize local Qdrant database
    print("3. Connecting to local embedded Qdrant database...")
    client = QdrantClient(path=DB_PATH)

    # Recreate collection
    vector_size = 384  # all-MiniLM-L6-v2 output dimension
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

    # 4. Generate embeddings and upsert points
    print(f"4. Generating embeddings and storing into '{COLLECTION_NAME}'...")
    texts = [c["text"] for c in all_chunks]
    
    batch_size = 64
    total_chunks = len(all_chunks)

    for i in range(0, total_chunks, batch_size):
        batch_chunks = all_chunks[i:i + batch_size]
        batch_texts = texts[i:i + batch_size]

        embeddings = list(embedder.embed(batch_texts))
        points = []

        for chunk, emb in zip(batch_chunks, embeddings):
            point_id = str(uuid.uuid4())
            points.append(
                PointStruct(
                    id=point_id,
                    vector=emb.tolist(),
                    payload={
                        "file_path": chunk["file_path"],
                        "start_line": chunk["start_line"],
                        "end_line": chunk["end_line"],
                        "text": chunk["text"]
                    }
                )
            )

        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"   Indexed chunks {min(i + batch_size, total_chunks)} / {total_chunks}")

    # 5. Update code map in AGENTS.md
    update_agents_code_map(indexed_files, total_chunks, domains)

    elapsed = time.time() - start_time
    print("\n==================================================")
    print(f"INDEXING COMPLETE in {elapsed:.2f}s!")
    print(f"  Files Indexed : {indexed_files}")
    print(f"  Chunks Stored : {total_chunks}")
    print(f"  Vector Store  : {DB_PATH}")
    print("You can now search semantically with:")
    print("  make search-memory q=\"your query\"")
    print("==================================================")


if __name__ == "__main__":
    main()

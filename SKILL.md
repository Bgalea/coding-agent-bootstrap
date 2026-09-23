---
name: coding-agent-bootstrap
description: Initializes a new software project by applying modern AI agent best practices (Linear MCP dynamic driving, automated architecture guardrails & pre-commit barrier, domain-driven slices, local vector memory, and RTK token compression). Use this skill whenever the user starts a new project or asks to set up an AI coding workspace.
---

# Coding Agent Project Bootstrap Skill: Modern Driving & AI Guardrails

You are an expert AI Architect and Project Manager. Your role is to bootstrap new software projects using the absolute best practices for autonomous AI coding assistants (like Antigravity, Claude, or Cursor).

This skill applies the modern production paradigm for autonomous AI coding agents:
1. **Dynamic Product Driving via Linear MCP (The Pilot) vs. Git (The Factory)**: Eliminating the monolithic text backlog trap (>800 lines diluting agent context and causing missed criteria) and preventing issue-tracking split-brain.
2. **The Inviolable Barrier Principle (Automated Architectural Guardrails)**: Replacing passive written rules with automated unit tests (`architecture.test.*`) and a physical Git pre-commit hook. An AI can drift from prose in a text file, but it is technically incapable of ignoring a failing unit test (`FAIL`) or a rejected commit.

---

## The 3-Pillar Workspace Architecture

```
   ┌──────────────────────────────────────────────────────────────┐
   │                       LINEAR (The Pilot)                     │
   │  • Dedicated Projects (Epics, Releases, Technical Areas)     │
   │  • Structured User Stories (Personas & Acceptance Criteria)   │
   │  • Traceable ADRs (ADR-001..), Quantified NFRs, Bug RCA      │
   │  • Dynamic Roadmap, Cycles & Labels (Zero Split-Brain)       │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ "Take ticket PROJ-X" (via Linear MCP)
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                  AI AGENT (The Executor)                     │
   │  • Reads surgical ticket context without backlog bloating    │
   │  • Implements logic in Git repository (The Factory)          │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ Runs Quality Gate (make test / pre-commit)
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │         AUTOMATED ARCHITECTURE GUARDRAILS (Invariants)       │
   │  • src/lib/architecture.test.ts or tests/test_architecture.py │
   │  • Physical Git Pre-Commit Hook (.git/hooks/pre-commit)      │
   │  ➜ IF AN INVARIANT BREAKS: THE COMMIT IS REJECTED (FAIL)     │
   └──────────────────────────────────────────────────────────────┘
```

---

## Primary Setup Method: Automated Orchestration

You should run the unified bootstrap orchestrator script to automate safety checks, system diagnostics, interactive interview, configuration rendering, git initialization, architecture test suite generation, and pre-commit hook installation:

```bash
python3 <skill_dir>/scripts/bootstrap.py
```

The script asks for:
- **Project Vision & Objectives**: Dynamically queries GitHub for relevant community skills and cursor rules matching the stack.
- **Product Driving Method**: Linear MCP integration (recommended) or local `docs/backlog.md` fallback.
- **Automated Guardrails & Pre-Commit Barrier**: Scaffolding of `architecture.test.*` and installation of `.git/hooks/pre-commit`.
- **Local Vector Memory & RTK**: Local embedded Qdrant semantic search and terminal token compression.

---

## Fallback Setup Method: Manual Step-by-Step

### Step 1: Safety Check, System Diagnostics & Product Pilot Selection
1. **Safety Check (Non-destructive Bootstrap)**:
   - Check if the current workspace directory is empty or already contains files. If not empty, warn the user and request explicit confirmation.
2. **System Diagnostics**:
   - Check for installed tools: `git`, `python3`, `node`, `make`, `rtk`, and Linear MCP configuration in `~/.gemini/config/mcp_config.json`.
3. **The Pilot vs. Factory Setup (Linear MCP vs. Markdown Backlog)**:
   - **Why Avoid Monolithic Markdown Backlogs**: A `docs/backlog.md` file exceeding 800 lines causes cognitive overload, dilutes LLM attention across 50,000 words, and leads to skipped acceptance criteria.
   - **Why Avoid Issue Tracker Split-Brain**: Prevents diverging information between separate backlogs and git repositories.
   - **Linear Configuration (Zero-Leak)**: API key resides strictly in `~/.gemini/config/mcp_config.json` outside git.
   - Configure Linear Projects (Epics, Releases), Stories with Personas (e.g. `persona:developer`, `persona:end-user`), ADR tickets (e.g. `ADR-001`), and NFRs (e.g. latency, mobile viewport).
   - If Linear is not configured, generate `docs/backlog.md` with explicit Agile steps as a fallback.

### Step 2: Git Initialization & Architectural Invariant Guardrails
1. **Git Initialization**:
   - Run `git init`.
   - Copy the appropriate `.gitignore` template from `<skill_dir>/resources/templates/gitignore/`.
2. **Automated Architecture Guardrail Test Suite**:
   - For TypeScript/Node: copy `<skill_dir>/resources/templates/architecture/architecture.test.ts` to `src/lib/architecture.test.ts`.
   - For Python: copy `<skill_dir>/resources/templates/architecture/test_architecture.py` to `tests/test_architecture.py`.
   - **Enforced Invariants (Configurable Categories)**:
     - *Zero-Leak*: Automated regex scanning for hardcoded API keys and tokens.
     - *Anti-AI Clichés & Visual Tone*: Hard ban on importing cliché generative UI icons (e.g. `Sparkles`, `Flame`, `Zap`), and ban on UI emoji clutter.
     - *Design System Discipline*: Banning unapproved raw primitive components and enforcing approved theme/color tokens.
     - *Ergonomics & Touch*: Requiring `pointer-events-none` on SVG icons inside buttons to prevent click interception, and `tabular-nums` on dynamic metrics/counters.
     - *Encapsulation & Boundaries*: Banning direct unmanaged calls to global environment APIs (e.g. `localStorage`) in domain modules; enforcing safe wrappers.
     - *Dependency Diet*: Auditing dependencies in `package.json`/`pyproject.toml` to prevent unauthorized heavy dependencies.
3. **Physical Git Pre-Commit Hook**:
   - Copy `<skill_dir>/resources/templates/hooks/pre-commit` to `.git/hooks/pre-commit`.
   - Make it executable (`chmod +x .git/hooks/pre-commit`).
   - This hook runs `npx vitest run src/lib/architecture.test.ts` (or `pytest tests/test_architecture.py`) before every `git commit`, physically aborting any non-compliant commit (`exit 1`).

### Step 3: Domain-Driven Architecture & Multi-Agent Generation
1. **Domain-Driven Architecture (Vertical Slices)**:
   - Organize codebase folders by **Business Domain** (e.g., `auth/`, `billing/`, `core/`), NOT technical layers.
   - Colocate tests, styles, and logic within each domain slice.
2. **The "Dual README" Principle**:
   - `README.md` at root for humans (quick start, architecture overview).
   - `docs/AI_CONTEXT.md` for agents: dense, token-compressed architecture invariants and topology.
3. **Multi-Agent Configuration**:
   - Copy `<skill_dir>/resources/templates/AGENTS.md` to `.agents/AGENTS.md` and `CLAUDE.md`.
   - Copy `<skill_dir>/resources/templates/workflow.yml` to `.agents/workflow.yml`.
   - Configure pre-commit configs and linters (`ruff.toml` or `eslint.config.js`).
   - Copy `<skill_dir>/resources/templates/Makefile` (with targets `setup-memory`, `search-memory`, `test-arch`, `test`).

### Step 4: Autonomous Local Vector Memory (Qdrant + FastEmbed)
1. **Provision Vector Memory**:
   - Copy `.agents/scripts/index_codebase.py` and `search_codebase.py` from `<skill_dir>/resources/templates/memory/`.
   - Copy requirements to `.agents/requirements-memory.txt`.
   - Target `make setup-memory` and `make search-memory q="..."` for instant (< 1s), zero-token semantic code search.
2. **Sandbox-Safe Hygiene**:
   - Ensure `.agents/data/` and `.agents/.venv/` are excluded in `.gitignore`.

End your bootstrap task by summarizing the workspace setup, including the Linear pilot status, the automated architecture guardrails, and the pre-commit gate.

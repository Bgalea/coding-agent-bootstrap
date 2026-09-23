# Coding Agent Bootstrap Skill

This repository contains a **Skill** for autonomous AI coding assistants (like Google Antigravity, Claude, or Cursor). 

The `coding-agent-bootstrap` skill automates the setup of a new software project by applying battle-tested industry best practices. It establishes a modern 3-pillar architecture: **Linear as the Pilot**, **Git as the Factory**, and **Automated Architecture Guardrails as Invariants**.

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

## Features

- **Modern Product Driving (Linear MCP vs. Factory Git)**:
  - Eliminates the **Static Backlog Trap**: monolithic markdown backlogs (>800 lines) flood context windows with 50,000+ words, diluting attention and causing agents to miss vital acceptance criteria.
  - Prevents the **Split-Brain Trap**: avoids duplicate ticket management and diverging information across disconnected trackers.
  - Pilot directly via natural language: *"Take ticket PROJ-11"*. The agent fetches the exact ticket and its acceptance criteria via Linear MCP with surgical token efficiency.
  - Secure Zero-Leak protocol: API keys reside strictly on your local machine (`~/.gemini/config/mcp_config.json`), outside Git.
- **Automated Architectural Guardrails ("Inviolable Barriers")**:
  - *The Principle*: An AI agent can ignore prose in a markdown file, but it cannot ignore a failing unit test in the terminal (`FAIL`).
  - Pre-built, customizable test suite (`src/lib/architecture.test.ts` or `tests/test_architecture.py`) enforcing invariants at every test run and commit:
    - **Security & Zero-Leak**: Catches hardcoded API keys and tokens before commits.
    - **Anti-AI Clichés & Tone**: Blocks stereotypical generative UI icons (e.g. `Sparkles`, `Flame`, `Zap`) and prohibits decorative emoji clutter in user-facing UI labels.
    - **Design System Invariants**: Prevents raw primitive components (e.g. unstyled `<button>`) and detects unapproved colors or styling utility classes.
    - **Interface Ergonomics**: Enforces click/touch event reliability (`pointer-events-none` on inner button SVGs) and figure alignment (`tabular-nums` on dynamic metrics/counters).
    - **Encapsulation & Boundaries**: Bans direct unmanaged calls to global browser storage (e.g. `window.localStorage`) in domain modules; mandates safe wrappers for SSR/private browsing.
    - **Dependency Diet**: Automatically audits `package.json`/`pyproject.toml` against unauthorized heavy third-party packages.
- **Physical Git Pre-Commit Hook Barrier**:
  - Automatically installs `.git/hooks/pre-commit` to execute the architecture test suite before every `git commit`.
  - Rejects non-compliant code physically (`exit 1`), making it impossible for an agent to commit violating code.
- **Vertical Slices Architecture**: Organizes your codebase by business domain instead of technical layers, drastically improving LLM context locality.
- **Dynamic Rules Sourcing**: Scrapes community repositories in real-time to fetch the best AI prompts for your specific stack.
- **Dual README Principle**: Generates a standard `README.md` for humans and a compressed `AI_CONTEXT.md` for machines.
- **RTK Terminal Compression**: Integrates with [RTK (Rust Token Killer)](https://github.com/rtk-ai/rtk) to reduce terminal output tokens by 60–90% on test suites (`pytest`, `vitest`, `cargo test`), linters (`ruff`, `eslint`, `tsc`), and git commands.
- **Autonomous Local Vector Memory (Sandbox-Safe)**: Embedded Qdrant vector database + FastEmbed (`all-MiniLM-L6-v2`) for instant (< 1s), zero-token semantic code search via `make search-memory q="..."`.
- **Multi-Agent Orchestration**: Templates a `workflow.yml` delegating tasks to specialized sub-agents with strict QA gates.

---

## Usage & Installation

### 1. Quick One-Line Installation (Recommended)
Run the following command in your terminal to automatically install or update the skill:
```bash
curl -fsSL https://raw.githubusercontent.com/Bgalea/coding-agent-bootstrap/main/install.sh | bash
```

### 2. Manual Installation for Google Antigravity
Clone this repository into your global skills directory:
```bash
git clone https://github.com/Bgalea/coding-agent-bootstrap.git ~/.gemini/config/skills/coding-agent-bootstrap
```
Once installed, simply ask your agent:
> *"I want to start a new project. Use the coding-agent-bootstrap skill."*

### 3. For Claude (Anthropic)
Copy and paste the contents of `SKILL.md` into Claude Projects system instructions.

### 4. For Cursor Editor
Paste `SKILL.md` content into `.cursorrules` or `.cursor/rules/bootstrap.mdc`.

---

## Requirements
- An autonomous AI assistant (Google Antigravity, Claude, Cursor, etc.).
- `python3` (for local orchestrator and vector memory scripts).
- Linear account & Linear MCP server configured (optional but highly recommended for dynamic product driving).
- `rtk` CLI (optional, recommended: `brew install rtk` to cut terminal output tokens by 60–90%).

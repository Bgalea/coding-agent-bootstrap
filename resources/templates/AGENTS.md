# AI Development Guidelines & Workspace Rules

> [!IMPORTANT]
> These rules are binding for all autonomous agents executing tasks in this workspace.

---

## 1. Modern Product Driving: Linear MCP vs. Factory Git

To eliminate cognitive overload, context dilution, and agent hallucinations, this workspace establishes the **Pilot vs. Factory** separation of concerns:

* **Linear = The PILOT (What to build & When)**:
  - Manages Epics, Releases, User Stories, Personas, Acceptance Criteria, Non-Functional Requirements (NFRs), and Architecture Decision Records (ADRs as traceable tickets).
  - Avoids the **Static Backlog Trap**: monolithic markdown backlogs (>800 lines) flood LLM context with 50,000+ words, diluting attention and causing agents to miss critical acceptance criteria.
  - Prevents the **GitHub Projects Split-Brain Trap**: avoids duplicate ticket management and diverging information.
* **Git / GitHub = The FACTORY (How it is built)**:
  - Houses source code, commit history, Pull Requests, and automated CI verification pipelines.
* **Direct Agent Operation via Linear MCP (Zero-Leak)**:
  - When asked: *"Take ticket PROJ-X"*, the agent uses Linear MCP (`get_issue`) to fetch the exact ticket, its acceptance criteria, and persona context with surgical token efficiency.
  - Upon completion and QA verification, the agent updates the ticket status (`save_issue`) and logs resolution notes (`save_comment`).
  - *Fallback*: If Linear MCP is not configured, agents must strictly maintain and update `docs/backlog.md`.

---

## 2. Automated Architecture Guardrails ("Inviolable Barriers" & Pre-Commit Hook)

> [!CAUTION]
> **The Inviolable Barrier Principle**: An AI agent may inadvertently drift from written instructions in a markdown file. However, an AI agent is technically incapable of ignoring a unit test that fails in the terminal (`FAIL`) or a `git commit` rejected by a pre-commit hook.

All architectural, visual, ergonomic, and security invariants are enforced by automated test suites (`src/lib/architecture.test.ts` or `tests/test_architecture.py`) and a physical Git pre-commit hook (`.git/hooks/pre-commit`):

1. **Security & Zero-Leak**:
   - Automated regex scanning prevents committing hardcoded API keys, private tokens, or credentials.
2. **Anti-AI Clichés & Visual Tone**:
   - Prevent stereotypical generative AI visual tropes (e.g. overused generic icons like `Sparkles`, `Flame`, `Zap` from iconography libraries).
   - Prohibit decorative emoji clutter in user-facing UI labels to maintain a sober, production-grade interface.
3. **Design System & Theme Invariants**:
   - Never bypass design system components with raw unstyled primitives (e.g., raw `<button>` when a project `BaseButton` is standard).
   - Strictly adhere to approved color tokens, typography scales, and theme palettes. Unapproved classes or colors fail the test suite.
4. **Ergonomics & Touch / Event Robustness**:
   - Interactive icon buttons must prevent inner SVG elements from intercepting touch or pointer events (`pointer-events-none`).
   - Numerical metrics, prices, and timers should enforce tabular figures (`tabular-nums`) to prevent layout shifting on updates.
   - Screen layouts must respect target viewport bounds without unintended horizontal or vertical scrollbars.
5. **Encapsulation & Storage Boundaries**:
   - Prohibit unmanaged direct access to global environment primitives (such as `window.localStorage` in domain modules). All storage must pass through a centralized wrapper ensuring SSR and private-browsing safety.
6. **Dependency Diet & Bloat Prevention**:
   - Prohibit the introduction of heavy, unvetted third-party packages in `package.json` or `pyproject.toml` when native or lightweight solutions are required.

---

## 3. Zero-Leak Secrets Security
* **NO HARDCODED SECRETS**: Never write real passwords, API keys, tokens, or credentials in any codebase file.
* **Environment Variables**: All configurations must be sourced via environment variables. Use the provided `.env.example` as a baseline.
* **Local MCP Protocol**: API keys for external services (Linear, LLM providers) reside strictly on the local machine (e.g. `~/.gemini/config/mcp_config.json`), never in the git repository.

---

## 4. No Vibecoding (Structured Engineering)
* **Planning Phase**: Before writing or modifying any source code, you MUST formulate a detailed implementation plan in an artifact.
* **Atomic Tasks**: Break all work down into small, logical sub-tasks taking 5-10 minutes each. Track tasks in `task.md` or dedicated Linear sub-issues.
* **Incremental Changes**: Make code changes incrementally. Write tests and verify compilation/build at each step.

---

## 5. Architecture & Code Quality
* **Vertical Slice Architecture**: Organize files by business domain (e.g. `auth/`, `billing/`, `core/`), NOT technical layer. Colocate tests, styles, and logic within each domain slice.
* **Strong Typing**: Strict static typing is mandatory. Bypassing types (`any` in TS, `Any` without reason in Python) is an automatic failure.
* **Clean Code**: Keep methods short and focused on a single responsibility. Preserve all comments and docstrings unless explicitly asked to modify them.

---

## 6. Token & Context Optimization
* **Semantic Codebase Search (< 1s, Zero-Token)**: Use `make search-memory q="your concept"` or run `.agents/scripts/search_codebase.py` before opening large files. Pinpoint exact functions and lines locally to avoid flooding context.
* **Terminal Token Optimization (RTK)**: When available, prefix test runners (`rtk pytest`, `rtk vitest`, `rtk cargo test`, `rtk jest`), linters (`rtk ruff check`, `rtk tsc`, `rtk eslint`), and git inspections (`rtk git status`, `rtk git diff`) with `rtk` to compress bash output by 60-90%.
* **Native Tool Boundary**: Never use `rtk read`, `rtk grep`, or `rtk find` via bash. Always prioritize Antigravity's native `view_file`, `grep_search`, and `find_by_name` tools.
* **Lazy Reading & Skill Loading**: Do not read large files or global skill instructions upfront. Use `view_file` on a specific skill's `SKILL.md` ONLY when preparing to execute a task explicitly requiring that skill.
* **Concise Communication**: Avoid conversational fluff. Keep responses dense, technical, and action-oriented.

---

## 7. QA Gates & Testing
* **Test Verification**: A developer agent cannot mark a user story or Linear ticket as "done" without running test suites.
* **Physical Pre-Commit Gate**: Commits must pass both linting and the automated architecture guardrails test suite.
* **QA Handoff**: Completed features must be handed off to a QA/testing step (or dedicated QA agent) for verification.

---

## 8. Activated Project-Specific Skills
The following specialized skills have been activated and recommended for this project:
${ACTIVATED_SKILLS}

---

## 9. Agile Iterative Loop Rules
All agents must adhere to the following 9-step Agile lifecycle:
1. **Vision Definition** (PO defines vision in Linear Project or `backlog.md`)
2. **Objectives Sourcing** (PO defines milestones/cycles)
3. **Epic & Feature Sourcing** (Architect defines Epics and intermediate deliverables/Features, mapping NFR requirements and Feature Acceptance Criteria)
4. **User Story Backlog** (PO writes functional acceptance criteria and personas in Linear / `backlog.md`)
5. **Feature Development** (Developer writes code and colocates tests targeting the current Feature)
6. **Iterative Local Testing** (Developer tests/fixes locally - **MAX 5 loops**. Verify functional criteria, NFR constraints, and run `architecture.test.*`. If tests still fail after 5 loops, stop and notify the human).
7. **Feature Branch Upload** (Developer commits code—enforced by pre-commit hooks—and pushes to a dedicated feature branch `feat/[feature-name]` to trigger GitHub Actions CI tests)
8. **GitHub Actions CI Verification** (QA monitors CI. If tests fail or NFR criteria are not met, developer returns to Step 5 to fix - **MAX 5 CI correction loops**. If still failing after 5 CI runs, stop and notify the human).
9. **Acceptance & Success** (PO reviews and signs off on User Stories and their parent Feature's acceptance criteria/NFRs before merging to the main branch).

<!-- START_CODE_MAP -->
<!-- This section will be automatically populated with the project codebase map -->
<!-- END_CODE_MAP -->

# AI Development Guidelines & Workspace Rules

> [!IMPORTANT]
> These rules are binding for all autonomous agents executing tasks in this workspace.

## 1. Zero-Leak Secrets Security
* **NO HARDCODED SECRETS**: Never write real passwords, API keys, tokens, or credentials in any codebase file.
* **Environment Variables**: All configurations must be sourced via environment variables. Use the provided `.env.example` as a baseline.
* **Consent Required**: You must request explicit human consent before creating or writing any file containing actual secret values (e.g. `.env`).

## 2. No Vibecoding (Structured Engineering)
* **Planning Phase**: Before writing or modifying any source code, you MUST formulate a detailed implementation plan in an artifact.
* **Atomic Tasks**: Break all work down into small, logical sub-tasks taking 5-10 minutes each. Track tasks in `task.md`.
* **Incremental Changes**: Make code changes incrementally. Write tests and verify compilation/build at each step.

## 3. Architecture & Code Quality
* **Vertical Slice Architecture**: Organize files by business domain (e.g. `auth/`, `payment/`), NOT technical layer. colocated tests, styles, and logic.
* **Strong Typing**: You must use strict static typing. Bypassing types is an automatic failure.
* **Clean Code**: Keep methods short and focused on a single responsibility. Preserve all comments and docstrings unless explicitly asked to modify them.

## 4. Token & Context Optimization
* **Lazy Reading**: Do not read large files fully unless absolutely necessary. Use `grep` or semantic search to pinpoint lines to edit.
* **Lazy Loading of Skills**: Do not load or read instructions for all global workspace skills at startup. Use `view_file` on a specific skill's `SKILL.md` ONLY when you are preparing to run a task that explicitly requires that skill. This minimizes context pollution and saves tokens.
* **Concise Communication**: Avoid conversational fluff. Keep responses dense, technical, and action-oriented.
* **File Exclusion**: Ignore build directories, logs, dependency folders, and node modules. Ensure `.agentsignore` or `.cursorignore` is respected.

## 5. QA Gates & Testing
* **Test Verification**: A developer agent cannot mark a user story or task as "done".
* **QA Handoff**: Completed features must be handed off to a QA/testing step (or dedicated QA agent) for verification. All test suites must pass successfully.

## 6. Activated Project-Specific Skills
The following specialized skills have been activated and recommended for this project:
${ACTIVATED_SKILLS}

## 7. Agile Iterative Loop Rules
All agents must adhere to the following 9-step Agile lifecycle:
1. **Vision Definition** (PO defines vision in `backlog.md`)
2. **Objectives Sourcing** (PO defines milestones in `backlog.md`)
3. **Epic & Feature Sourcing** (Architect defines Epics and intermediate deliverables/Features, mapping NFR requirements and Feature Acceptance Criteria in `backlog.md`)
4. **User Story Backlog** (PO writes functional acceptance criteria in `backlog.md` and links Stories to parent Features)
5. **Feature Development** (Developer writes code and colocates tests targeting the current Feature)
6. **Iterative Local Testing** (Developer tests/fixes locally - **MAX 5 loops**. Verify both functional criteria and NFR constraints. If tests still fail after 5 loops, stop and notify the human).
7. **Feature Branch Upload** (Developer commits code and pushes to a dedicated feature branch `feat/[feature-name]` to trigger GitHub Actions CI tests)
8. **GitHub Actions CI Verification** (QA monitors CI. If tests fail or NFR criteria are not met, developer returns to Step 5 to fix - **MAX 5 CI correction loops**. If still failing after 5 CI runs, stop and notify the human).
9. **Acceptance & Success** (PO reviews and signs off on User Stories and their parent Feature's acceptance criteria/NFRs in `backlog.md` before merging to the main branch).

<!-- START_CODE_MAP -->
<!-- This section will be automatically populated with the project codebase map -->
<!-- END_CODE_MAP -->

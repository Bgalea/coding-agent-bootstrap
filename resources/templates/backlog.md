# Project Backlog & Agile Workspace

> [!NOTE]
> **Modern Product Management Recommendation**:
> For active production projects, a monolithic text backlog (>800 lines) can introduce cognitive overload and agent context dilution (50,000+ words leading to missed acceptance criteria).
> We strongly recommend interconnecting your workspace with **Linear via Linear MCP**:
> - **Linear = The PILOT**: Dynamic Kanban, Epics, User Stories with Personas & Acceptance Criteria, ADR tickets, and NFRs.
> - **Git = The FACTORY**: Source code, commits, CI test pipelines.
> - **Natural Language Operation**: Instruct the agent with *"Take ticket PROJ-X"*, reading criteria directly via MCP without context saturation.
> 
> If Linear is not configured, this `backlog.md` serves as your local fallback backlog.

> [!IMPORTANT]
> **AI Rule**: When using this fallback backlog, all agents MUST follow the 9-step Agile lifecycle. You are strictly required to update this backlog's statuses at the end of every step and iteration.

---

## 1. Project Vision
*Define the high-level vision and the core value of the product to be built.*

- **Vision Statement**: [Enter Project Vision here]
- **Target Audience**: [Enter target audience / personas]

---

## 2. Key Objectives
*List the measurable objectives, milestones, and success criteria.*

- [ ] **Objective 1**: [Define KPI / Milestone 1]
- [ ] **Objective 2**: [Define KPI / Milestone 2]

---

## 3. Epics
*Group core features into high-level thematic Epics.*

| Epic ID | Title | Description | Status |
|---|---|---|---|
| EPIC-1 | Core Infrastructure & Guardrails | Initial setup, configuration, linting, architecture test suite, pre-commit hook. | [ ] Not Started |
| EPIC-2 | Core Domain Logic | Implementation of vertical slices for business logic. | [ ] Not Started |

---

## 4. Features & Non-Functional Requirements (NFR)
*Intermediate deliverables grouping User Stories, including NFRs and global Acceptance Criteria.*

| Feature ID | Parent Epic | Title & Scope | Non-Functional Requirements (NFR) | Feature Acceptance Criteria | Status |
|---|---|---|---|---|---|
| FEAT-1.1 | EPIC-1 | **Guardrails & CI Automation**: Configure code linting tools, architecture invariant tests, and pre-commit hook. | Response time: CI run < 2 min; Security: zero secrets leaked; Coverage: N/A. | 1. Pre-commit hooks block commits on code style or architecture test failure.<br>2. GitHub Actions runs successful verification on push. | [ ] Not Started |
| FEAT-2.1 | EPIC-2 | **User Auth Vertical Slice**: Implement user sign-up, sign-in, and token session validation. | Performance: auth check < 50ms; Security: token expiration < 1 hour; Coverage: > 85% test coverage. | 1. API responds to valid logins with JWT.<br>2. Unit tests colocated in `auth/` verify token security.<br>3. QA validates response latency is < 50ms. | [ ] Not Started |

---

## 5. User Stories Backlog
*Atomic User Stories pointing to their parent Feature, detailing functional acceptance criteria.*

| Story ID | Parent Feature | Title & Description | Dev Status | Local Tests (Max 5 Loops) | CI (Max 5 Loops) | Sign-off PO/QA |
|---|---|---|---|---|---|---|
| US-1.1.1 | FEAT-1.1 | **As a** developer, **I want to** initialize stack structure and architecture tests, **so that** invariants are automatically enforced. | [ ] Not Started | [ ] Pending | [ ] Pending | [ ] Pending |
| US-1.1.2 | FEAT-1.1 | **As a** developer, **I want to** setup pre-commit hooks, **so that** code style and architecture tests are checked locally before commit. | [ ] Not Started | [ ] Pending | [ ] Pending | [ ] Pending |
| US-2.1.1 | FEAT-2.1 | **As a** user, **I want to** sign up with email and password, **so that** I have a personal account. | [ ] Not Started | [ ] Pending | [ ] Pending | [ ] Pending |
| US-2.1.2 | FEAT-2.1 | **As a** user, **I want to** log in with my credentials, **so that** I get an active session JWT token. | [ ] Not Started | [ ] Pending | [ ] Pending | [ ] Pending |

---

## 6. Iteration & Sprint Planning
- [ ] **Sprint 1: Core Setup & Quality Gates (Target: FEAT-1.1)**
  - [ ] Initialize repository & system check
  - [ ] Set up pre-commit & CI pipelines with architecture guardrails
- [ ] **Sprint 2: Core Features & Acceptance (Target: FEAT-2.1)**
  - [ ] Implement vertical slices & tests
  - [ ] Perform final QA sign-off

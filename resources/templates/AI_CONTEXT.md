# AI Machine Context

> [!NOTE]
> This file is optimized for machine parsing. It provides dense architectural constraints, topology, and invariant rules.

## Operating Topology: The 3 Pillars

```
   ┌──────────────────────────────────────────────────────────────┐
   │                       LINEAR (The Pilot)                     │
   │  • Epics, User Stories (with Personas & Acceptance Criteria) │
   │  • Traceable ADRs (ADR-001..), Quantified NFRs, Bug RCA      │
   │  • Roadmap, Cycles & Priorities (Zero Split-Brain)           │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ "Take ticket PROJ-X" (via Linear MCP)
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                  AI AGENT (The Executor)                     │
   │  • Reads surgical ticket context without backlog bloating    │
   │  • Implements logic in Git repository (The Factory)          │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ Launches Quality Gate (make test / pre-commit)
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │         AUTOMATED ARCHITECTURE GUARDRAILS (Invariants)       │
   │  • architecture.test.* (Design tokens, anti-cliché, diet)    │
   │  • Physical Git Pre-Commit Hook (.git/hooks/pre-commit)      │
   │  ➜ IF AN INVARIANT BREAKS: THE COMMIT IS REJECTED (FAIL)     │
   └──────────────────────────────────────────────────────────────┘
```

## System Topology & Directory Structure
```
[root]
├── .agents/             # Multi-agent rules and workflow configurations
│   ├── AGENTS.md        # Core rules loaded by the AI
│   └── workflow.yml     # Multi-agent roles and routing configuration
├── .git/hooks/          # Pre-commit hook enforcing architectural tests
├── docs/                # System documentation
│   ├── backlog.md       # Product backlog (fallback when Linear is not used)
│   ├── AI_CONTEXT.md    # This file (Machine Context)
│   └── architecture.md  # Architectural design notes & ADR references
├── src/ (or [domain]/)  # Vertical slices of business domain (e.g., auth, billing)
│   ├── lib/             # Shared wrappers (e.g. storage.ts, architecture.test.ts)
│   ├── models.py/ts     # Data structures
│   ├── logic.py/ts      # Core business rules
│   └── tests/           # Feature-specific tests colocated
└── Makefile             # Task automation runner (RTK-accelerated)
```

## Core Business Domain Constraints
* Define domain entities clearly. 
* Business logic must reside in domain slices, not in outer frameworks or delivery layers.
* Interfaces between domains must be explicitly defined and use plain data-transfer objects (DTOs).

## Inviolable Architectural Invariants (Configurable)
* **Zero-Leak**: Zero hardcoded secrets, tokens, or credentials in codebase.
* **Anti-Cliché & Tone**: No generic AI visual tropes or decorative emoji clutter in user-facing UI labels.
* **Design System**: Strict adherence to project base components and approved color/theme tokens.
* **Ergonomics & Touch**: Button icon events must not intercept clicks (`pointer-events-none`); numeric figures must use tabular figures.
* **Encapsulation**: Domain modules must never bypass project wrappers for storage or global environment APIs.
* **Dependency Diet**: Prohibited from adding heavy unvetted third-party packages.

## Language & Coding Constraints
* **Typing**: Strict strong typing is mandatory. Hallucinations or type bypasses (`any` in TS, `Any` without justification in Python) are strictly prohibited.
* **Testing**: Minimum test coverage target is 80%. Every feature must include colocated tests and pass `architecture.test.*`.

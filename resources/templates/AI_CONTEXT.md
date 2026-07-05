# AI Machine Context

> [!NOTE]
> This file is optimized for machine parsing. It provides dense architectural constraints and business domain information.

## System Topology & Directory Structure
```
[root]
├── .agents/             # Multi-agent rules and workflow configurations
│   ├── AGENTS.md        # Core rules loaded by the AI
│   └── workflow.yml     # Multi-agent roles and routing configuration
├── docs/                # System documentation
│   ├── backlog.md       # Product backlog (User Stories)
│   ├── AI_CONTEXT.md    # This file (Machine Context)
│   └── architecture.md  # Architectural design notes
├── [domain]/            # Vertical slices of business domain (e.g., auth, billing)
│   ├── models.py/ts     # Data structures
│   ├── logic.py/ts      # Core business rules
│   └── tests/           # Feature-specific tests colocated
└── Makefile             # Task automation runner
```

## Core Business Domain Constraints
* Define domain entities clearly. 
* Business logic must reside in domain slices, not in outer frameworks or delivery layers.
* Interfaces between domains must be explicitly defined and use plain data-transfer objects (DTOs).

## Language & Coding Constraints
* **Typing**: Strict strong typing is mandatory. HALLUCINATIONS or type-safety bypasses (like Python `Any` without justification or TS `any`) are strictly prohibited.
* **Testing**: Minimum target test coverage is 80%. Every user story must be accompanied by integration or unit tests colocated within the feature slice.

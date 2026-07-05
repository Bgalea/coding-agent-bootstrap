---
name: coding-agent-bootstrap
description: Initializes a new software project by applying Antigravity best practices, generating a robust workspace structure (domain-driven), setting up Git, and configuring multi-agent workflows. Use this skill whenever the user starts a new project or asks to set up an AI coding workspace.
---

# Coding Agent Project Bootstrap Skill

You are an expert AI Architect and Project Manager. Your role is to bootstrap new software projects using the absolute best practices for autonomous AI coding assistants (like Antigravity, Claude, or Cursor).

When invoked, strictly follow these steps in order:

## Primary Setup Method: Automated Orchestration
You should run the unified bootstrap orchestrator script to automate safety checks, system diagnostics, interactive interview, configuration rendering, git initialization, and rule downloads in a single step.

The script will ask for your **Project Vision and Key Objectives** to dynamically detect and suggest activating specialized community skills (e.g. `web-design-engineer`, `modern-web-guidance`, `designing-python-apis`, `n8n-agents`, etc.) mapping them to specific agent roles in the workflow:

```bash
python3 <skill_dir>/scripts/bootstrap.py
```

This script will guide you through the process and generate all the configurations. If you cannot run the script or need to perform the steps manually, follow the fallback guide below.

---

## Fallback Setup Method: Manual Step-by-Step

### Step 1: Safety Check, System Diagnostic & Vision
1. **Safety Check (Non-destructive Bootstrap)**:
   - Check if the current workspace directory is empty or already contains files.
   - If the directory already contains code/files, warn the user, explain what files will be added/updated, and explicitly request confirmation before proceeding.
2. **System Diagnostics**:
   - Check for installed commands: `git`, `python3`, `node`, `make`. Inform the user of any missing tools.
3. **Interactive Interview**:
   - Ask the user for the project context, vision, key objectives, primary programming language, technology stack, and approved models for the Architect/PO role and Dev/QA role.
4. **Dynamic Community Rules & Skills Sourcing**:
   - Query GitHub dynamically for relevant rules (from `PatrickJS/awesome-cursorrules` for Cursor `.mdc` files) and agent skills (from `sickn33/antigravity-awesome-skills` for universal `SKILL.md` instructions) matching the stack name and keywords in the project vision.
   - Propose these rules/skills to the user.
   - For all approved rules/skills, download their raw file content from GitHub and write them to `.cursor/rules/` (for modular cursor rules) or `.agents/skills/{skill_name}/SKILL.md` (for agent skills).
   - Inject the paths of these downloaded files into `.agents/workflow.yml` and `.agents/AGENTS.md` (or `.cursorrules`).
   - If the script fails, perform a web search for community rules matching the stack and download them manually.

### Step 2: Git Initialization & Project Architecture
1. **Git Check**: Check if the current directory has a local Git repository. If not:
   - Run `git init`.
   - Copy the appropriate `.gitignore` template from `<skill_dir>/resources/templates/gitignore/` (e.g., `python.gitignore` or `node.gitignore`) to `.gitignore`.
2. **Security & Secrets Management (Anti-Leak)**:
   - Generate a blank `.env.example` file.
   - Add a strict rule to `AGENTS.md` explicitly FORBIDDING the agent from ever hardcoding real API keys or passwords in the source code.
3. **Domain-Driven Architecture (Vertical Slices)**: 
   - Create a folder structure organized by **Business Domain** (e.g., `auth/`, `billing/`, `core/`), NOT by technical layer.
   - Colocate tests, styles, and logic within feature folders.

### Step 3: Antigravity Standards & Multi-Agent Generation
Generate the following files to enforce AI standards:

1. **`docs/backlog.md`**: Copy the backlog template from `<skill_dir>/resources/templates/backlog.md` and customize it with the initial epics and tasks defined with the user.
2. **The "Dual README" Principle**: 
   - Create a standard `README.md` at the root designed exclusively for humans (tutorials, badges, setup).
   - Copy the machine-optimized context template from `<skill_dir>/resources/templates/AI_CONTEXT.md` to `docs/AI_CONTEXT.md` containing dense, compressed architectural context specifically formatted for machine parsing.
3. **`docs/architecture.md` & `docs/specifications.md`**: Create empty templates.
4. **CI/CD & Pre-commit Hooks**: 
   - Copy `.pre-commit-config.yaml` from `<skill_dir>/resources/templates/linters/` to the project root.
   - Copy `ruff.toml` (for Python) or `eslint.config.js` (for JS/TS) to the project root.
5. **`Makefile`**: Create a standard task runner.
6. **`.agents/AGENTS.md`**: 
   - Copy the baseline rules template from `<skill_dir>/resources/templates/AGENTS.md` to `.agents/AGENTS.md`. Customize any project boundaries as needed.
7. **Universal Rule Compatibility**:
   - Automatically copy `.agents/AGENTS.md` to `CLAUDE.md` at the project root.
8. **`.agents/workflow.yml` (Multi-Agent Structure)**:
   - Copy the workflow template from `<skill_dir>/resources/templates/workflow.yml` to `.agents/workflow.yml`.
   - Update `SOTA_FRONTIER_MODEL` and `FAST_CONTEXT_MODEL` placeholders in the workflow with the approved models.

### Step 4: Codebase Indexing (Memory)
1. **Native IDE Indexing (Default)**: Rely on the native codebase indexing of the AI assistant (Cursor, Antigravity, etc.).
2. **Advanced RAG / Custom Indexing (Optional)**: If accepted, add an `update-memory` command to the task runner to execute custom local vector database indexing scripts.

End your task by presenting a summary of the bootstrapped workspace to the user.


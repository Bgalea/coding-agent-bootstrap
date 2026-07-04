# Coding Agent Bootstrap Skill

This repository contains a **Skill** for autonomous AI coding assistants (like Google Antigravity, Claude, or Cursor). 

The `coding-agent-bootstrap` skill automates the setup of a new software project by applying industry best practices for AI agents. It initializes the workspace, sets up Git, establishes a domain-driven folder structure, and provisions a multi-agent workflow (PO, Architect, Developer, QA) with strict rules (like the "No Vibecoding" rule and strong typing requirements).

## Features

- **Interactive Setup**: Prompts you for the project context, stack, and MCP requirements.
- **Dynamic Rules Sourcing**: Scrapes community repositories (like `awesome-cursorrules` and `cursor.directory`) in real-time to fetch the absolute best AI prompts for your specific stack.
- **Security First**: Generates `.env.example` and explicitly blocks the AI from leaking real secrets into the codebase.
- **Vertical Slices Architecture**: Organizes your codebase by business domain instead of technical layers, drastically improving LLM context locality.
- **Universal AI Standards**: Generates `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `task.md`, and an agile `backlog.md`.
- **Dual README Principle**: Generates a standard `README.md` for humans and a compressed `AI_CONTEXT.md` for machines, saving tokens.
- **Token & Context Optimization**: Enforces the creation of `.cursorignore` / `.agentsignore` and instructs the AI to use minimal context and semantic search to avoid wasting tokens on large files.
- **Built-in CI/CD**: Automatically configures pre-commit hooks or GitHub Actions to ensure AI-generated code is always linted and formatted before commits.
- **Multi-Agent Orchestration**: Automatically templates a `workflow.yml` that delegates tasks to specialized sub-agents.
- **Explicit Model Routing**: Instructs the agent to explicitly ask the user which LLM models they have access to for each role (Architect, Developer, PO, QA) before generating the workflow, preventing any hallucination of unavailable models.
- **QA Gate Rule**: Prevents the developer agent from closing tasks without explicit review and testing by a QA agent.
- **Local Indexing Ready**: Prepares a `Makefile` to quickly index the workspace into a local Qdrant vector database.

## Usage & Installation

### 1. For Google Antigravity
Clone this repository into your global skills directory:
```bash
git clone https://github.com/Bgalea/coding-agent-bootstrap.git ~/.gemini/config/skills/coding-agent-bootstrap
```
Once installed, simply ask your agent:
> *"Je veux démarrer un nouveau projet Python. Utilise le skill coding-agent-bootstrap."*

### 2. For Claude (Anthropic)
To use this as a bootstrap prompt in Claude, the best method is to use **Claude Projects**:
1. Open Claude and go to **Projects** (left sidebar) -> **Create Project**.
2. Name your project (e.g., "Bootstrap [MyStack]").
3. Click on **Set project instructions**.
4. Copy and paste the entire contents of `SKILL.md` into the instructions box.
5. Save. You can now prompt Claude inside this project: *"Execute the project bootstrap process for a new [Language/Framework] project."*

### 3. For Cursor Editor
To use this in Cursor, you can configure it globally or per-project:
- **Global Rules (Applies everywhere)**: Open Cursor Settings (`Cmd + Shift + P` -> "Cursor Settings"). Go to **Rules > User Rules**. Paste the contents of `SKILL.md` here.
- **Project Rules (Specific project)**: Create a `.cursorrules` file in the root of an empty directory, or create a `.cursor/rules/bootstrap.mdc` file, and paste the `SKILL.md` content into it.

Once configured, hit `Cmd + I` (Composer) or `Cmd + L` (Chat) and ask Cursor to bootstrap the project.

## Requirements
- An autonomous AI assistant (Google Antigravity, Claude, Cursor, etc.).
- `gh` CLI (optional, if you want the agent to automatically create private GitHub repos).

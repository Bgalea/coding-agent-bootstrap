# Coding Agent Bootstrap Skill

This repository contains a **Skill** for autonomous AI coding assistants (like Google Antigravity, Claude, or Cursor). 

The `coding-agent-bootstrap` skill automates the setup of a new software project by applying industry best practices for AI agents. It initializes the workspace, sets up Git, establishes a domain-driven folder structure, and provisions a multi-agent workflow (PO, Architect, Developer, QA) with strict rules (like the "No Vibecoding" rule and strong typing requirements).

## Features

- **Interactive Setup**: Prompts you for the project context, stack, and MCP requirements.
- **Dynamic Rules Sourcing**: Scrapes community repositories (like `awesome-cursorrules` and `cursor.directory`) in real-time to fetch the absolute best AI prompts for your specific stack.
- **Vertical Slices Architecture**: Organizes your codebase by business domain instead of technical layers, drastically improving LLM context locality.
- **Antigravity Standards**: Generates `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `task.md`, and an agile `backlog.md`.
- **Multi-Agent Orchestration**: Automatically templates a `workflow.yml` that delegates tasks to specialized sub-agents.
- **Local Indexing Ready**: Prepares a `Makefile` to quickly index the workspace into a local Qdrant vector database.

## Installation for Google Antigravity

To install this skill locally in your Antigravity environment, clone this repository into your skills directory:

```bash
git clone https://github.com/Bgalea/coding-agent-bootstrap.git ~/.gemini/config/skills/coding-agent-bootstrap
```

Once installed, simply ask your agent:
> *"Je veux démarrer un nouveau projet Python. Utilise le skill coding-agent-bootstrap."*

## Requirements
- Google Antigravity (or compatible AI assistant).
- `gh` CLI (optional, if you want to automatically create private GitHub repos).

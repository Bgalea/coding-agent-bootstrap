# Coding Agent Bootstrap Skill

This repository contains a **Skill** for autonomous AI coding assistants (like Google Antigravity, Claude, or Cursor). 

The `coding-agent-bootstrap` skill automates the setup of a new software project by applying industry best practices for AI agents. It initializes the workspace, sets up Git, establishes a domain-driven folder structure, and provisions a multi-agent workflow (PO, Architect, Developer, QA) with strict rules (like the "No Vibecoding" rule and strong typing requirements).

## Features

- **Interactive Setup**: Prompts you for the project context, stack, and MCP requirements.
- **Dynamic Rules Sourcing**: Scrapes community repositories (like `awesome-cursorrules` and `cursor.directory`) in real-time to fetch the absolute best AI prompts for your specific stack.
- **Vertical Slices Architecture**: Organizes your codebase by business domain instead of technical layers, drastically improving LLM context locality.
- **Universal AI Standards**: Generates `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `task.md`, and an agile `backlog.md`.
- **Multi-Agent Orchestration**: Automatically templates a `workflow.yml` that delegates tasks to specialized sub-agents.
- **Local Indexing Ready**: Prepares a `Makefile` to quickly index the workspace into a local Qdrant vector database.

## Usage & Installation

### 1. For Google Antigravity
Clone this repository into your global skills directory:
```bash
git clone https://github.com/Bgalea/coding-agent-bootstrap.git ~/.gemini/config/skills/coding-agent-bootstrap
```
Once installed, simply ask your agent:
> *"Je veux démarrer un nouveau projet Python. Utilise le skill coding-agent-bootstrap."*

### 2. For Claude (Anthropic), Cursor, or Other Agents
You can inject the core instructions directly into your agent's context. 
Provide the `SKILL.md` file as a system prompt, custom instruction, or project knowledge. 

For example, simply prompt your AI with:
> *"Read the instructions in `SKILL.md` and execute the project bootstrap process for a new [Language/Framework] project."*

## Requirements
- An autonomous AI assistant (Google Antigravity, Claude, Cursor, etc.).
- `gh` CLI (optional, if you want the agent to automatically create private GitHub repos).

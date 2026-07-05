#!/usr/bin/env python3
import os
import sys
import json
import shutil
import subprocess
import urllib.request
import urllib.error
import urllib.parse

# Define the root of the bootstrap skill
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_command(cmd):
    """Check if a shell command exists."""
    return shutil.which(cmd) is not None

def run_diagnostics():
    """Check system requirements and print status."""
    print("==================================================")
    print("      BOOTSTRAP PRE-FLIGHT SYSTEM CHECK           ")
    print("==================================================")
    
    requirements = {
        "git": {"req": True, "desc": "Version control system"},
        "gh": {"req": False, "desc": "GitHub CLI (Optional, to link repositories)"},
        "python3": {"req": True, "desc": "Python runtime (Required for agent scripts)"},
        "node": {"req": False, "desc": "Node.js runtime (Optional, for JS/TS stack)"},
        "make": {"req": False, "desc": "Make build runner (Optional, for tasks)"},
        "docker": {"req": False, "desc": "Docker runtime (Optional, for containers)"}
    }
    
    missing_required = []
    
    for cmd, info in requirements.items():
        exists = check_command(cmd)
        status = "✔ Installed" if exists else ("✘ Missing" if info["req"] else "⚠ Missing (Optional)")
        print(f"  {cmd:<10} : {status:<22} | {info['desc']}")
        if not exists and info["req"]:
            missing_required.append(cmd)
            
    print("==================================================")
    if missing_required:
        print(f"CRITICAL: Missing required system tools: {', '.join(missing_required)}")
        print("Please install them before running the bootstrap process.")
        sys.exit(1)
    else:
        print("System diagnostics check passed successfully.")
    print("")

def check_safety():
    """Verify if the destination folder is empty."""
    current_files = [f for f in os.listdir(".") if not f.startswith('.')]
    if current_files:
        print("WARNING: The current directory is NOT empty.")
        print("Existing files found:")
        for f in current_files[:5]:
            print(f"  - {f}")
        if len(current_files) > 5:
            print(f"  - and {len(current_files) - 5} more...")
        
        confirm = input("\nDo you want to proceed? Existing configurations might be overwritten. (y/N): ")
        if confirm.lower() != 'y':
            print("Bootstrap cancelled by user.")
            sys.exit(0)
    print("")

def search_github_skills(stack, vision, editor):
    """Dynamically query community GitHub repositories for matching rules/skills."""
    print("Searching GitHub repositories dynamically for relevant skills/rules...")
    results = []
    headers = {"User-Agent": "Antigravity-Bootstrap-Agent"}
    
    # Extract vision keywords of length > 3
    query_words = [stack] + [w.strip(".,!?\"'") for w in vision.split() if len(w) > 3]
    
    # Source 1: Antigravity Awesome Skills (Universal agent skills)
    url_skills = "https://api.github.com/repos/sickn33/antigravity-awesome-skills/contents/skills"
    try:
        req = urllib.request.Request(url_skills, headers=headers)
        with urllib.request.urlopen(req) as res:
            if res.status == 200:
                data = json.loads(res.read().decode('utf-8'))
                for item in data:
                    name = item.get("name", "")
                    if item.get("type") == "dir":
                        # Match if any keyword matches the folder name
                        if any(kw.lower() in name.lower() for kw in query_words):
                            # Guess target role based on name heuristics
                            role = "developer"
                            if any(x in name.lower() for x in ["test", "audit", "security", "qa"]):
                                role = "qa_tester"
                            elif any(x in name.lower() for x in ["design", "api", "architecture", "structure"]):
                                role = "architect"
                            elif any(x in name.lower() for x in ["pm", "product", "backlog", "spec"]):
                                role = "product_owner"
                                
                            results.append({
                                "name": name,
                                "type": "skill",
                                "source": "sickn33/antigravity-awesome-skills",
                                "raw_url": f"https://raw.githubusercontent.com/sickn33/antigravity-awesome-skills/main/skills/{name}/SKILL.md",
                                "target_role": role,
                                "description": f"Community agent skill for {name}"
                            })
    except Exception as e:
        print(f"Skipped search on awesome-skills: {e}")

    # Source 2: Awesome Cursorrules (Cursor specific rules)
    # Also query this if editor is Cursor or user wants Cursor compatibility rules
    if editor == "cursor":
        url_rules = "https://api.github.com/repos/PatrickJS/awesome-cursorrules/contents/rules"
        try:
            req = urllib.request.Request(url_rules, headers=headers)
            with urllib.request.urlopen(req) as res:
                if res.status == 200:
                    data = json.loads(res.read().decode('utf-8'))
                    for item in data:
                        name = item.get("name", "")
                        if item.get("type") == "file" and name.endswith(".mdc"):
                            if any(kw.lower() in name.lower() for kw in query_words):
                                results.append({
                                    "name": name,
                                    "type": "rule",
                                    "source": "PatrickJS/awesome-cursorrules",
                                    "raw_url": f"https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/{name}",
                                    "target_role": "developer",
                                    "description": f"Cursor modular rule (.mdc) for {name[:-4]}"
                                })
        except Exception as e:
            print(f"Skipped search on awesome-cursorrules: {e}")

    # Sort results (exact stack match first, then shorter names)
    def rank_result(item):
        name_lower = item["name"].lower()
        exact_match = (name_lower == f"{stack}.mdc" or name_lower == stack)
        starts_with = name_lower.startswith(stack)
        return (not exact_match, not starts_with, len(item["name"]), item["name"])

    results.sort(key=rank_result)
    return results

def download_file(url):
    """Download raw text content from a URL."""
    headers = {"User-Agent": "Antigravity-Bootstrap-Agent"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as res:
            if res.status == 200:
                return res.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading file {url}: {e}")
    return None

def run_interview():
    """Collect project details and vision from the user."""
    print("==================================================")
    print("          INTERACTIVE PROJECT SETUP               ")
    print("==================================================")
    
    project_name = input("Project Name (default: my-awesome-project): ").strip()
    if not project_name:
        project_name = "my-awesome-project"
        
    stack = input("Technology Stack (python, node, typescript, go, rust) (default: python): ").strip().lower()
    if not stack:
        stack = "python"
        
    editor = input("Primary AI Editor/Assistant (antigravity, cursor, claude-code, codex) (default: antigravity): ").strip().lower()
    if not editor:
        editor = "antigravity"
        
    sota_model = input("SOTA Frontier Model (PO/Architect) (default: Claude 3.5 Sonnet): ").strip()
    if not sota_model:
        sota_model = "Claude 3.5 Sonnet"
        
    fast_model = input("Fast Context Model (Dev/QA) (default: Gemini 3.5 Flash): ").strip()
    if not fast_model:
        fast_model = "Gemini 3.5 Flash"
        
    print("\nProject Vision & Scope:")
    vision = input("Enter the vision, objectives, or keywords for the project: ").strip().lower()
    
    # Query GitHub dynamically based on vision and editor selection
    recommended_skills = search_github_skills(stack, vision, editor)
    
    activated_skills = []
    if recommended_skills:
        print("\nRecommended Community Skills/Rules discovered dynamically on GitHub:")
        for idx, skill in enumerate(recommended_skills, 1):
            print(f"  [{idx}] {skill['name']} ({skill['description']}) [Source: {skill['source']}]")
            
        print("\nWe will download and activate these skills in your local project workspace.")
        confirm = input("Do you want to activate all recommended skills? (Y/n): ").strip().lower()
        if confirm != 'n':
            activated_skills = recommended_skills
        else:
            selection = input("Enter indices of skills to activate (comma-separated, e.g. 1,3) or press Enter to skip: ").strip()
            if selection:
                try:
                    indices = [int(i.strip()) - 1 for i in selection.split(",")]
                    activated_skills = [recommended_skills[i] for i in indices if 0 <= i < len(recommended_skills)]
                except ValueError:
                    print("Invalid selection. No custom skills activated.")
                    
    return {
        "project_name": project_name,
        "stack": stack,
        "editor": editor,
        "sota_model": sota_model,
        "fast_model": fast_model,
        "vision": vision,
        "activated_skills": activated_skills
    }

def fetch_community_rules(stack, editor):
    """Download stack baseline rules using fetch_rules.py."""
    fetch_script = os.path.join(SKILL_DIR, "scripts", "fetch_rules.py")
    if os.path.exists(fetch_script):
        print(f"\nFetching community rules for stack: '{stack}'...")
        try:
            subprocess.run(["python3", fetch_script, stack], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch community rules: {e}")

def bootstrap_project(details):
    """Copy and render all templates, downloading and injecting matching skills."""
    print("\nBootstrapping files...")
    
    # Create main directory structure
    os.makedirs("docs", exist_ok=True)
    
    # 1. Setup .gitignore
    gitignore_src = os.path.join(SKILL_DIR, "resources", "templates", "gitignore", f"{details['stack']}.gitignore")
    if not os.path.exists(gitignore_src):
        gitignore_src = os.path.join(SKILL_DIR, "resources", "templates", "gitignore", "python.gitignore")
        
    if os.path.exists(gitignore_src):
        shutil.copy(gitignore_src, ".gitignore")
        print("  - Generated .gitignore")
        
    # 2. Setup blank .env.example
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write("# Environment Variables template\n# DO NOT COMMIT REAL SECRETS\nDATABASE_URL=sqlite:///app.db\nPORT=8080\n")
    print("  - Generated .env.example")
    
    # Download activated skills/rules and map them to roles
    po_skills = ["Agile backlog & user story management guidelines"]
    architect_skills = ["Software design patterns guidelines"]
    dev_skills = ["Code quality & vertical slice guidelines"]
    qa_skills = ["QA verification & test suite guidelines"]
    
    activated_list_md = []
    
    for skill in details["activated_skills"]:
        name = skill["name"]
        role = skill["target_role"]
        desc = skill["description"]
        raw_url = skill["raw_url"]
        
        # Download rules content
        content = download_file(raw_url)
        if content:
            if skill["type"] == "rule":
                # Save as modular rule in .cursor/rules/
                os.makedirs(".cursor/rules", exist_ok=True)
                dest = os.path.join(".cursor/rules", name)
                with open(dest, "w", encoding="utf-8") as f:
                    f.write(content)
                skill_ref = f"Guidelines from local rule `{dest}`"
                activated_list_md.append(f"* **{name}** : {desc} (Downloaded to: {dest})")
            else:
                # Save as agent skill in .agents/skills/
                dest_dir = os.path.join(".agents", "skills", name)
                os.makedirs(dest_dir, exist_ok=True)
                dest = os.path.join(dest_dir, "SKILL.md")
                with open(dest, "w", encoding="utf-8") as f:
                    f.write(content)
                skill_ref = f"Guidelines from local skill `{dest}`"
                activated_list_md.append(f"* **{name}** : {desc} (Downloaded to: {dest})")
                
            # Associate to role
            if role == "product_owner":
                po_skills.append(skill_ref)
            elif role == "architect":
                architect_skills.append(skill_ref)
            elif role == "developer":
                dev_skills.append(skill_ref)
            elif role == "qa_tester":
                qa_skills.append(skill_ref)
        else:
            print(f"Warning: Failed to download skill '{name}'")
            
    activated_skills_str = "\n".join(activated_list_md) if activated_list_md else "* None (No specialized skills activated)"
    
    # Variables mapping for rendering templates
    vars_mapping = {
        "PROJECT_NAME": details["project_name"],
        "SOTA_FRONTIER_MODEL": details["sota_model"],
        "FAST_CONTEXT_MODEL": details["fast_model"],
        "skill_dir": SKILL_DIR,
        "PO_SKILLS": ", ".join(po_skills),
        "ARCHITECT_SKILLS": ", ".join(architect_skills),
        "DEV_SKILLS": ", ".join(dev_skills),
        "QA_SKILLS": ", ".join(qa_skills),
        "ACTIVATED_SKILLS": activated_skills_str
    }
    
    # Helper to render templates safely
    def render_template(src_rel_path, dest_path):
        src_path = os.path.join(SKILL_DIR, "resources", "templates", src_rel_path)
        if os.path.exists(src_path):
            with open(src_path, "r", encoding="utf-8") as sf:
                content = sf.read()
            
            # Simple replacement logic
            for k, v in vars_mapping.items():
                content = content.replace(f"${{{k}}}", str(v))
                content = content.replace(f"${k}", str(v))
                
            os.makedirs(os.path.dirname(dest_path), exist_ok=True) if os.path.dirname(dest_path) else None
            with open(dest_path, "w", encoding="utf-8") as df:
                df.write(content)
            print(f"  - Generated {dest_path}")
            
    # 3. Render Backlog
    render_template("backlog.md", "docs/backlog.md")
    
    # 4. Render AI_CONTEXT
    render_template("AI_CONTEXT.md", "docs/AI_CONTEXT.md")
    
    # 5. Conditional generation based on selected editor
    editor = details["editor"]
    print(f"Configuring workspace rules targeting editor: '{editor}'")
    
    if editor == "antigravity":
        os.makedirs(".agents", exist_ok=True)
        render_template("AGENTS.md", ".agents/AGENTS.md")
        render_template("workflow.yml", ".agents/workflow.yml")
        render_template("AGENTS.md", "CLAUDE.md")
    elif editor == "cursor":
        render_template("AGENTS.md", ".cursorrules")
    elif editor == "claude-code":
        render_template("AGENTS.md", "CLAUDE.md")
    elif editor == "codex":
        render_template("AGENTS.md", ".codexrules")
    else:
        os.makedirs(".agents", exist_ok=True)
        render_template("AGENTS.md", ".agents/AGENTS.md")
        render_template("workflow.yml", ".agents/workflow.yml")
        render_template("AGENTS.md", "CLAUDE.md")
        
    # 6. Create empty architecture and specifications files
    with open("docs/architecture.md", "w", encoding="utf-8") as f:
        f.write("# Architecture Design Notes\n")
    with open("docs/specifications.md", "w", encoding="utf-8") as f:
        f.write("# Project Specifications\n")
    print("  - Generated docs/architecture.md & docs/specifications.md")
    
    # 7. Set up linters & pre-commit
    linter_templates = os.path.join(SKILL_DIR, "resources", "templates", "linters")
    if details["stack"] in ["python"]:
        shutil.copy(os.path.join(linter_templates, "ruff.toml"), "ruff.toml")
        shutil.copy(os.path.join(linter_templates, ".pre-commit-config.yaml"), ".pre-commit-config.yaml")
        print("  - Generated ruff.toml & .pre-commit-config.yaml (Python)")
    elif details["stack"] in ["node", "typescript", "javascript"]:
        shutil.copy(os.path.join(linter_templates, "eslint.config.js"), "eslint.config.js")
        shutil.copy(os.path.join(linter_templates, ".pre-commit-config.yaml"), ".pre-commit-config.yaml")
        print("  - Generated eslint.config.js & .pre-commit-config.yaml (Node/TS)")
    else:
        shutil.copy(os.path.join(linter_templates, ".pre-commit-config.yaml"), ".pre-commit-config.yaml")
        print("  - Generated .pre-commit-config.yaml (Generic)")
        
    # 8. Git Init
    if not os.path.exists(".git"):
        try:
            subprocess.run(["git", "init"], check=True, stdout=subprocess.DEVNULL)
            print("  - Initialized Git repository")
        except Exception as e:
            print(f"Warning: Failed to initialize Git repository: {e}")

def main():
    run_diagnostics()
    check_safety()
    details = run_interview()
    bootstrap_project(details)
    fetch_community_rules(details["stack"], details["editor"])
    
    print("\n==================================================")
    print("      PROJECT BOOTSTRAPPED SUCCESSFULLY!          ")
    print("==================================================")
    print(f"Project: {details['project_name']}")
    print(f"Stack: {details['stack']}")
    print(f"IDE Target: {details['editor']}")
    if details["activated_skills"]:
        print("Activated Skills/Rules:")
        for skill in details["activated_skills"]:
            print(f"  - {skill['name']} (from {skill['source']})")
    print("You are ready to code with your AI workspace rules!")
    print("==================================================")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error
import urllib.parse

# List of source repositories containing rules
SOURCES = [
    {
        "name": "PatrickJS/awesome-cursorrules",
        "api_url": "https://api.github.com/repos/PatrickJS/awesome-cursorrules/contents/rules",
        "raw_url_template": "https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/{file_name}"
    },
    {
        "name": "sparesparrow/cursor-rules",
        "api_url": "https://api.github.com/repos/sparesparrow/cursor-rules/contents",
        "raw_url_template": "https://raw.githubusercontent.com/sparesparrow/cursor-rules/main/{file_name}"
    }
]

def search_rules(stack_query):
    print(f"Searching community rules for: '{stack_query}' across multiple sources...")
    all_matches = []
    
    headers = {"User-Agent": "Antigravity-Bootstrap-Agent"}
    
    for source in SOURCES:
        req = urllib.request.Request(source["api_url"], headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    continue
                data = json.loads(response.read().decode('utf-8'))
                
                # Filter files matching query
                query_lower = stack_query.lower()
                for item in data:
                    name = item.get("name", "")
                    if item.get("type") == "file" and name.endswith(".mdc"):
                        if query_lower in name.lower():
                            all_matches.append({
                                "name": name,
                                "source": source["name"],
                                "raw_url": source["raw_url_template"].format(file_name=name)
                            })
        except Exception as e:
            # Silently skip failing sources (like offline or API rate limits)
            print(f"Skipped search on {source['name']}: {e}")
            continue
            
    # Sort matches to find the most relevant one
    # 1. Exact match (e.g., "python.mdc" for "python")
    # 2. Starts with query (e.g., "python-django...")
    # 3. Shorter names first (more generic)
    def rank_match(match_item):
        name_lower = match_item["name"].lower()
        query_lower = stack_query.lower()
        exact_match = (name_lower == f"{query_lower}.mdc" or name_lower == query_lower)
        starts_with = name_lower.startswith(query_lower)
        return (not exact_match, not starts_with, len(match_item["name"]), match_item["name"])

    all_matches.sort(key=rank_match)
    return all_matches

def download_rule(url):
    print(f"Downloading rule from: {url}")
    headers = {"User-Agent": "Antigravity-Bootstrap-Agent"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return response.read().decode('utf-8')
            else:
                print(f"Failed to download rule. Status: {response.status}")
    except Exception as e:
        print(f"Error downloading rule: {e}")
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_rules.py <stack_name>")
        sys.exit(1)
        
    stack_query = sys.argv[1]
    matches = search_rules(stack_query)
    
    if not matches:
        print(f"No rules found across sources for '{stack_query}'.")
        sys.exit(0)
        
    print(f"\nFound the following matching rule sets (sorted by relevance):")
    for idx, match in enumerate(matches, 1):
        print(f"  {idx}. {match['name']} (from {match['source']})")
        
    selected = matches[0]
    print(f"\nSelecting standard rule set: '{selected['name']}' from {selected['source']}")
    
    content = download_rule(selected['raw_url'])
    if content:
        os.makedirs(".cursor/rules", exist_ok=True)
        output_file = os.path.join(".cursor/rules", selected['name'])
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully saved rules to {output_file}")
    else:
        print("Failed to fetch rule content.")

if __name__ == "__main__":
    main()

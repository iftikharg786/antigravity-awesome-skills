
import os
import re
import json

CATEGORIES = {
    "security": ["security", "pentest", "attack", "exploit", "auth", "vulnerability", "hacking", "cyber", "xss", "sql-injection", "privilege", "reverse-engineer", "attacks"],
    "automation": ["automation", "automate", "workflow", "integration", "tool-builder", "action", "mcp", "orchestrate"],
    "cloud": ["aws", "azure", "gcp", "cloud", "supabase", "vercel", "host", "compute", "serverless", "infrastructure"],
    "frontend": ["react", "angular", "vue", "frontend", "web", "css", "tailwind", "ui", "ux", "browser", "extension"],
    "backend": ["api", "backend", "nodejs", "python", "fastapi", "django", "laravel", "ruby", "go-", "server-", "backend-patterns"],
    "data": ["data", "database", "analytics", "spreadsheet", "csv", "sql", "excel", "google-sheets", "airtable", "postgres", "cosmos", "mysql"],
    "ai-ml": ["agent", "ai", "llm", "ml", "model", "prompt", "gpt", "claude", "gemini", "rag", "eval", "pydantic"],
    "devops": ["cicd", "docker", "k8s", "kubernetes", "deploy", "pipeline", "git", "github", "gitlab", "cicd-", "ci-"],
    "communication": ["email", "whatsapp", "slack", "discord", "telegram", "messenger", "sms", "communication", "gmail", "outlook"],
    "productivity": ["asana", "jira", "trello", "monday", "todoist", "notion", "productivity", "management", "confluence", "linear"],
    "content": ["markdown", "text", "audio", "video", "content", "writer", "generate", "summarize", "search", "scraper", "crawling"]
}

SKILLS_DIR = 'skills'

def get_category(skill_id, name, desc):
    text = f"{skill_id} {name} {desc}".lower()
    for cat, keywords in CATEGORIES.items():
        if any(kw in text for kw in keywords):
            return cat
    return "uncategorized"

def update_skill(skill_id, name, desc):
    skill_path = os.path.join(SKILLS_DIR, skill_id, 'SKILL.md')
    if not os.path.exists(skill_path):
        return False
    
    category = get_category(skill_id, name, desc)
    if category == "uncategorized":
        return False

    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if category already exists in frontmatter
    frontmatter_match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        return False

    frontmatter = frontmatter_match.group(1)
    if 'category:' in frontmatter:
        return False # Skip if already categorized

    # Prepend category
    new_frontmatter = f"category: {category}\n" + frontmatter
    new_content = content.replace(frontmatter, new_frontmatter, 1)

    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    if not os.path.exists('uncategorized_list.json'):
        print("uncategorized_list.json not found")
        return

    with open('uncategorized_list.json', 'r', encoding='utf-8') as f:
        skills = json.load(f)

    updated_count = 0
    for skill in skills:
        if update_skill(skill['id'], skill['name'], skill['desc']):
            updated_count += 1
            print(f"Updated {skill['id']}")

    print(f"Finished. Total updated: {updated_count}")

if __name__ == "__main__":
    main()

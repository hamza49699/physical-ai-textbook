
import os
import re
import requests
import frontmatter

API_URL_INGEST = "http://localhost:8000/ingest"
API_URL_RESET = "http://localhost:8000/reset"
DOCS_DIR = "../docs"

def reset_database():
    try:
        response = requests.post(API_URL_RESET)
        if response.status_code == 200:
            print("Database reset successfully.")
        else:
            print(f"Failed to reset database: {response.text}")
    except Exception as e:
        print(f"Error resetting database: {e}")

def ingest_file(filepath):
    filename = os.path.basename(filepath)
    print(f"Processing {filename}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            post = frontmatter.load(f)
            content = post.content
        except Exception as e:
            print(f"Error parsing frontmatter for {filename}: {e}")
            return
            
    # Determine chapter/module from filename
    chapter = 0
    match = re.search(r'module-(\d+)', filename)
    if match:
        chapter = int(match.group(1))
    elif 'intro' in filename:
        chapter = 0
    else:
        chapter = 99 # Tutorial/Extra
        
    title = filename.replace('.md', '').replace('-', ' ').title()
    
    # Split content by H2 or H3 headers (## or ###)
    # This creates smaller chunks for better Bag-of-Words retrieval
    sections = re.split(r'\n#{2,3}\s+', content)
    
    # First part might be intro before first H2
    if sections[0].strip():
        payload = {
            "title": title,
            "chapter": chapter,
            "section": "Introduction",
            "content": sections[0].strip()[:2000] # Limit chunk size
        }
        send_ingest(payload)
        
    for i in range(1, len(sections)):
        lines = sections[i].strip().split('\n')
        header = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()
        
        if not body:
            continue
            
        payload = {
            "title": title,
            "chapter": chapter,
            "section": header,
            "content": body[:4000] # Qdrant/Embedding limit safety
        }
        send_ingest(payload)

def send_ingest(payload):
    try:
        response = requests.post(API_URL_INGEST, json=payload)
        if response.status_code == 200:
            print(f"Ingested: {payload['section'][:30]}...")
        else:
            print(f"Failed to ingest {payload['section'][:30]}... {response.text}")
    except Exception as e:
        print(f"Request error: {e}")

if __name__ == "__main__":
    if not os.path.exists(DOCS_DIR):
        # Maybe running from root
        DOCS_DIR = "docs"
    
    # Reset first
    reset_database()
        
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".md"):
            ingest_file(os.path.join(DOCS_DIR, filename))

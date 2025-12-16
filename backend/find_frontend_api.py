import sys
import os

# Find all frontend source files
print("Searching for frontend files...")
print("=" * 60)

# Search in common frontend directories
search_paths = [
    r"c:\Users\digital\claude_first\physical-ai-textbook\src",
    r"c:\Users\digital\claude_first\physical-ai-textbook",
]

keywords = ["localhost:8000", "8000", "fetch", "axios", "/query"]

for search_path in search_paths:
    if os.path.exists(search_path):
        print(f"\nSearching in: {search_path}")
        for root, dirs, files in os.walk(search_path):
            # Skip node_modules and build directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'build', '.git', '__pycache__']]
            
            for file in files:
                if file.endswith(('.tsx', '.ts', '.jsx', '.js', '..html')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            for keyword in keywords:
                                if keyword in content:
                                    print(f"\n✓ Found '{keyword}' in: {file_path}")
                                    break
                    except:
                        pass

print("\n" + "=" * 60)
print("Search complete!")

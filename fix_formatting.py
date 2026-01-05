import os
import re

def normalize_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Replace 3 underscores (___) with 3 dashes (---), ensuring blank lines around
    # The regex looks for:
    # (?m)^      : Start of line (multiline)
    # \s*        : Optional whitespace
    # _{3,}      : 3 or more underscores
    # \s*        : Optional whitespace
    # $          : End of line
    
    # We replace it with \n\n---\n\n to ensure standard markdown spacing
    # But we need to be careful not to introduce too many newlines if they already exist.
    # A safer, direct replacement for the user's specific case:
    
    # User Case:
    # Links: 
    # ___
    # # Title
    
    # pattern = r'(Links:\s*\n)_{4,}'
    # replacement = r'\1\n---'
    
    # General Case for Horizontal Rules:
    # Replace any line consisting of only 3+ or 4+ underscores with `---`
    content = re.sub(r'(?m)^\s*_{3,}\s*$', '---', content)
    
    # 2. Ensure blank lines around `---`
    content = re.sub(r'\n*^---\s*$\n*', '\n\n---\n\n', content, flags=re.MULTILINE)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
    else:
        print(f"No changes: {filepath}")
        pass

def main():
    target_dir = "Java" # Hardcoded for now as per context, or we can ask input
    
    if not os.path.exists(target_dir):
        print(f"Directory '{target_dir}' not found.")
        return

    print(f"Scanning '{target_dir}' for formatting issues...")
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                normalize_file(os.path.join(root, file))
                count += 1
                
    print("Done.")

if __name__ == "__main__":
    main()

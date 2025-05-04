import os
import sys
import re
from pathlib import Path
import string
from PIL import Image  # for images


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".gif"}

TEXT_EXTENSIONS = {
    ".html", ".htm", ".css", ".js", ".ts", ".jsx", ".tsx",
    ".json", ".xml", ".yml", ".yaml", ".py", ".java", ".c",
    ".cpp", ".php", ".rb", ".go", ".rs", ".sh", ".bat",
    ".ini", ".md", ".txt", ".vue",

    ".unity", ".prefab", ".mat", ".meta", ".anim", ".controller", ".meta", ".sln", ".csproj", ".asset", ".cs",

    ".csv", ".tsv", ".log", ".toml", ".cfg", ".env"
}

# yes my terminal looks nice
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def get_base_filename(name):
    return re.sub(r"_\d+(?=\.[^\.]+$)", "", name)

def is_image_valid(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception as e:
        print(f"  {RED}[!] Invalid image file: {file_path} - {e}{RESET}")
        return False

def analyze_folder(folder_path):
    image_deletions = []
    text_deletions = []
    renames = []

    print(f"\n{BOLD}{CYAN}🔍 Scanning files and analyzing...{RESET}")

    for file in Path(folder_path).rglob("*"):
        if file.is_file():

            # delete macos meta files
            if file.name.startswith("._"):
                try:
                    file.unlink()
                    print(f"{RED}🗑️  Deleted AppleDouble metadata file:{RESET} {file}")
                except Exception as e:
                    print(f"{RED}[!] Failed to delete {file}:{RESET} {e}")
                continue

            suffix = file.suffix.lower()

            # IMAGE FILES
            if suffix in IMAGE_EXTENSIONS:
                print(f"  - Checking image: {file.name}")
                if is_image_valid(file):
                    print(f"{GREEN}✅ Valid image file:{RESET} {file.name}")
                    base_name = get_base_filename(file.name)
                    new_name = file.parent / base_name
                    if (file.name != base_name and
                        (not new_name.exists() or new_name in image_deletions or new_name.resolve() == file.resolve())):
                        renames.append((file, new_name))
                else:
                    image_deletions.append(file)

            # TEXT FILES
            elif suffix in TEXT_EXTENSIONS:
                print(f"  - Checking text file: {file.name}")
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        head = f.read(2048)
                        if not head.strip():
                            raise Exception("Empty or unreadable file.")
                    print(f"{GREEN}✅ Valid text file:{RESET} {file.name}")
                    base_name = get_base_filename(file.name)
                    new_name = file.parent / base_name
                    if (file.name != base_name and
                        (not new_name.exists() or new_name in text_deletions or new_name.resolve() == file.resolve())):
                        renames.append((file, new_name))
                except Exception as e:
                    print(f"  {RED}[!] Invalid text file: {file} - {e}{RESET}")
                    text_deletions.append(file)

    print(f"\n{'='*60}")
    print(f"{YELLOW}🗑️  Image files marked for deletion (broken images):{RESET} {len(image_deletions)}")
    print(f"{YELLOW}🗑️  Text files marked for deletion (broken text):{RESET} {len(text_deletions)}")
    print(f"{YELLOW}✏️  Files to rename:{RESET} {len(renames)}")
    
    confirm = input(f"{BOLD}⚠️  Proceed with deletion and renaming? (Y/N): {RESET}").strip().lower()

    if confirm == 'y':
        for file in image_deletions + text_deletions:
            try:
                file.unlink()
                print(f"{RED}🗑️  Deleted:{RESET} {file}")
            except Exception as e:
                print(f"{RED}[!] Failed to delete {file}:{RESET} {e}")

        for src, dst in renames:
            try:
                src.rename(dst)
                print(f"{GREEN}✏️  Renamed:{RESET} {src.name} → {dst.name}")
            except Exception as e:
                print(f"{RED}[!] Failed to rename {src.name}:{RESET} {e}")
    else:
        print(f"{YELLOW}⚠️  Aborted. No files were changed.{RESET}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{RED}Usage: python analyze_files.py \"Path/To/Folder\"{RESET}")
        sys.exit(1)

    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"{RED}Invalid folder: {folder}{RESET}")
        sys.exit(1)

    print(f"{CYAN}📂 Analyzing folder:{RESET} {folder}")
    analyze_folder(folder)
    print(f"\n{GREEN}🎉 Done.{RESET}")
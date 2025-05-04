import os
import sys
import re
from pathlib import Path
import string

VALID_EXTENSIONS = {
    ".html", ".css", ".js", ".unity", ".prefab", ".meta",
}

def is_probably_corrupted(filepath):
    try:
        size = filepath.stat().st_size
        if size == 0:
            return True

        with open(filepath, 'rb') as f:
            head = f.read(2048)

        non_printable = sum(1 for b in head if chr(b) not in string.printable)

        ratio = non_printable / len(head) if head else 1

        return ratio > 0.8
    except Exception:
        return True

def get_base_filename(name):
    return re.sub(r"_\d+(?=\.[^\.]+$)", "", name)

def analyze_folder(folder_path):
    files_map = {}

    for file in Path(folder_path).rglob("*"):
        if file.is_file() and file.suffix.lower() in VALID_EXTENSIONS:
            base_name = get_base_filename(file.name)
            key = (file.parent, base_name)
            files_map.setdefault(key, []).append(file)

    for (parent, base_name), variants in files_map.items():
        print(f"\nAnalyzing group: {base_name}")
        best_candidate = None
        lowest_noise = 1.0

        for file in variants:
            size = file.stat().st_size

            try:
                with open(file, 'rb') as f:
                    head = f.read(2048)

                non_printable = sum(1 for b in head if chr(b) not in string.printable)
                ratio = non_printable / len(head) if head else 1
            except Exception as e:
                ratio = 1
                print(f"  [!] Failed to read {file.name}: {e}")
            else:
                print(f"  - {file.name} | size: {size} bytes | non-printable ratio: {ratio:.2f}")

            if size > 0 and ratio < lowest_noise:
                lowest_noise = ratio
                best_candidate = file

        if best_candidate:
            print(f"  => Most likely valid: {best_candidate.name}")
        else:
            print("  => No usable file found in this group.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_files.py \"Path/To/Folder\"")
        sys.exit(1)

    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"Invalid folder: {folder}")
        sys.exit(1)

    print(f"Analyzing folder: {folder}")
    analyze_folder(folder)
    print("\nDone.")

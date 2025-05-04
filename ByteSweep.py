import string

def is_corrupted(filepath):
    try:
        size = filepath.stat().st_size
        if size == 0:
            return True

        # Read first few bytes to test for noise
        with open(filepath, 'rb') as f:
            head = f.read(1024)

        # Check for high ratio of non-printable characters
        nontext_ratio = sum(1 for b in head if chr(b) not in string.printable) / len(head)
        if nontext_ratio > 0.8:
            return True  # Too much noise

        return False
    except Exception as e:
        print(f"⚠️ Error reading {filepath}: {e}")
        return True

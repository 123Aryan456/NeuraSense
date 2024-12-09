from hashlib import md5

class DuplicateCodeDetector:
    """Detects duplicate code blocks."""
    def __init__(self, code):
        self.code = code

    def detect_duplicates(self):
        lines = self.code.splitlines()
        line_hashes = {}
        duplicates = {}
        for i, line in enumerate(lines):
            line_content = line.strip()
            if not line_content:
                continue
            line_hash = md5(line_content.encode('utf-8')).hexdigest()
            if line_hash in line_hashes:
                duplicates.setdefault(line_content, []).extend([line_hashes[line_hash], i + 1])
            else:
                line_hashes[line_hash] = i + 1
        return duplicates
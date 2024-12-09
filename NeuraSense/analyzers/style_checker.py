import re

class StyleChecker:
    """Analyzes code style compliance (e.g., PEP 8 issues)."""
    def __init__(self, code, config):
        self.code = code
        self.config = config

    def check_pep8(self):
        issues = []
        max_line_length = self.config.get("max_line_length", 79)
        for i, line in enumerate(self.code.splitlines(), 1):
            if len(line) > max_line_length:
                issues.append(f"Line {i}: Line exceeds {max_line_length} characters.")
            if line.rstrip() != line:
                issues.append(f"Line {i}: Trailing whitespace detected.")
            if '\t' in line:
                issues.append(f"Line {i}: Tab character detected; use spaces instead.")
            if re.match(r'^\s*$', line) and i < len(self.code.splitlines()) and re.match(r'^\s*$', self.code.splitlines()[i]):
                issues.append(f"Line {i}: Multiple consecutive blank lines.")
        return issues
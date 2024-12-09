import re

class ReadabilityAnalyzer:
    """Analyzes code readability using NLP techniques."""
    def __init__(self, code):
        self.code = code

    def calculate_readability(self):
        words = self._extract_identifiers()
        total_words = len(words)
        complex_words = sum(1 for word in words if len(word) > 7)
        if total_words == 0:
            return 100.0
        score = 100 - (complex_words / total_words) * 100
        return round(score, 2)

    def _extract_identifiers(self):
        pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
        words = pattern.findall(self.code)
        python_keywords = set([
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
            'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
            'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
            'while', 'with', 'yield'
        ])
        words = [word for word in words if word not in python_keywords]
        return words
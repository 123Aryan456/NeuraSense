import ast

class InlineCommentChecker:
    """Analyzes inline comments."""
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)
        self.comment_lines = self._extract_comments()
        self.function_defs = self._extract_function_defs()

    def _extract_comments(self):
        comments = []
        tokens = ast.walk(self.tree)
        for node in tokens:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                comments.append((node.lineno, node.value.s))
        return comments

    def _extract_function_defs(self):
        function_defs = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                function_defs.append((node.lineno, node.name))
        return function_defs

    def check_comments(self):
        commented_functions = [line for line, _ in self.comment_lines]
        missing_comments = []
        for lineno, func_name in self.function_defs:
            if lineno - 1 not in commented_functions:
                missing_comments.append(f"Function '{func_name}' at line {lineno} is missing a docstring.")
        return self.comment_lines, missing_comments
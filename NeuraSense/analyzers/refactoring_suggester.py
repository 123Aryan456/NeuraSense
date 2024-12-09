import ast

class RefactoringSuggester(ast.NodeVisitor):
    """Suggests code refactoring opportunities."""
    def __init__(self, code, config):
        self.code = code
        self.config = config
        self.tree = ast.parse(code)
        self.suggestions = []
        self.visit(self.tree)

    def visit_FunctionDef(self, node):
        function_length = len(node.body)
        max_length = self.config.get("max_function_length", 50)
        if function_length > max_length:
            self.suggestions.append(f"Function '{node.name}' is too long ({function_length} lines). Consider refactoring.")
        nesting_depth = self._calculate_nested_depth(node)
        if nesting_depth > 3:
            self.suggestions.append(f"Function '{node.name}' has deep nesting ({nesting_depth} levels). Consider simplifying.")
        self.generic_visit(node)

    def _calculate_nested_depth(self, node, current_depth=0):
        max_depth = current_depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.FunctionDef, ast.Try)):
                depth = self._calculate_nested_depth(child, current_depth + 1)
                max_depth = max(max_depth, depth)
        return max_depth

    def get_suggestions(self):
        return self.suggestions
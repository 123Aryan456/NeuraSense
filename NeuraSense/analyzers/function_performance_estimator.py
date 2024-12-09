import ast

class FunctionPerformanceEstimator(ast.NodeVisitor):
    """Estimates time complexity of functions using AST analysis."""
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)
        self.function_complexities = {}
        self.current_function = None
        self.visit(self.tree)

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.loop_depth = 0
        self.max_loop_depth = 0
        self.recursive_calls = 0
        self.generic_visit(node)
        complexity = self._estimate_complexity()
        self.function_complexities[self.current_function] = complexity
        self.current_function = None

    def visit_For(self, node):
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.current_function:
            self.recursive_calls += 1
        self.generic_visit(node)

    def _estimate_complexity(self):
        if self.recursive_calls > 0:
            complexity = f"O({self.current_function}(n))"
        elif self.max_loop_depth > 0:
            complexity = f"O(n^{self.max_loop_depth})"
        else:
            complexity = "O(1)"
        return complexity

    def estimate_performance(self):
        return self.function_complexities
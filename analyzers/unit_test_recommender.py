import ast

class UnitTestRecommender(ast.NodeVisitor):
    """Recommends unit tests by identifying uncovered functions."""
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)
        self.function_defs = []
        self.test_functions = []
        self.visit(self.tree)

    def visit_FunctionDef(self, node):
        if node.name.startswith('test_'):
            self.test_functions.append(node.name[5:])
        else:
            self.function_defs.append(node.name)
        self.generic_visit(node)

    def recommend_tests(self):
        uncovered_functions = set(self.function_defs) - set(self.test_functions)
        recommendations = []
        for func in uncovered_functions:
            recommendations.append(f"Function '{func}' is not covered by unit tests.")
        return recommendations
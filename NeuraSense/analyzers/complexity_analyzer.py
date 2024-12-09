import ast
import math

class ComplexityAnalyzer(ast.NodeVisitor):
    """Analyzes Python code to calculate complexity metrics."""
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)
        self.metrics = {
            "lines_of_code": 0,
            "cyclomatic_complexity": 0,
            "maintainability_index": 0.0,
            "halstead_volume": 0.0,
            "nested_block_depth": 0,
        }
        self._analyze()

    def _analyze(self):
        self.metrics["lines_of_code"] = self.code.count('\n') + 1
        self.visit(self.tree)
        self.metrics["maintainability_index"] = self._calculate_maintainability_index()
        self.metrics["halstead_volume"] = self._calculate_halstead_volume()

    def visit_FunctionDef(self, node):
        self.metrics["cyclomatic_complexity"] += self._calculate_cyclomatic_complexity(node)
        self.metrics["nested_block_depth"] = max(self.metrics["nested_block_depth"], self._calculate_nested_depth(node))
        self.generic_visit(node)

    def _calculate_cyclomatic_complexity(self, node):
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler, ast.With, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _calculate_nested_depth(self, node, current_depth=0):
        max_depth = current_depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.FunctionDef)):
                depth = self._calculate_nested_depth(child, current_depth + 1)
                max_depth = max(max_depth, depth)
        return max_depth

    def _calculate_maintainability_index(self):
        loc = self.metrics["lines_of_code"]
        cc = self.metrics["cyclomatic_complexity"]
        hv = self.metrics["halstead_volume"]
        mi = max(0, (171 - 5.2 * math.log(hv + 1) - 0.23 * cc - 16.2 * math.log(loc + 1)) * 100 / 171)
        return mi

    def _calculate_halstead_volume(self):
        operators = set()
        operands = set()
        operator_count = 0
        operand_count = 0

        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
                                  ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
                                  ast.FloorDiv)):
                operators.add(type(node).__name__)
                operator_count += 1
            elif isinstance(node, (ast.Num, ast.Str, ast.Bytes, ast.NameConstant)):
                operands.add(node.n)
                operand_count += 1
            elif isinstance(node, ast.Name):
                operands.add(node.id)
                operand_count += 1

        n1 = len(operators)
        n2 = len(operands)
        N1 = operator_count
        N2 = operand_count
        vocabulary = n1 + n2
        length = N1 + N2
        if vocabulary == 0 or length == 0:
            volume = 0
        else:
            volume = length * math.log(vocabulary, 2)
        return volume

    def get_metrics(self):
        return self.metrics
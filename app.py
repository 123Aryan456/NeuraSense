from flask import Flask, render_template, request
import os

from analyzers.complexity_analyzer import ComplexityAnalyzer
from analyzers.style_checker import StyleChecker
from analyzers.duplicate_code_detector import DuplicateCodeDetector
from analyzers.dependency_vulnerability_checker import DependencyVulnerabilityChecker
from analyzers.function_performance_estimator import FunctionPerformanceEstimator
from analyzers.inline_comment_checker import InlineCommentChecker
from analyzers.readability_analyzer import ReadabilityAnalyzer
from analyzers.refactoring_suggester import RefactoringSuggester
from analyzers.unit_test_recommender import UnitTestRecommender

app = Flask(__name__)

def analyze_code(code_str, config):
    # Run complexity analysis
    complexity_analyzer = ComplexityAnalyzer(code_str)
    complexity_metrics = complexity_analyzer.get_metrics()

    # Style issues
    style_checker = StyleChecker(code_str, config.get("style", {}))
    style_issues = style_checker.check_pep8()

    # Duplicate code detection
    duplicate_detector = DuplicateCodeDetector(code_str)
    duplicates = duplicate_detector.detect_duplicates()

    # Vulnerability checks
    project_dir = os.getcwd()
    vulnerability_checker = DependencyVulnerabilityChecker(project_dir, config.get("vulnerability", {}))
    vulnerabilities = vulnerability_checker.check_vulnerabilities()

    # Performance estimation
    performance_estimator = FunctionPerformanceEstimator(code_str)
    performance_metrics = performance_estimator.estimate_performance()

    # Inline comments
    comment_checker = InlineCommentChecker(code_str)
    comments_found, missing_comments = comment_checker.check_comments()
    comment_metrics = {
        "comments_found": comments_found,
        "missing_comments": missing_comments
    }

    # Readability score
    readability_analyzer = ReadabilityAnalyzer(code_str)
    readability_score = readability_analyzer.calculate_readability()

    # Refactoring suggestions
    refactoring_suggester = RefactoringSuggester(code_str, config.get("refactoring", {}))
    refactoring_suggestions = refactoring_suggester.get_suggestions()

    # Unit test recommendations
    unit_test_recommender = UnitTestRecommender(code_str)
    test_recommendations = unit_test_recommender.recommend_tests()

    return {
        "complexity_metrics": complexity_metrics,
        "style_issues": style_issues,
        "duplicates": duplicates,
        "vulnerabilities": vulnerabilities,
        "performance_metrics": performance_metrics,
        "comment_metrics": comment_metrics,
        "readability_score": readability_score,
        "refactoring_suggestions": refactoring_suggestions,
        "test_recommendations": test_recommendations
    }

@app.route('/', methods=['GET'])
def index():
    # Render the home page (index.html) with an optional error message
    # if code submission was invalid previously.
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Configuration for the analyzers
    config = {
        "style": {"max_line_length": 79},
        "complexity": {"max_cyclomatic_complexity": 10},
        "readability": {"min_score": 60},
        "vulnerability": {"sources": ["OSV"]},
        "refactoring": {"max_function_length": 50},
    }

    code_str = request.form.get('code_input', '')
    uploaded_file = request.files.get('code_file')

    # If a file was uploaded and has a filename, read code from it.
    if uploaded_file and uploaded_file.filename.strip():
        code_str = uploaded_file.read().decode('utf-8')

    # If no code is provided (empty textarea and no file), return to index with error
    if not code_str.strip():
        return render_template('index.html', error="Please provide code to analyze.")

    # Run analysis
    results = analyze_code(code_str, config)

    # Render results page with the analysis outcome
    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
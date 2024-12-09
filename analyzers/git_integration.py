

class GitIntegration:
    """Provides Git-specific analysis and recommendations."""
    def __init__(self, project_dir, repo):
        self.project_dir = project_dir
        self.repo = repo

    def compare_versions(self, file_path):
        try:
            diffs = self.repo.git.diff('HEAD~1', 'HEAD', file_path)
            return diffs
        except Exception as e:
            return f"Error comparing versions: {e}"
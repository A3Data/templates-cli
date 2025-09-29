import json
import subprocess
from .abs import TemplateConfig, TemplateClass
import os


def ensure_dir(path: str) -> None:
    """Ensure a directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)

class GithubRepositoryTemplate(TemplateClass):
    def __init__(self, config: TemplateConfig):
        super().__init__(config)

    def build(self, output_dir: str) -> None:
        """Build the github repository template"""
        try:
            ensure_dir(output_dir)
            repo_url = f"https://github.com/{self.config.organization}/{self.config.repository}.git"
            branch = self.config.branch or "master"
            result =  subprocess.run(
                ["git", "clone", repo_url,"--branch", branch],
                check=True,
                cwd=os.path.abspath(output_dir)
            )
            
        except Exception as e:
            raise RuntimeError(f"Failed to build template: {str(e)}")
    
    def is_available(self):
        return True

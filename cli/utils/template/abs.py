import requests
import yaml
import os
import typer
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TemplateConfig:
    """Configuration for a template"""
    name: str
    description: str
    type: str  # 'nix' or 'cookiecutter'
    organization: str
    repository: str
    branch: str = "main"
    configPath: str = "config.yaml"


def token_github() -> str:
    gh_config_path = os.path.expanduser("~/.config/gh/hosts.yml")

    if not os.path.exists(gh_config_path):
        raise typer.BadParameter("Execute `gh auth login` primeiro.")

    with open(gh_config_path, "r") as file:
        config = yaml.safe_load(file)

    github_info = config.get("github.com")
    if not github_info or "oauth_token" not in github_info:
        raise typer.BadParameter("Token OAuth não encontrado.")
    return github_info["oauth_token"]


class TemplateClass(ABC):
    """Abstract base class for templates"""

    def __init__(self, config: TemplateConfig):
        self.config = config

    def __str__(self) -> str:
        """Pretty print representation of the template"""
        return f"""{self.config.name} - {self.config.description} <https://github.com/{self.config.organization}/{self.config.repository}>"""

    def _fetch_github_file(self, path: str) -> str:
        """Helper method to fetch files from GitHub"""
        url = f"https://api.github.com/repos/{self.config.organization}/{self.config.repository}/contents/{path}?ref={self.config.branch}"
        headers = {
            "Authorization": f"Bearer {token_github()}",
            "Accept": "application/vnd.github.v3.raw",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        if not response.text:
            raise ValueError(f"Failed to fetch file from {url}")
        return response.text

    def get_template_options(self) -> Dict[str, Any]:
        """
        Fetch template options from the repository
        Returns: Tuple of (options_dict, error_message)
        """
        file_content = self._fetch_github_file(self.config.configPath)
        if not file_content:
            raise ValueError("Failed to fetch template options")
        
        return yaml.safe_load(file_content)

    @abstractmethod
    def encode_input(self, collected_data: dict) -> str:
        """Encodes the collected data into a format suitable for the template engine"""
        pass

    # @abstractmethod
    # def display_summary(self, collected_data: Dict[str, Any]) -> bool:
    #     """Display a summary of the collected data"""
    #     pass

    @abstractmethod
    def build(self, config: str, output_dir: str) -> None:
        """Build the template and create it in the specified directory"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the template is available"""
        pass

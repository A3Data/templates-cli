import requests
import yaml
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TemplateConfig:
    """Configuration for a template"""
    name: str
    description: str
    type: str
    organization: str
    repository: str
    branch: str = "main"
    configPath: str = "config.yaml"


class GitHubAuthError(Exception):
    """Custom exception for GitHub authentication errors"""
    pass


def token_github() -> str:
    gh_config_path = os.path.expanduser("~/.config/gh/hosts.yml")

    if not os.path.exists(gh_config_path):
        raise GitHubAuthError("Execute `gh auth login` primeiro.")

    with open(gh_config_path, "r") as file:
        config = yaml.safe_load(file)

    github_info = config.get("github.com")
    if not github_info or "oauth_token" not in github_info:
        raise GitHubAuthError("Token OAuth não encontrado. Execute `gh auth login` primeiro.")
    return github_info["oauth_token"]


class TemplateClass(ABC):
    """Abstract base class for templates"""

    def __init__(self, config: TemplateConfig):
        self.config = config

    def __str__(self) -> str:
        """Pretty print representation of the template using rich markup"""
        url = f"https://github.com/{self.config.organization}/{self.config.repository}/tree/{self.config.branch}"
        return (
            f"[green]{self.config.name}[/green] - "
            f"[cyan]{self.config.description}[/cyan] "
            f"<[yellow]{url}[/yellow]>"
        )

    def _fetch_github_file(self, path: str) -> str:
        """Helper method to fetch files from GitHub"""
        url = f"https://api.github.com/repos/{self.config.organization}/{self.config.repository}/contents/{path}?ref={self.config.branch}"
        headers = {
            "Authorization": f"Bearer {token_github()}",
            "Accept": "application/vnd.github.v3.raw",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            raise GitHubAuthError("Você não possui acesso a esse repositório ou não esta logado na conta do github. Execute `gh auth login` primeiro.")
    
        response.raise_for_status()
        
        if not response.text:
            raise ValueError(f"Failed to fetch file from {url}")
        return response.text

    @abstractmethod
    def build(self, output_dir: str) -> None:
        """Build the template and create it in the specified directory"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the template is available"""
        pass

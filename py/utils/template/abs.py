from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple
import requests
import base64
import yaml


@dataclass
class TemplateConfig:
    """Configuration for a template"""

    name: str
    description: str
    type: str  # 'nix' or 'cookiecutter'
    organization: str
    repository: str
    branch: str = "main"


class TemplateClass(ABC):
    """Abstract base class for templates"""

    def __init__(self, config: TemplateConfig):
        self.config = config

    def _fetch_github_file(self, path: str) -> Tuple[Optional[dict], Optional[str]]:
        """Helper method to fetch files from GitHub"""
        try:
            url = f"https://api.github.com/repos/{self.config.organization}/{self.config.repository}/contents/{path}?ref={self.config.branch}"
            response = requests.get(url)

            if response.status_code != 200:
                return None, f"Error fetching from GitHub: HTTP {response.status_code}"

            content = response.json()
            file_content: str = base64.b64decode(content["content"]).decode("utf-8")
            return yaml.safe_load(file_content), None

        except requests.RequestException as e:
            return None, f"Network error while accessing GitHub: {str(e)}"
        except Exception as e:
            return None, f"Error fetching from GitHub: {str(e)}"

    @abstractmethod
    def get_template_options(self) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Fetch and return template options from the repository
        Returns: Tuple of (options_dict, error_message)
        """
        pass

    @abstractmethod
    def build_template(self, options: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Build the template with the given options
        Args:
            options: Dictionary of template options and their values
        Returns: Tuple of (success, error_message)
        """
        pass

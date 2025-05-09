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
    configPath: str = "config.yaml"


# def get_github_template_options(t:TemplateConfig):
#     """Fetch template options from GitHub repository"""
#     try:
#         # Fetch config.yaml from GitHub
#         url = f"https://api.github.com/repos/{t.organization}/{t.repository}/contents/{t.configPath}?ref={t.branch}"
#         response = requests.get(url)

#         if response.status_code != 200:
#             return None, f"Error fetching template config from GitHub: HTTP {response.status_code}"

#         content = response.json()
#         # Decode content from base64
#         file_content = base64.b64decode(content['content']).decode('utf-8')

#         # Parse YAML content
#         return yaml.safe_load(file_content), None
#     except requests.RequestException as e:
#         return None, f"Network error while accessing GitHub: {str(e)}"
#     except Exception as e:
#         return None, f"Error fetching template config from GitHub: {str(e)}"


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
            return file_content, None

        except requests.RequestException as e:
            return None, f"Network error while accessing GitHub: {str(e)}"
        except Exception as e:
            return None, f"Error fetching from GitHub: {str(e)}"

    def _fetch_template_options(self) -> Dict[str, Any]:
        """
        Fetch template options from the repository
        Returns: Tuple of (options_dict, error_message)
        """
        file_content = self._fetch_github_file(self.config.configPath)

        return yaml.safe_load(file_content)

    @abstractmethod
    def collect_inputs(self) -> str:
        """Collect inputs from the user and return them as a string (nix expression) or cookiecutter.json as a string"""
        pass

    @abstractmethod
    def display_summary(self, collected_data: Dict[str, Any]) -> bool:
        """Display a summary of the collected data"""
        pass

    @abstractmethod
    def build(self, config: str, output_dir: str) -> None:
        """Build the template and create it in the specified directory"""
        pass

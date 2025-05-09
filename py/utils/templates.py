import yaml
import requests
import base64
from template.abs import TemplateConfig, TemplateClass
from template.nix import NixTemplate
from template.cookiecutter import CookiecutterTemplate

# Configuration - can be set to "local" or "github"
SOURCE = "github"
# GitHub repo information
GITHUB_REPO_OWNER = "A3DAndre"
GITHUB_REPO_NAME = "demo"
GITHUB_BRANCH = "python-cli"  # Default branch


def new_template(config: TemplateConfig) -> TemplateClass:
    """Create a new template instance based on the configuration"""
    if config.type == "nix":
        return NixTemplate(config)
    elif config.type == "cookiecutter":
        return CookiecutterTemplate(config)
    else:
        raise ValueError(f"Unknown template type: {config.type}")


def get_templates():
    """Read templates from templates.yaml file locally or from GitHub"""
    # TODO: add spinner
    template_configs = get_github_templates()
    templates = [new_template(config) for config in template_configs]
    # TODO: end spinner
    return templates


def get_github_templates() -> list[TemplateConfig]:
    """Fetch templates from GitHub repository"""
    try:
        # Fetch templates.yaml from GitHub
        url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/templates.yaml?ref={GITHUB_BRANCH}"
        response = requests.get(url)

        if response.status_code != 200:
            return (
                None,
                f"Error fetching templates from GitHub: HTTP {response.status_code}",
            )

        content = response.json()
        # Decode content from base64
        file_content = base64.b64decode(content["content"]).decode("utf-8")

        # Parse YAML content
        data = yaml.safe_load(file_content)
        template_configs = data.get("templates", [])
        templates = [
            TemplateConfig(
                name=template["name"],
                description=template["description"],
                type=template["type"],
                organization=template["organization"],
                repository=template["repository"],
                branch=template.get("branch", GITHUB_BRANCH),
                configPath=template.get("configPath", "config.yaml"),
            )
            for template in template_configs
        ]
        return templates, None

    except requests.RequestException as e:
        return None, f"Network error while accessing GitHub: {str(e)}"
    except Exception as e:
        return None, f"Error fetching templates from GitHub: {str(e)}"


def set_template_source(source, owner=None, repo=None, branch=None):
    """Configure template source - local or GitHub"""
    global SOURCE, GITHUB_REPO_OWNER, GITHUB_REPO_NAME, GITHUB_BRANCH

    if source not in ["local", "github"]:
        return False, "Source must be 'local' or 'github'"

    SOURCE = source

    if source == "github":
        if owner:
            GITHUB_REPO_OWNER = owner
        if repo:
            GITHUB_REPO_NAME = repo
        if branch:
            GITHUB_BRANCH = branch

    return True, f"Template source set to {source}"

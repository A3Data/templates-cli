import yaml
import requests
import base64
from utils.template.abs import TemplateConfig, TemplateClass
from utils.template.nix import NixTemplate
from utils.template.cookiecutter import CookiecutterTemplate
import rich
import os
# import typer

# Configuration - can be set to "local" or "github"
SOURCE = "github"
# GitHub repo information
GITHUB_REPO_OWNER = "A3DAndre"
GITHUB_REPO_NAME = "demo"
GITHUB_BRANCH = "cookie/python-cli"  # Default branch


def pretty_print_template(template: TemplateConfig):
    rich.print(f"[bold magenta]Template Name:[/bold magenta] {template.name}\n")
    rich.print(f"[bold magenta]Description:[/bold magenta] {template.description}\n")
    rich.print(f"[bold magenta]Type:[/bold magenta] {template.type}\n")
    rich.print(f"[bold magenta]Organization:[/bold magenta] {template.organization}\n")
    rich.print(f"[bold magenta]Repository:[/bold magenta] {template.repository}\n")
    rich.print(f"[bold magenta]Branch:[/bold magenta] {template.branch}\n")
    rich.print(f"[bold magenta]Config Path:[/bold magenta] {template.configPath}\n")


def new_template(config: TemplateConfig) -> TemplateClass:
    """Create a new template instance based on the configuration"""
    print(f"Creating template: {config.name}")
    if config.type == "nix":
        return NixTemplate(config)
    elif config.type == "cookiecutter":
        return CookiecutterTemplate(config)
    else:
        raise ValueError(f"Unknown template type: {config.type}")


def get_templates() -> list[TemplateClass]:
    """Read templates from templates.yaml file locally or from GitHub"""
    # TODO: add spinner
    template_configs = get_github_templates()
    print(template_configs)
    print(template_configs.__class__)
    print(template_configs[0].__class__)
    # templates = [new_template(config) for config in template_configs]
    templates = []
    for config in template_configs:
        try:
            template = new_template(config)
            templates.append(template)
            print(template)
        except Exception as e:
            print(f"Error creating template: {e}")
            continue
    # TODO: end spinner
    return templates


def get_github_templates() -> list[TemplateConfig]:
    """Fetch templates from GitHub repository"""
    try:
        # Fetch templates.yaml from GitHub
        url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/templates.yaml?ref={GITHUB_BRANCH}"
        print(url)
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
        return templates

    except requests.RequestException as e:
        # return None, f"Network error while accessing GitHub: {str(e)}"
        print(f"Network error while accessing GitHub: {str(e)}")
        os.exit(1)
    except Exception as e:
        print(f"Error fetching templates from GitHub: {str(e)}")
        os.exit(1)
        # return None, f"Error fetching templates from GitHub: {str(e)}"


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

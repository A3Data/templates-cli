import os
import yaml
import requests
import base64
from .abs import TemplateConfig, TemplateClass
from .nix_template import NixTemplate
from .cookiecutter import CookiecutterTemplate

# GitHub repo information
GITHUB_REPO_OWNER = "A3Data"
GITHUB_REPO_NAME = "templates-cli"
GITHUB_BRANCH = "main"  
TEMPLATE_FILE_PATH = "templates.yaml"  
CLI_VERSION = 0.4
def get_github_templates() -> list[TemplateConfig]:
    """Fetch templates from GitHub repository"""
    try:
        # Fetch templates.yaml from GitHub
        # TODO: add headers + accept type to skip base64 dencoding 
        url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{TEMPLATE_FILE_PATH}?ref={GITHUB_BRANCH}"
        response = requests.get(url)

        if response.status_code == 401:
            raise ValueError("Você não possui acesso a esse repositório ou não esta logado na conta do github. Execute `gh auth login` primeiro.")
    
        response.raise_for_status()
                
        content = response.json()
        # Decode content from base64
        file_content = base64.b64decode(content["content"]).decode("utf-8")

        # Parse YAML content
        data = yaml.safe_load(file_content)
        
        version = data.get("version",None)
        if version != CLI_VERSION:
            RED = "\033[91m"
            RESET = "\033[0m"
            print(f"{RED}Warning: Uma nova versão da CLI foi encontrada.{RESET}")
            print(f"{RED}Versão atual: {CLI_VERSION}, Versão disponível: {version}{RESET}")
            print(f"{RED}Considere atualizar a CLI para obter as últimas melhorias e correções de bugs.{RESET}")
            print(f"{RED}Use `pip install git+https://github.com/A3Data/templates-cli.git --upgrade` to update.{RESET}")

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
        # print(f"Network error while accessing GitHub: {str(e)}")
        raise RuntimeError(f"Network error while accessing GitHub: {str(e)}")
    except Exception as e:
        # print(f"Error fetching templates from GitHub: {str(e)}")
        # os.exit(1)
        raise RuntimeError(f"Error fetching templates from GitHub: {str(e)}")

def new_template(config: TemplateConfig) -> TemplateClass:
    """Create a new template instance based on the configuration"""
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
    # templates = [new_template(config) for config in template_configs]
    templates = []
    for config in template_configs:
        try:
            template: TemplateClass = new_template(config)
            templates.append(template)
            # print(template)
        except Exception as e:
            print(f"Error creating template: {e}")
            continue
    # TODO: end spinner
    return templates



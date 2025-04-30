import yaml
import sys
import os
import requests
import json
import base64
from pathlib import Path

# Configuration - can be set to "local" or "github"
SOURCE = "github"
# GitHub repo information
GITHUB_REPO_OWNER = "A3DAndre"
GITHUB_REPO_NAME = "demo"
GITHUB_BRANCH = "main"  # Default branch


def get_templates():
    """Read templates from templates.yaml file locally or from GitHub"""
    if SOURCE == "local":
        return get_local_templates()
    else:
        return get_github_templates()


def get_local_templates():
    """Read templates from local templates.yaml file"""
    try:
        with open("templates.yaml", "r") as file:
            data = yaml.safe_load(file)
            return data.get("templates", [])
    except FileNotFoundError:
        return None, "Error: templates.yaml file not found"
    except yaml.YAMLError as e:
        return None, f"Error parsing templates.yaml: {e}"


def get_github_templates():
    """Fetch templates from GitHub repository"""
    try:
        # Fetch templates.yaml from GitHub
        url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/templates.yaml?ref={GITHUB_BRANCH}"
        response = requests.get(url)

        if response.status_code != 200:
            return None, f"Error fetching templates from GitHub: HTTP {response.status_code}"

        content = response.json()
        # Decode content from base64
        file_content = base64.b64decode(content['content']).decode('utf-8')

        # Parse YAML content
        data = yaml.safe_load(file_content)
        return data.get("templates", [])
    except requests.RequestException as e:
        return None, f"Network error while accessing GitHub: {str(e)}"
    except Exception as e:
        return None, f"Error fetching templates from GitHub: {str(e)}"


def get_template_options(template_name):
    """Read template options from template config file locally or from GitHub"""
    if SOURCE == "local":
        return get_local_template_options(template_name)
    else:
        return get_github_template_options(template_name)


def get_local_template_options(template_name):
    """Read template options from local template config file"""
    template_config_path = f"templates/{template_name}/config.yaml"
    try:
        with open(template_config_path, "r") as file:
            return yaml.safe_load(file), None
    except FileNotFoundError:
        return None, f"Error: Template config file not found: {template_config_path}"
    except yaml.YAMLError as e:
        return None, f"Error parsing template config: {e}"


def get_github_template_options(template_name):
    """Fetch template options from GitHub repository"""
    try:
        # Fetch config.yaml from GitHub
        url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/templates/{template_name}/config.yaml?ref={GITHUB_BRANCH}"
        response = requests.get(url)

        if response.status_code != 200:
            return None, f"Error fetching template config from GitHub: HTTP {response.status_code}"

        content = response.json()
        # Decode content from base64
        file_content = base64.b64decode(content['content']).decode('utf-8')

        # Parse YAML content
        return yaml.safe_load(file_content), None
    except requests.RequestException as e:
        return None, f"Network error while accessing GitHub: {str(e)}"
    except Exception as e:
        return None, f"Error fetching template config from GitHub: {str(e)}"


def set_nested_value(data_dict, path, value):
    """Set a value in a nested dictionary using dot notation path"""
    keys = path.split('.')
    current = data_dict

    # Navigate to the correct nested level, creating dicts as needed
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]

    # Set the final value
    current[keys[-1]] = value
    return data_dict


def flatten_config_summary(data, prefix=""):
    """Convert nested configuration data to a flattened format for display"""
    rows = []

    def add_row(key, value):
        rows.append({"key": key, "value": value})

    def process_dict(d, p=""):
        for k, v in d.items():
            path = f"{p}.{k}" if p else k
            if isinstance(v, dict):
                process_dict(v, path)
            else:
                add_row(path, v)

    process_dict(data, prefix)
    return rows


def generate_config_markdown_table(config_data):
    """Generate markdown table from configuration data"""
    table_data = "| Configuration | Value |\n| --- | --- |\n"

    for row in flatten_config_summary(config_data):
        table_data += f"| {row['key']} | {row['value']} |\n"

    return table_data


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

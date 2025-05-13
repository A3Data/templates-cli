from typing import Dict, Any
from cookiecutter.main import cookiecutter
import json
import yaml
from utils.template.abs import TemplateConfig, TemplateClass
from utils.ui import display_header, get_user_input, display_separator
from utils.ui import display_format_markdown, display_info


class CookiecutterTemplate(TemplateClass):
    def __init__(self, config: TemplateConfig):
        super().__init__(config)
        self._is_yaml_config = True
        self._raw_config = None

    def collect_inputs(self) -> str:
        """Collect inputs from the user based on template configuration"""
        display_header("Template Configuration")

        self._raw_config = self._get_template_config()

        if not self._raw_config:
            raise ValueError("Failed to load template configuration")

        collected_data = self._collect_user_inputs()
        return json.dumps(collected_data)

    def display_summary(self, collected_data: Dict[str, Any]) -> bool:
        """Display a summary of collected data and get confirmation"""
        display_header("Configuration Summary")

        summary = self._format_summary_table(json.loads(collected_data))
        display_format_markdown(summary)
        display_info(f"Template: {self.config.name}")

        return self._get_user_confirmation()

    def build(self, config: str, output_dir: str) -> None:
        """Build the cookiecutter template"""
        try:
            options = json.loads(config)
            cookiecutter(
                f"gh:{self.config.organization}/{self.config.repository}",
                no_input=True,
                extra_context=options,
                output_dir=output_dir,
                checkout=self.config.branch,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to build template: {str(e)}")

    def _get_template_config(self) -> Dict[str, Any]:
        """Try to load YAML config first, fallback to JSON if not found"""
        # Try YAML config first
        yaml_content = self._fetch_github_file(self.config.configPath)
        if yaml_content:
            self._is_yaml_config = True
            return yaml.safe_load(yaml_content)

        raise ValueError(f"Failed to load yaml config {yaml_content}")
        # Fallback to JSON config
        # json_content, json_error = self._fetch_github_file("cookiecutter.json")
        # if not json_error and json_content:
        #     self._is_yaml_config = False
        #     return json.loads(json_content)

        # raise ValueError(
        #     "No valid configuration found (tried cookiecutter.yaml and cookiecutter.json)"
        # )

    def _collect_user_inputs(self) -> Dict[str, Any]:
        """Collect user inputs based on configuration format"""
        if self._is_yaml_config:
            return self._collect_from_yaml()
        else:
            return self._collect_from_json()

    def _collect_from_yaml(self) -> Dict[str, Any]:
        """Collect inputs based on YAML structured format"""
        collected_data = {}
        print(self._raw_config)
        for field_name, field_config in self._raw_config.items():
            # print(field_config)
            prompt = field_config.get("prompt", field_name)
            default = field_config.get("default", "")

            value, success = get_user_input(prompt, str(default))
            if not success:
                raise ValueError("Input collection cancelled by user")

            collected_data[field_name] = value
            display_separator()

        return collected_data

    def _collect_from_json(self) -> Dict[str, Any]:
        """Collect inputs based on cookiecutter.json format"""
        collected_data = {}

        for key, default in self._raw_config.items():
            if key.startswith("_"):  # Skip private variables
                continue

            prompt = f"Enter {key}"
            value, success = get_user_input(prompt, str(default))
            if not success:
                raise ValueError("Input collection cancelled by user")

            collected_data[key] = value
            display_separator()

        return collected_data

    def _format_summary_table(self, data: Dict[str, Any]) -> str:
        """Format collected data as markdown table"""
        table_rows = ["| Parameter | Value |", "|-----------|-------|"]

        for key, value in data.items():
            table_rows.append(f"| {key} | {value} |")

        return "\n".join(table_rows)

    def _get_user_confirmation(self) -> bool:
        """Get user confirmation for the configuration"""
        response, success = get_user_input("Do you want to proceed? (y/N)", "N")
        return success and response.lower() == "y"

from typing import Dict, Any
import subprocess
from utils.template.abs import TemplateClass
from utils.ui import display_header, get_user_input, display_separator
from utils.ui import display_info, display_code
import yaml
from utils import nix


class NixTemplate(TemplateClass):
    def collect_inputs(self) -> str:
        """Collect inputs from the user based on template configuration"""
        display_header("Template Configuration")
        # Get template config
        config = self._get_template_config()
        if not config:
            raise ValueError("Failed to load template configuration")

        # Collect inputs and convert to Nix expression
        collected_data = self._prompt_user(config)

        self.display_summary(collected_data)

        return self._generate_nix_attr_set(collected_data)

    def _prompt_user(self, template_options):
        """Collect user inputs based on template options"""
        collected_data = {}

        print(display_header("Template Configuration"))

        for field_name, field_config in template_options.items():
            field_type = field_config.get("type")
            prompt = field_config.get("prompt", f"Enter {field_name}")
            default = field_config.get("default", "")
            option = field_config.get("option", field_name)

            if field_type == "input":
                value, success = get_user_input(prompt, default)
                if success:
                    nix.set_nested_value(collected_data, option, value)

            elif field_type == "choose":
                # choices = field_config.get("choices", [])
                # value, success = get_user_choice(prompt, choices)
                value, success = get_user_input(prompt + " Sim/Não", default)

                if success:
                    # Convert 'Sim'/'Não' to boolean values for options
                    if value == "Sim":
                        value = True
                    elif value == "Não":
                        value = False

                    nix.set_nested_value(collected_data, option, value)
                elif default:
                    # Use default if user canceled
                    value = default
                    display_info(f"Using default: {default}")
                    nix.set_nested_value(collected_data, option, value)

            display_separator()

        return collected_data

    def display_summary(self, collected_data: Dict[str, Any]) -> bool:
        """Display a summary of collected data and get confirmation"""
        display_header("Configuration Summary")

        # Display the Nix expression
        display_info("Generated Nix Configuration:")
        display_code(collected_data, "nix")
        display_info(f"Template: {self.config.name}")

        # Get user confirmation
        return self._get_user_confirmation()

    def build(self, config: str, output_dir: str) -> None:
        """Build the nix template"""
        try:
            # Create Nix expression
            nix_expr = self._create_nix_expression(config)

            # Run nix-build
            result = subprocess.run(
                ["nix", "build", "--impure", "--print-out-paths", "--expr", nix_expr],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                raise RuntimeError(f"Nix build failed: {result.stderr}")

        except Exception as e:
            raise RuntimeError(f"Failed to build template: {str(e)}")

    def _get_template_config(self):
        """Get template configuration from YAML"""
        yaml_content = self._fetch_github_file(self.config.configPath)
        print(yaml_content)
        if not yaml_content:
            raise ValueError("Failed to fetch template config")

        return yaml.safe_load(yaml_content)

    def _generate_nix_attr_set(self, data: Dict[str, Any]) -> str:
        """Convert dictionary to Nix attribute set"""
        nix_attrs = []

        for key, value in data.items():
            if isinstance(value, bool):
                nix_value = "true" if value else "false"
            elif isinstance(value, (int, float)):
                nix_value = str(value)
            elif isinstance(value, dict):
                nix_value = self._generate_nix_attr_set(value)
            else:
                nix_value = f'"{value}"'

            nix_attrs.append(f"  {key} = {nix_value};")

        return "{\n" + "\n".join(nix_attrs) + "\n}"

    def _create_nix_expression(self, attr_set: str) -> str:
        """Create complete Nix expression for building"""
        return f"""
        with import <nixpkgs> {{}};
        let
            template = builtins.getFlake "github:{self.config.organization}/{self.config.repository}";
            args = {attr_set};
        in
            template.packages.x86_64-linux.{self.config.name} args
        """

    def _get_user_confirmation(self) -> bool:
        """Get user confirmation for the configuration"""
        response, success = get_user_input("Do you want to proceed? (y/N)", "N")
        return success and response.lower() == "y"

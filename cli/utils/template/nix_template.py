from typing import Dict, Any
import subprocess
from utils.template.abs import TemplateClass
import utils.ui as ui
import yaml
from utils import nix


class NixTemplate(TemplateClass):
    def collect_inputs(self) -> str:
        """Collect inputs from the user based on template configuration"""
        ui.display_header("Template Configuration")
        # Get template config
        config = self._get_template_config()
        if not config:
            raise ValueError("Failed to load template configuration")

        # Collect inputs and convert to Nix expression
        collected_data = self._prompt_user(config)

        print(collected_data)

        return self._generate_nix_attr_set(collected_data)

    def _prompt_user(self, template_options):
        """Collect user inputs based on template options"""
        return ui.collect_template_inputs(template_options)


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

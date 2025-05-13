import subprocess
from typing import Dict, Any
from utils.template.abs import TemplateClass

class NixTemplate(TemplateClass):
    def encode_input(self, collected_data) -> str:
        """Encodes the collected data into a Nix attribute set that will be used as the arguments for the derivation that builds the template"""
        return self._generate_nix_attr_set(collected_data)

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

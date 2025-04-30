import subprocess
import tempfile
import os

def generate_nix_attr_set(data):
    """Convert a dictionary to a Nix attribute set string"""
    result = "{\n"

    def format_value(val):
        if isinstance(val, str):
            # Escape quotes in strings
            escaped = val.replace('"', '\\"')
            return f'"{escaped}"'
        elif isinstance(val, bool):
            return "true" if val else "false"
        elif isinstance(val, (int, float)):
            return str(val)
        elif isinstance(val, dict):
            return generate_nix_attr_set(val)
        elif val is None:
            return "null"
        else:
            return f'"{val}"'

    # Generate each attribute
    for key, value in data.items():
        if isinstance(value, dict):
            result += f"  {key} = {generate_nix_attr_set(value)};\n"
        else:
            result += f"  {key} = {format_value(value)};\n"

    result += "}"
    return result

def create_nix_expression(template_name, attr_set):
    """Create a Nix expression for the given template and attribute set"""
    return f'''
    with import <nixpkgs> {{}};
    let
      template = builtins.getFlake "github:A3DAndre/demo";
      args = {attr_set};
    in
    template.packages.x86_64-linux.{template_name} args
    '''

def run_nix_build(nix_expr):
    """Run nix build command with the given Nix expression and return the result"""
    try:
        # Run the Nix build command
        build_result = subprocess.run(
            ["nix", "build", "--impure", "--print-out-paths", "--expr", nix_expr],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if build_result.returncode == 0:
            output_path = build_result.stdout.strip()
            return {
                "success": True,
                "output_path": output_path,
                "stderr": None
            }
        else:
            return {
                "success": False,
                "output_path": None,
                "stderr": build_result.stderr
            }
    except Exception as e:
        return {
            "success": False,
            "output_path": None,
            "stderr": str(e)
        }

def format_nix_command(nix_expr):
    """Format the nix build command for display"""
    return f"nix build --impure --print-out-paths --expr '{nix_expr}'"

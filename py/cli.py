#!/usr/bin/env python3
import typer
from typing import Dict, Any, Optional
from rich.console import Console

# Import our modules
from utils import ui
from utils import nix
from utils import templates

app = typer.Typer()
console = Console()


def collect_inputs(template_options: Dict[str, Any]) -> Dict[str, Any]:
    """Collect user inputs based on template options"""
    collected_data = {}

    ui.display_header("Template Configuration")

    for field_name, field_config in template_options.items():
        field_type = field_config.get("type")
        prompt = field_config.get("prompt", f"Enter {field_name}")
        default = field_config.get("default", "")
        option = field_config.get("option", field_name)

        if field_type == "input":
            value, success = ui.get_user_input(prompt, default)
            if success:
                templates.set_nested_value(collected_data, option, value)

        elif field_type == "choose":
            choices = field_config.get("choices", [])
            value, success = ui.get_user_choice(prompt, choices)

            if success:
                # Convert 'Sim'/'Não' to boolean values for options
                if value == "Sim":
                    value = True
                elif value == "Não":
                    value = False

                templates.set_nested_value(collected_data, option, value)
            elif default:
                value = default
                ui.display_info(f"Using default: {default}", ui.ACCENT_COLOR)
                templates.set_nested_value(collected_data, option, value)

        ui.display_separator()

    return collected_data


def display_summary(template_name: str, collected_data: Dict[str, Any]) -> bool:
    """Display a summary of the collected data"""
    ui.display_header("Configuration Summary")

    # Generate markdown table
    table_md = templates.generate_config_markdown_table(collected_data)
    ui.display_format_markdown(table_md)
    ui.display_info(f"Template: {template_name}")

    # Confirmation step
    result, success = ui.get_user_choice(
        "Do you want to proceed with these settings?", ["Yes", "No"]
    )

    if result != "Yes" or not success:
        ui.display_error("Operation canceled by user")
        return False
    return True


def build_project(template_name: str, attr_set: str) -> Optional[str]:
    """Build the project using Nix"""
    ui.display_header("Building with Nix")

    # Create the Nix expression
    nix_expr = nix.create_nix_expression(template_name, attr_set)
    build_cmd_str = nix.format_nix_command(nix_expr)

    ui.display_info("Running command:", ui.ACCENT_COLOR)
    ui.display_code(build_cmd_str, "sh")

    # Run the Nix build with a spinner
    def do_build():
        return nix.run_nix_build(nix_expr)

    build_result = ui.display_spinner(
        "Building project... This may take a while", do_build
    )

    if build_result["success"]:
        output_path = build_result["output_path"]
        ui.display_success("✓ Build completed successfully!")
        ui.display_info(f"Output path: {output_path}")
        return output_path

    ui.display_error("❌ Build failed!")

    if build_result["stderr"]:
        ui.display_header("Error Details")
        ui.display_info(build_result["stderr"], "red")

    return None


@app.command()
def main():
    """A3 Template Generator CLI"""
    title = """
     _    _____   _____                    _       _
    / \\  |___ /  |_   _|__ _ __ ___  _ __ | | __ _| |_ ___  ___
   / _ \\   |_ \\    | |/ _ \\ '_ ` _ \\| '_ \\| |/ _` | __/ _ \\/ __|
  / ___ \\ ___) |   | |  __/ | | | | | |_) | | (_| | ||  __/\\__ |
 /_/   \\_\\____/    |_|\\___|_| |_| |_| .__/|_|\\__,_|\\__\\___||___/
                                    |_|
"""
    console.print(title)

    # Get available templates with a spinner
    templates_data = ui.display_spinner("Loading templates...", templates.get_templates)

    if isinstance(templates_data, tuple):
        ui.display_error(templates_data[1])
        raise typer.Exit(1)

    # Extract template information for display
    # template_info = [
    #     f"{template['name']} - {template['description']}"
    #     for template in templates_data
    # ]
    template_info = [f"{template['name']}" for template in templates_data]

    # Display templates and let user select one
    ui.display_header("Select a Template")
    selected_option, success = ui.get_user_choice("Choose a template:", template_info)

    if not success or not selected_option:
        ui.display_error("Template selection canceled")
        raise typer.Exit(1)

    selected_template = selected_option.split(" - ")[0]
    ui.display_info(f"Selected template: {selected_template}", ui.PRIMARY_COLOR)

    # Get template options
    template_options, error = ui.display_spinner(
        f"Loading template options for {selected_template}...",
        templates.get_template_options,
        selected_template,
    )

    if error:
        ui.display_error(error)
        raise typer.Exit(1)

    # Collect inputs and build
    collected_data = collect_inputs(template_options)
    if display_summary(selected_template, collected_data):
        nix_attr_set = nix.generate_nix_attr_set(collected_data)

        ui.display_header("Generated Nix Configuration")
        ui.display_code(nix_attr_set, "nix")

        result, success = ui.get_user_choice(
            "Do you want to build with this configuration?", ["Yes", "No"]
        )

        if result == "Yes" and success:
            output_path = build_project(selected_template, nix_attr_set)
            if output_path:
                console.print(output_path)
        else:
            ui.display_error("Build canceled by user")


if __name__ == "__main__":
    app()

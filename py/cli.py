#!/usr/bin/env python3
import typer
from rich.console import Console

# Import our modules
from utils import ui
from utils.template import get_templates
from utils.template import TemplateClass

app = typer.Typer()
console = Console()


def choose_template(templates: list[TemplateClass]) -> TemplateClass:
    """Prompt the user to choose a template from the list"""
    ui.display_header("Available Templates")

    # Display templates with descriptions
    template_info = [
        f"{template['name']} - {template['description']}" for template in templates
    ]

    selected_option, success = ui.get_user_choice("Choose a template:", template_info)

    if not success or not selected_option:
        ui.display_error("Template selection canceled")
        raise typer.Exit(1)

    selected_template = selected_option.split(" - ")[0]
    ui.display_info(f"Selected template: {selected_template}", ui.PRIMARY_COLOR)

    return selected_template


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
    templates_data = get_templates()
    template = choose_template(templates_data)
    template_config = template.collect_inputs()
    template.build(template_config)


if __name__ == "__main__":
    app()

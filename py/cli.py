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

    # Display templates with index
    for idx, template in enumerate(templates, 1):
        ui.display_info(f"{idx}. {template.config.name}", ui.PRIMARY_COLOR)

    while True:
        try:
            choice = input("\nEnter template number: ").strip()
            if not choice:
                ui.display_error("Template selection canceled")
                raise typer.Exit(1)

            index = int(choice) - 1
            if 0 <= index < len(templates):
                selected_template = templates[index]
                ui.display_info(
                    f"Selected template: {selected_template.config.name}",
                    ui.PRIMARY_COLOR,
                )
                return selected_template
            else:
                ui.display_error(
                    f"Please enter a number between 1 and {len(templates)}"
                )
        except ValueError:
            ui.display_error("Please enter a valid number")


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

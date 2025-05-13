#!/usr/bin/env python3
import typer
from rich.console import Console

# Import our modules
from utils import ui
from utils.template import get_templates
from utils.template import TemplateClass

app = typer.Typer()
console = Console()


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
    template = ui.choose_template(templates_data)
    template_options = template.get_template_options()
    collected_data = ui.collect_template_inputs(template_options)
    template_config = template.encode_input(collected_data)
    print(template_config)
    template.build(template_config, "./output")


if __name__ == "__main__":
    app()

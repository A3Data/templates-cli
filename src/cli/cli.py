#!/usr/bin/env python3
import typer
from rich.console import Console
from rich.panel import Panel
from rich.traceback import Traceback
import subprocess
# Import our modules
from .utils import ui
from .utils.template import get_templates
from .utils.template import TemplateClass

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
    try:
        console.print(title)
        # Get available templates with a spinner
        templates_data = get_templates()
        template:TemplateClass = ui.choose_item(templates_data, "template")
        assert template.is_available(), "Template is not available"
        
        try:
            template_options = template.get_template_options()
            collected_data = ui.collect_template_inputs(template_options)
            template_config = template.encode_input(collected_data)
            console.print(template_config)
        except Exception as e:
            console.print(Panel(
                f"[yellow]Warning: Falha ao carregar informações adicionais.\nA engine do template será responsavel por criar o template.", # \nReason: {str(e)}[/yellow]
                title="Warning",
                border_style="yellow"
            ))
            template_config = "{}"  # or set to a sensible default if needed

        # Ask for output directory
        output_dir, success = ui.get_string_option(
            "Em qual pasta vc gostaria de criar o template?",
            default="./."
        )
        if not success:
            raise KeyboardInterrupt

        template.build(template_config, output_dir)
    except KeyboardInterrupt:
        console.print("\n[yellow]Process cancelled by user[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(Panel(
            f"[red]Error while generating template:[/red]\n{str(e)}",
            title="Error",
            border_style="red"
        ))
        # Print detailed traceback in debug mode
        # console.print(Traceback(), soft_wrap=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()

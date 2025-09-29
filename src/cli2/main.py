#!/usr/bin/env python3
import json
import typer
from rich.console import Console
from rich.panel import Panel
from rich.traceback import Traceback
import os

# Import our modules
from .utils import ui
from .templates.factory import get_templates, TemplateClass
from .templates.abs import GitHubAuthError
from .utils.telemetry import send_telemetry


app = typer.Typer(
    help="Uma ferramenta CLi para gerar templates de projetos da A3 Data. Utilize o comando 'a3t' para criar um novo projeto a partir de um template."
)
console = Console()


@app.command("list")
def list_templates(
    json_output: bool = typer.Option(False, "--json", help="Output as JSON")
):
    """List available templates."""
    templates_data = get_templates()
    if json_output:
        output = [t.config.__dict__ for t in templates_data]
        console.print(json.dumps(output, indent=2))
    else:
        ui.display_header("Templates disponíveis:")
        for idx, t in enumerate(templates_data):
            console.print(f"[{idx}] {t.config.name} - {t.config.description}")


@app.command("build")
def build_template(
    template_id: int = typer.Option(
        ..., "--template", "-t", help="ID do template (use 'a3t list' para ver os IDs)"
    )
):
    """Build a template by ID and options."""
    templates_data = get_templates()

    template: TemplateClass = templates_data[template_id]
    send_telemetry(
        {
            "template_name": template.config.name,
            "code": "BUILD_TEMPLATE",
            "metadata": {
                "organization": template.config.organization,
                "repository": template.config.repository,
                "branch": template.config.branch,
            },
        }
    )
    if not template.is_available():
        console.print(f"[red]Template não disponível ou não encontrado.[/red]")
        raise typer.Exit(1)
    try:
        output_dir, success = ui.get_string_option(
            "Em qual pasta vc gostaria de criar o template? (Pressione Enter para usar a pasta atual)",
            default="./.",
        )
        console.print(
            f"[bold]O template será criado na pasta:[/bold] { os.path.abspath(output_dir) }"
        )
        if not success:
            raise KeyboardInterrupt

        template.build(output_dir)

        send_telemetry(
            {
                "template_name": template.config.name,
                "metadata": {
                    "organization": template.config.organization,
                    "repository": template.config.repository,
                    "branch": template.config.branch,
                },
                "code": "TEMPLATE_GENERATED",
            }
        )

    except KeyboardInterrupt:
        console.print("\n[yellow]Process cancelled by user[/yellow]")
        raise typer.Exit(1)
    except Exception as e:

        send_telemetry(
            {
                "template_name": template.config.name,
                "metadata": {
                    "organization": template.config.organization,
                    "repository": template.config.repository,
                    "branch": template.config.branch,
                    "error": str(e),
                },
                "code": "ERROR_GENERATING_TEMPLATE",
            }
        )
        console.print(
            Panel(
                f"[red]Error while generating template:[/red]\n{str(e)}",
                title="Error",
                border_style="red",
            )
        )
        ui.display_header(
            "Para relatar um bug, por favor, abra uma issue no repositório do GitHub."
        )
        console.print(
            "[bold]Repositório do GitHub:[/bold] https://github.com/A3Data/templates-cli/issues"
        )
        raise typer.Exit(1)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
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
        ui.display_header(
            "Um gerador de templates para acelerar o eu.A3 para sugestões e melhorias, abra uma issue no repositório da CLI, ou do template especifico."
        )
        console.print(
            "[bold] GitHub:[/bold] https://github.com/A3Data/templates-cli/issues"
        )
        # Get available templates with a spinner
        templates_data = get_templates()
        template: TemplateClass = ui.choose_item(templates_data, "template")
        assert template.is_available(), "Template não disponível ou não encontrado."

        send_telemetry(
            {
                "template_name": template.config.name,
                "metadata": {
                    "organization": template.config.organization,
                    "repository": template.config.repository,
                    "branch": template.config.branch,
                },
                "code": "SELECTED_TEMPLATE",
            }
        )

        # Ask for output directory
        output_dir, success = ui.get_string_option(
            "Em qual pasta vc gostaria de criar o template? (Pressione Enter para usar a pasta atual)",
            default="./.",
        )
        console.print(
            f"[bold]O template será criado na pasta:[/bold] { os.path.abspath(output_dir) }"
        )
        if not success:
            raise KeyboardInterrupt

        template.build(output_dir)

        send_telemetry(
            {
                "template_name": template.config.name,
                "metadata": {
                    "organization": template.config.organization,
                    "repository": template.config.repository,
                    "branch": template.config.branch,
                },
                "code": "TEMPLATE_GENERATED",
            }
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Process cancelled by user[/yellow]")
        raise typer.Exit(1)
    except Exception as e:

        send_telemetry(
          {
                "template_name": template.config.name,
                "metadata": {
                    "organization": template.config.organization,
                    "repository": template.config.repository,
                    "branch": template.config.branch,
                },
                "code": "ERROR_GENERATING_TEMPLATE",
            }
        )
        console.print(
            Panel(
                f"[red]Error while generating template:[/red]\n{str(e)}",
                title="Error",
                border_style="red",
            )
        )
        ui.display_header(
            "Para relatar um bug, por favor, abra uma issue no repositório do GitHub."
        )
        console.print(
            "[bold]Repositório do GitHub:[/bold] https://github.com/A3Data/templates-cli/issues"
        )
        # Print detailed traceback in debug mode
        # console.print(Traceback(), soft_wrap=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

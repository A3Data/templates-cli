from typing import List, Any, Callable
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel
from rich.prompt import Prompt

# Define color constants
PRIMARY_COLOR = "yellow"  # Yellow for main elements
SECONDARY_COLOR = "blue"  # Blue for secondary elements
ACCENT_COLOR = "cyan"  # Cyan for highlights
SEPARATOR_COLOR = "grey70"  # Grey for separators

console = Console()


def display_header(text: str) -> None:
    """Display a styled header"""
    console.print(
        Panel(
            text,
            style=PRIMARY_COLOR,
            border_style=PRIMARY_COLOR,
            padding=(0, 1),
            width=65,
        )
    )


def display_error(message: str) -> None:
    """Display error message"""
    console.print(f"[red bold]{message}[/]")


def display_success(message: str) -> None:
    """Display success message"""
    console.print(f"[green bold]{message}[/]", justify="center", width=50)


def display_info(message: str, color: str = SECONDARY_COLOR) -> None:
    """Display informational message"""
    console.print(f"[{color}]{message}[/]")


def display_code(code: str, language: str = "") -> None:
    """Display code with syntax highlighting"""
    syntax = Syntax(code, language or "text", theme="monokai")
    print(syntax)


def get_user_choice(prompt: str, options: List[str]) -> tuple[str, bool]:
    """Get user choice from a list of options"""
    display_info(prompt, PRIMARY_COLOR)
    try:
        # Use Rich's Prompt with choices
        result = Prompt.ask(
            "", choices=[opt.replace(" ", "_") for opt in options], show_choices=True
        )
        # Convert back from underscore format to original option
        original_option = next(
            opt for opt in options if opt.replace(" ", "_") == result
        )
        return original_option, True
    except KeyboardInterrupt:
        return "", False


def get_user_input(
    prompt: str, default: str = "", placeholder: str = ""
) -> tuple[str, bool]:
    """Get user input with a prompt"""
    # Display the prompt
    console.print(f"[{SECONDARY_COLOR} bold]{prompt}[/]")

    # Show default value hint if provided
    if default:
        console.print(
            f"[{ACCENT_COLOR}]Default: {default} (Press Enter to use default)[/]"
        )

    try:
        value = Prompt.ask("", default=default, show_default=False)

        if not value and default:
            console.print(f"[italic {ACCENT_COLOR}]Using default: {default}[/]")
            value = default

        return value, True
    except KeyboardInterrupt:
        return "", False


def display_separator() -> None:
    """Display a separator line"""
    console.print(f"[{SEPARATOR_COLOR}]{'─' * 35}[/]")


def display_spinner(
    message: str, action_func: Callable, *args: Any, **kwargs: Any
) -> Any:
    """Display a spinner while executing a function"""
    with console.status(message, spinner="dots"):
        return action_func(*args, **kwargs)


def display_format_markdown(markdown_text: str) -> None:
    """Display formatted markdown text"""
    md = Markdown(markdown_text)
    console.print(md)

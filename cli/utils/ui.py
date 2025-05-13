from typing import List, Any, Callable, Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.status import Status

# Define color constants
PRIMARY_COLOR = "yellow"
SECONDARY_COLOR = "blue"
ACCENT_COLOR = "cyan"
SEPARATOR_COLOR = "grey70"

console = Console()


def display_header(text: str) -> None:
    """Display a styled header in a panel"""
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
    """Display error message in red"""
    console.print(f":x: [red bold]{message}[/]")


def display_success(message: str) -> None:
    """Display success message in green"""
    console.print(f":white_check_mark: [green bold]{message}[/]")


def display_info(message: str, color: str = SECONDARY_COLOR) -> None:
    """Display informational message in specified color"""
    console.print(f"[{color}]{message}[/]")


def display_code(code: str, language: str = "") -> None:
    """Display code with syntax highlighting"""
    syntax = Syntax(code, language or "text", theme="monokai")
    console.print(syntax)


def get_user_choice(prompt: str, options: List[str]) -> tuple[str, bool]:
    """Get user choice from a list of options using Rich's Prompt"""
    try:
        display_info(prompt, PRIMARY_COLOR)
        # Convert spaces to underscores for choices
        choice_map = {opt.replace(" ", "_"): opt for opt in options}
        result = Prompt.ask(
            "",
            choices=list(choice_map.keys()),
            show_choices=True,
        )
        return choice_map[result], True
    except KeyboardInterrupt:
        return "", False


def get_user_input(
    prompt: str,
    default: str = "",
    validate: Optional[Callable[[str], bool]] = None,
) -> tuple[str, bool]:
    """Get user input with optional validation"""
    try:
        # Show prompt with color
        console.print(f"[{SECONDARY_COLOR}]{prompt}[/]")

        if default:
            console.print(f"[{ACCENT_COLOR}]Default: {default}[/]")

        while True:
            value = Prompt.ask("", default=default, show_default=False)

            if not value and default:
                value = default
                console.print(f"[italic {ACCENT_COLOR}]Using default: {default}[/]")

            if validate is None or validate(value):
                return value, True

            display_error("Invalid input, please try again")

    except KeyboardInterrupt:
        return "", False


def get_user_confirmation(prompt: str, default: bool = False) -> bool:
    """Get yes/no confirmation from user"""
    try:
        return Confirm.ask(prompt, default=default)
    except KeyboardInterrupt:
        return False


def display_separator() -> None:
    """Display a separator line"""
    console.print(f"[{SEPARATOR_COLOR}]{'─' * 35}[/]")


def display_spinner(
    message: str, action_func: Callable, *args: Any, **kwargs: Any
) -> Any:
    """Display a spinner while executing a function"""
    with Status(message, spinner="dots") as status:
        try:
            result = action_func(*args, **kwargs)
            status.update("[green]Complete!")
            return result
        except Exception as e:
            status.update("[red]Failed!")
            raise e


def display_format_markdown(markdown_text: str) -> None:
    """Display formatted markdown text"""
    md = Markdown(markdown_text)
    console.print(md)

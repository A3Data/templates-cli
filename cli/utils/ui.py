
import sys
from typing import List, Any, Callable, Optional, Union, Set, Dict
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


def get_string_option(
    prompt: str,
    default: str = "",
    validate: Optional[Callable[[str], bool]] = None,
) -> tuple[str, bool]:
    """Get a string input from the user with optional validation.

    Args:
        prompt: The prompt to show to the user
        default: Default value if no input is provided
        validate: Optional validation function

    Returns:
        tuple[str, bool]: The input value and whether input was successful
    """
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


def get_radio_option(
    prompt: str, options: List[str], default: Optional[str] = None
) -> tuple[str, bool]:
    """Get a single selection from a list of options using radio-style selection.

    Args:
        prompt: The prompt to show to the user
        options: List of options to choose from
        default: Default option if none selected

    Returns:
        tuple[str, bool]: The selected option and whether selection was successful
    """
    try:
        display_info(prompt, PRIMARY_COLOR)
        # Convert spaces to underscores for choices
        choice_map = {opt.replace(" ", "_"): opt for opt in options}

        default_key = default.replace(" ", "_") if default in options else None

        result = Prompt.ask(
            "",
            choices=list(choice_map.keys()),
            default=default_key,
            show_choices=True,
            show_default=bool(default),
        )
        return choice_map[result], True
    except KeyboardInterrupt:
        return "", False


def get_checkbox_option(
    prompt: str, options: List[str], default: Optional[List[str]] = None
) -> tuple[List[str], bool]:
    """Get multiple selections from a list of options using checkboxes.

    Args:
        prompt: The prompt to show to the user
        options: List of options to choose from
        default: Default selected options

    Returns:
        tuple[List[str], bool]: The selected options and whether selection was successful
    """
    try:
        display_info(prompt, PRIMARY_COLOR)
        result = Prompt.ask(
            "",
            choices=options,
            default=default,
            show_default=bool(default),
        )
        return result, True
    except KeyboardInterrupt:
        return [], False


def get_boolean_option(prompt: str, default: bool = False) -> tuple[bool, bool]:
    """Get a boolean input from the user.

    Args:
        prompt: The prompt to show to the user
        default: Default value if no input is provided

    Returns:
        tuple[bool, bool]: The boolean value and whether input was successful
    """
    try:
        result = Confirm.ask(prompt, default=default)
        return result, True
    except KeyboardInterrupt:
        return False, False

def collect_template_inputs(raw_config: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Collect user inputs based on template configuration.
    
    Args:
        raw_config: Dictionary containing template configuration options
        
    Returns:
        Dict[str, Any]: Dictionary containing collected user inputs. Returns field names 
        with their collected values. For radio/checkbox options, returns selected values 
        from the options list.
        
    Example raw_config:
        {
            "projectName": {
                "type": "string",
                "prompt": "What is the project name?",
                "default": "my-project"
            },
            "features": {
                "type": "checkbox",
                "prompt": "Select features to include",
                "list": ["api", "cli", "web"],
                "default": ["api"]
            },
            "deployment": {
                "type": "radio",
                "prompt": "Select deployment platform",
                "list": ["aws", "gcp", "azure"],
                "default": "aws"
            }
        }
    """
    collected_data = {}
    display_header("Template Configuration")

    for field_name, field_config in raw_config.items():
        option_type = field_config.get("type", "string")
        prompt = field_config.get("prompt", field_name)
        default = field_config.get("default")
        
        # Get user input based on option type
        if option_type == "string":
            value, success = get_string_option(prompt, str(default or ""))
            
        elif option_type == "checkbox":
            options = field_config.get("list", [])
            if isinstance(default, str):
                default = [default] if default else []
            value, success = get_checkbox_option(prompt, options, default)
            
        elif option_type == "radio":
            options = field_config.get("list", [])
            value, success = get_radio_option(prompt, options, default)
            
        elif option_type == "boolean":
            if isinstance(default, str):
                default = default.lower() == "true"
            value, success = get_boolean_option(prompt, bool(default))
            
        else:
            display_error(f"Unsupported option type: {option_type}")
            continue

        if not success:
            value = default

        # Store the collected value and its option path if specified
        option_path = field_config.get("option", field_name)
        collected_data[option_path] = value
        display_separator()

    return collected_data


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


def choose_item(items: list[Any], item_name: str = "item") -> Any:
    """Prompt the user to choose an item from the list"""
    display_header(f"Available {item_name.capitalize()}s")

    # Display items with index
    for idx, item in enumerate(items, 1):
        display_info(f"{idx}. {item}", PRIMARY_COLOR)

    while True:
        try:
            choice = input(f"\nEnter {item_name} number: ").strip()
            if not choice:
                display_error(f"{item_name.capitalize()} selection canceled")
                sys.exit(1)

            index = int(choice) - 1
            if 0 <= index < len(items):
                selected_item = items[index]
                display_info(
                    f"Selected {item_name}: {selected_item}",
                    PRIMARY_COLOR,
                )
                return selected_item
            else:
                display_error(
                    f"Please enter a number between 1 and {len(items)}"
                )
        except ValueError:
            display_error("Please enter a valid number")

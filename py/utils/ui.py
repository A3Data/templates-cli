import subprocess
import sys

# Define color constants
PRIMARY_COLOR = "yellow"      # Yellow for main elements
SECONDARY_COLOR = "blue"      # Blue for secondary elements
ACCENT_COLOR = "cyan"         # Cyan for highlights
SEPARATOR_COLOR = "240"       # Grey for separators

def run_command(args, input_text=None):
    """Helper function to run shell commands"""
    if input_text:
        process = subprocess.run(
            args,
            input=input_text,
            stdout=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
    else:
        process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
    return process.stdout.strip(), process.returncode

def display_header(text):
    """Display a styled header"""
    output, _ = run_command([
        "gum", "style",
        "--foreground", PRIMARY_COLOR,
        "--border", "rounded",
        "--border-foreground", PRIMARY_COLOR,
        "--padding", "0 1",
        "--align", "center",
        "--width", "65",
        text
    ])
    return output

def display_error(message):
    """Display error message"""
    error_msg, _ = run_command([
        "gum", "style",
        "--foreground", "red",
        "--bold",
        message
    ])
    print(error_msg)

def display_success(message):
    """Display success message"""
    success_msg, _ = run_command([
        "gum", "style",
        "--foreground", "green",
        "--bold",
        "--align", "center",
        "--width", "50",
        message
    ])
    return success_msg

def display_info(message, color=SECONDARY_COLOR):
    """Display informational message"""
    info, _ = run_command([
        "gum", "style",
        "--foreground", color,
        message
    ])
    return info

def display_code(code, language=""):
    """Display code with syntax highlighting if possible"""
    try:
        # Try to use bat for syntax highlighting
        result = subprocess.run(
            ["bat", "--color=always", "--language=" + language] + (["-"] if not language else []),
            input=code,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            return result.stdout
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    # Fallback to basic styling
    styled, _ = run_command([
        "gum", "style",
        "--foreground", SECONDARY_COLOR,
        code
    ])
    return styled

def get_user_choice(prompt, options):
    """Get user choice from a list of options"""
    print(display_info(prompt, PRIMARY_COLOR))
    result, code = run_command(["gum", "choose"] + options)
    return result, code == 0

def get_user_input(prompt, default="", placeholder=""):
    """Get user input with a prompt"""
    # Display the field prompt with styling
    prompt_display, _ = run_command([
        "gum", "style",
        "--foreground", SECONDARY_COLOR,
        "--bold",
        prompt
    ])
    print(prompt_display)

    # Show default value hint
    if default:
        default_hint, _ = run_command([
            "gum", "style",
            "--foreground", ACCENT_COLOR,
            f"Default: {default} (Press Enter to use default)"
        ])
        print(default_hint)

    placeholder_text = placeholder or f"Enter value (default: {default})" if default else "Enter value"
    value, code = run_command([
        "gum", "input",
        "--placeholder", placeholder_text,
        "--width", "50"
    ])

    # Use default if user provided no input
    if not value and default:
        value = default
        default_used_msg, _ = run_command([
            "gum", "style",
            "--italic",
            "--foreground", ACCENT_COLOR,
            f"Using default: {default}"
        ])
        print(default_used_msg)

    return value, code == 0

def display_separator():
    """Display a separator line"""
    sep, _ = run_command([
        "gum", "style",
        "--foreground", SEPARATOR_COLOR,
        "───────────────────────────────"
    ])
    print(sep)

def display_spinner(message, action_func, *args, **kwargs):
    """Display a spinner while executing a function"""
    # Start the spinner in a subprocess
    spinner_process = subprocess.Popen(
        ["gum", "spin", "--spinner", "dot", "--title", message],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Execute the function
        result = action_func(*args, **kwargs)
        return result
    finally:
        # Make sure spinner is terminated
        if spinner_process.poll() is None:
            spinner_process.terminate()

def display_format_markdown(markdown_text):
    """Display formatted markdown text"""
    formatted, _ = run_command(["gum", "format"], input_text=markdown_text)
    return formatted

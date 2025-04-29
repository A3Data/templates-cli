import os
import yaml
import subprocess
import sys
import json
import tempfile
import shlex

# Define color constants
PRIMARY_COLOR = "yellow"      # Yellow for main elements
SECONDARY_COLOR = "blue"      # Blue for secondary elements
ACCENT_COLOR = "cyan"         # Cyan for highlights
SEPARATOR_COLOR = "240"       # Grey for separators

def run_gum_command(args, input_text=None):
    """Helper function to run gum commands"""
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
    output, _ = run_gum_command([
        "gum", "style", 
        "--foreground", PRIMARY_COLOR, 
        "--border", "rounded", 
        "--border-foreground", PRIMARY_COLOR, 
        "--padding", "0 1", 
        "--align", "center", 
        "--width", "50", 
        text
    ])
    return output

def get_templates():
    """Read templates from templates.yaml file"""
    try:
        with open("templates.yaml", "r") as file:
            data = yaml.safe_load(file)
            return data.get("templates", [])
    except FileNotFoundError:
        error_msg, _ = run_gum_command([
            "gum", "style", 
            "--foreground", "red", 
            "--bold", 
            "Error: templates.yaml file not found"
        ])
        print(error_msg)
        sys.exit(1)
    except yaml.YAMLError as e:
        error_msg, _ = run_gum_command([
            "gum", "style", 
            "--foreground", "red", 
            "--bold", 
            f"Error parsing templates.yaml: {e}"
        ])
        print(error_msg)
        sys.exit(1)

def get_template_options(template_name):
    """Read template options from template config file"""
    template_config_path = f"templates/{template_name}/config.yaml"
    try:
        with open(template_config_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        error_msg, _ = run_gum_command([
            "gum", "style", 
            "--foreground", "red", 
            "--bold", 
            f"Error: Template config file not found: {template_config_path}"
        ])
        print(error_msg)
        sys.exit(1)
    except yaml.YAMLError as e:
        error_msg, _ = run_gum_command([
            "gum", "style", 
            "--foreground", "red", 
            "--bold", 
            f"Error parsing template config: {e}"
        ])
        print(error_msg)
        sys.exit(1)

def select_template(templates):
    """Use gum to select a template from the list"""
    print(display_header("Select a Template"))
    
    # Format template information for display
    template_info = []
    for template in templates:
        name = template["name"]
        desc = template["description"]
        formatted = f"{name} - {desc}"
        template_info.append(formatted)
    
    # Use gum choose for selection experience
    result, code = run_gum_command(["gum", "choose"] + template_info)
    
    if code != 0 or not result:
        msg, _ = run_gum_command([
            "gum", "style", 
            "--foreground", "red", 
            "Template selection canceled"
        ])
        print(msg)
        sys.exit(1)
    
    # Extract template name from the selected option
    selected_template = result.split(" - ")[0]
    
    return selected_template

def collect_inputs(template_options):
    """Collect user inputs based on template options"""
    collected_data = {}
    
    print(display_header("Template Configuration"))
    
    for field_name, field_config in template_options.items():
        field_type = field_config.get("type")
        prompt = field_config.get("prompt", f"Enter {field_name}")
        default = field_config.get("default", "")
        option = field_config.get("option", field_name)
        
        # Display the field prompt with styling
        prompt_display, _ = run_gum_command([
            "gum", "style", 
            "--foreground", SECONDARY_COLOR, 
            "--bold", 
            prompt
        ])
        print(prompt_display)
        
        # Show default value hint
        if default:
            default_hint, _ = run_gum_command([
                "gum", "style",
                "--foreground", ACCENT_COLOR,
                f"Default: {default} (Press Enter to use default)"
            ])
            print(default_hint)
        
        if field_type == "input":
            # Use gum input for text input without pre-filling default value
            value, code = run_gum_command([
                "gum", "input", 
                "--placeholder", f"Enter value (default: {default})", 
                "--width", "50"
            ])
            
            # Use default if user provided no input
            if not value and default:
                value = default
                default_used_msg, _ = run_gum_command([
                    "gum", "style",
                    "--italic",
                    "--foreground", ACCENT_COLOR,
                    f"Using default: {default}"
                ])
                print(default_used_msg)
            
            # Store the value in the correct nested location based on option
            set_nested_value(collected_data, option, value)
            
        elif field_type == "choose":
            choices = field_config.get("choices", [])
            # Use gum choose for selection
            value, code = run_gum_command([
                "gum", "choose"
            ] + choices)
            
            # Use default if user canceled
            if code != 0 and default:
                value = default
                default_used_msg, _ = run_gum_command([
                    "gum", "style",
                    "--italic",
                    "--foreground", ACCENT_COLOR,
                    f"Using default: {default}"
                ])
                print(default_used_msg)
            
            # Convert 'Sim'/'Não' to boolean values for options
            if value == "Sim":
                value = True
            elif value == "Não":
                value = False
            
            # Store the value in the correct nested location based on option
            set_nested_value(collected_data, option, value)
        
        # Add a separator between fields
        sep, _ = run_gum_command([
            "gum", "style", 
            "--foreground", SEPARATOR_COLOR, 
            "───────────────────────────────"
        ])
        print(sep)
    
    return collected_data

def set_nested_value(data_dict, path, value):
    """Set a value in a nested dictionary using dot notation path"""
    keys = path.split('.')
    current = data_dict
    
    # Navigate to the correct nested level, creating dicts as needed
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    # Set the final value
    current[keys[-1]] = value

def display_summary(template_name, collected_data):
    """Display a summary of the collected data"""
    print(display_header("Configuration Summary"))
    
    # Format the nested data as a flattened table for display
    table_data = "| Configuration | Value |\n| --- | --- |\n"
    
    # Recursively add all data to the table
    def add_to_table(data, prefix=""):
        nonlocal table_data
        if isinstance(data, dict):
            for key, value in data.items():
                path = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    add_to_table(value, path)
                else:
                    table_data += f"| {path} | {value} |\n"
        else:
            table_data += f"| {prefix} | {data} |\n"
    
    add_to_table(collected_data)
    
    # Use gum format to display the table
    formatted_table, _ = run_gum_command(["gum", "format"], input_text=table_data)
    print(formatted_table)
    
    # Template info
    template_info, _ = run_gum_command([
        "gum", "style",
        "--foreground", SECONDARY_COLOR,
        f"Template: {template_name}"
    ])
    print(template_info)
    
    # Confirmation step
    print()  # Add some space
    confirm_msg, _ = run_gum_command([
        "gum", "style",
        "--foreground", PRIMARY_COLOR,
        "Do you want to proceed with these settings?"
    ])
    print(confirm_msg)
    
    result, code = run_gum_command([
        "gum", "choose", "Yes", "No"
    ])
    
    if result != "Yes" or code != 0:
        cancel_msg, _ = run_gum_command([
            "gum", "style", 
            "--foreground", "red", 
            "Operation canceled by user"
        ])
        print(cancel_msg)
        sys.exit(1)

def generate_nix_attr_set(data):
    """Convert a dictionary to a Nix attribute set string"""
    result = "{\n"
    
    def format_value(val):
        if isinstance(val, str):
            # Escape quotes in strings
            escaped = val.replace('"', '\\"')
            return f'"{escaped}"'
        elif isinstance(val, bool):
            return "true" if val else "false"
        elif isinstance(val, (int, float)):
            return str(val)
        elif isinstance(val, dict):
            return generate_nix_attr_set(val)
        elif val is None:
            return "null"
        else:
            return f'"{val}"'
    
    # Generate each attribute
    for key, value in data.items():
        if isinstance(value, dict):
            result += f"  {key} = {generate_nix_attr_set(value)};\n"
        else:
            result += f"  {key} = {format_value(value)};\n"
    
    result += "}"
    return result

def run_nix_build(template_name, attr_set):
    """Run nix build command with the given template and attribute set"""
    print(display_header("Building with Nix"))
    
    # Create the Nix expression
    nix_expr = f'''
    with import <nixpkgs> {{}};
    let
      template = builtins.getFlake "github:A3DAndre/demo/a3";
      args = {attr_set};
    in
    template.packages.x86_64-linux.{template_name} args
    '''
    
    # Display the Nix command that will be executed
    build_cmd_str = f"nix build --impure --print-out-paths --expr '{nix_expr}'"
    
    command_display, _ = run_gum_command([
        "gum", "style",
        "--foreground", ACCENT_COLOR,
        "--italic",
        "Running command:"
    ])
    print(command_display)
    
    # Display the command with syntax highlighting if possible
    try:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.nix', delete=False) as tmp:
            tmp.write(build_cmd_str)
            tmp_path = tmp.name
        
        try:
            # Try to use bat for syntax highlighting if available
            syntax_result = subprocess.run(
                ["bat", "--color=always", "--language=sh", tmp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if syntax_result.returncode == 0:
                print(syntax_result.stdout)
            else:
                # Fallback to plain text
                print(build_cmd_str)
        except FileNotFoundError:
            # bat not installed, just print plain text
            print(build_cmd_str)
        
        os.unlink(tmp_path)
    except Exception:
        # Something went wrong, just print the plain command
        print(build_cmd_str)
    
    # Create a loading spinner
    spinner_msg = "Building project... This may take a while"
    # Start the spinner in a subprocess
    spinner_process = subprocess.Popen(
        ["gum", "spin", "--spinner", "dot", "--title", spinner_msg],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Run the Nix build command
        build_result = subprocess.run(
            ["nix", "build", "--impure", "--print-out-paths", "--expr", nix_expr],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Stop the spinner
        spinner_process.terminate()
        
        if build_result.returncode == 0:
            output_path = build_result.stdout.strip()
            
            success_msg, _ = run_gum_command([
                "gum", "style",
                "--foreground", "green",
                "--bold",
                "--align", "center",
                "--width", "50",
                "✓ Build completed successfully!"
            ])
            print(success_msg)
            
            path_msg, _ = run_gum_command([
                "gum", "style",
                "--foreground", SECONDARY_COLOR,
                f"Output path: {output_path}"
            ])
            print(path_msg)
            
            return output_path
        else:
            error_msg, _ = run_gum_command([
                "gum", "style",
                "--foreground", "red",
                "--bold",
                "❌ Build failed!"
            ])
            print(error_msg)
            
            if build_result.stderr:
                # Display error details
                print(display_header("Error Details"))
                error_details, _ = run_gum_command([
                    "gum", "style",
                    "--foreground", "red",
                    build_result.stderr
                ])
                print(error_details)
            
            return None
    finally:
        # Make sure spinner is terminated
        if spinner_process.poll() is None:
            spinner_process.terminate()

def format_nix_attr_for_display(attr_set):
    """Format the Nix attribute set for display with syntax highlighting"""
    # Try to highlight the Nix attribute set with syntax highlighting
    try:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.nix', delete=False) as tmp:
            tmp.write(f"# Nix attribute set\n{attr_set}")
            tmp_path = tmp.name
        
        try:
            # Try to use bat for syntax highlighting
            result = subprocess.run(
                ["bat", "--color=always", "--language=nix", tmp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            os.unlink(tmp_path)
            
            if result.returncode == 0:
                return result.stdout
            else:
                # Fallback to plain text
                return attr_set
        except FileNotFoundError:
            # bat not installed, use gum to add some basic styling
            os.unlink(tmp_path)
            styled_output, _ = run_gum_command([
                "gum", "style",
                "--foreground", SECONDARY_COLOR,
                attr_set
            ])
            return styled_output
    except Exception:
        # If anything goes wrong, just return the plain text
        return attr_set

def main():
    # Show welcome message
    print(display_header("Template CLI"))
    
    # Get available templates
    templates = get_templates()
    
    # Display templates and let user select one
    selected_template = select_template(templates)
    
    # Show selection confirmation
    template_selected_msg, _ = run_gum_command([
        "gum", "style", 
        "--foreground", PRIMARY_COLOR, 
        f"Selected template: {selected_template}"
    ])
    print(template_selected_msg)
    
    # Get options for the selected template
    template_options = get_template_options(selected_template)
    
    # Collect inputs based on template options
    collected_data = collect_inputs(template_options)
    
    # Display summary and confirmation
    display_summary(selected_template, collected_data)
    
    # Generate Nix attribute set
    nix_attr_set = generate_nix_attr_set(collected_data)
    
    # Show the resulting Nix attribute set
    print(display_header("Generated Nix Configuration"))
    formatted_nix = format_nix_attr_for_display(nix_attr_set)
    print(formatted_nix)
    
    # Ask for confirmation before building
    confirm_msg, _ = run_gum_command([
        "gum", "style",
        "--foreground", PRIMARY_COLOR,
        "Do you want to build with this configuration?"
    ])
    print(confirm_msg)
    
    result, code = run_gum_command([
        "gum", "choose", "Yes", "No"
    ])
    
    if result == "Yes":
        # Run the Nix build
        output_path = run_nix_build(selected_template, nix_attr_set)
        
        if output_path:
            # Save the configuration for future reference
            config_file = f"{selected_template}_config.json"
            with open(config_file, "w") as f:
                json.dump(collected_data, f, indent=2)
            
            file_saved_msg, _ = run_gum_command([
                "gum", "style",
                "--foreground", SECONDARY_COLOR,
                f"Configuration saved to {config_file}"
            ])
            print(file_saved_msg)
    else:
        cancel_msg, _ = run_gum_command([
            "gum", "style", 
            "--foreground", "red", 
            "Build canceled by user"
        ])
        print(cancel_msg)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# cli.py
import sys

# Import our modules
from utils import ui
from utils import nix
from utils import templates


def collect_inputs(template_options):
    """Collect user inputs based on template options"""
    collected_data = {}

    print(ui.display_header("Template Configuration"))

    for field_name, field_config in template_options.items():
        field_type = field_config.get("type")
        prompt = field_config.get("prompt", f"Enter {field_name}")
        default = field_config.get("default", "")
        option = field_config.get("option", field_name)

        if field_type == "input":
            value, success = ui.get_user_input(prompt, default)
            if success:
                templates.set_nested_value(collected_data, option, value)

        elif field_type == "choose":
            choices = field_config.get("choices", [])
            value, success = ui.get_user_choice(prompt, choices)

            if success:
                # Convert 'Sim'/'Não' to boolean values for options
                if value == "Sim":
                    value = True
                elif value == "Não":
                    value = False

                templates.set_nested_value(collected_data, option, value)
            elif default:
                # Use default if user canceled
                value = default
                print(ui.display_info(f"Using default: {default}", ui.ACCENT_COLOR))
                templates.set_nested_value(collected_data, option, value)

        ui.display_separator()

    return collected_data


def display_summary(template_name, collected_data):
    """Display a summary of the collected data"""
    print(ui.display_header("Configuration Summary"))

    # Generate markdown table
    table_md = templates.generate_config_markdown_table(collected_data)

    # Display the table
    print(ui.display_format_markdown(table_md))

    # Template info
    print(ui.display_info(f"Template: {template_name}"))

    # Confirmation step
    print()  # Add some space
    result, success = ui.get_user_choice(
        "Do you want to proceed with these settings?", ["Yes", "No"]
    )

    if result != "Yes" or not success:
        ui.display_error("Operation canceled by user")
        sys.exit(1)


def build_project(template_name, attr_set):
    """Build the project using Nix"""
    print(ui.display_header("Building with Nix"))

    # Create the Nix expression
    nix_expr = nix.create_nix_expression(template_name, attr_set)

    # Display the Nix command that will be executed
    build_cmd_str = nix.format_nix_command(nix_expr)

    print(ui.display_info("Running command:", ui.ACCENT_COLOR))
    print(ui.display_code(build_cmd_str, "sh"))

    # Run the Nix build with a spinner
    def do_build():
        return nix.run_nix_build(nix_expr)

    build_result = ui.display_spinner(
        "Building project... This may take a while", do_build
    )

    if build_result["success"]:
        output_path = build_result["output_path"]

        print(ui.display_success("✓ Build completed successfully!"))
        print(ui.display_info(f"Output path: {output_path}"))

        return output_path

    ui.display_error("❌ Build failed!")

    if build_result["stderr"]:
        # Display error details
        print(ui.display_header("Error Details"))
        print(ui.display_info(build_result["stderr"], "red"))

    return None


def main():
    #     title = """
    #        db         ad888888b,     888888888888                                          88
    #       d88b       d8"     "88          88                                               88                ,d
    #      d8'`8b              a8P          88                                               88                88
    #     d8'  `8b          aad8"           88   ,adPPYba,  88,dPYba,,adPYba,   8b,dPPYba,   88  ,adPPYYba,  MM88MMM  ,adPPYba,  ,adPPYba,
    #    d8YaaaaY8b         ""Y8,           88  a8P_____88  88P'   "88"    "8a  88P'    "8a  88  ""     `Y8    88    a8P_____88  I8[    ""
    #   d8aaa""a""8b           "8b          88  8PP"a"a"a"  88      88      88  88       d8  88  ,adPPPPP88    88    8PP""e""e"   `"Y8ba,
    #  d8'        `8b  Y8,     a88          88  "8b,   ,aa  88      88      88  88b,   ,a8"  88  88,    ,88    88,   "8b,   ,aa  aa    ]8I
    # d8'          `8b  "Y888888P'          88   `"Ybbd8"'  88      88      88  88`YbbdP"'   88  `"8bbdP"Y8    "Y888  `"Ybbd8"'  `"YbbdP"'
    # """

    #     title = """
    #       .o.         .oooo.        ooooooooooooo                                        oooo                .
    #      .888.      .dP""Y88b       8'   888   `8                                        `888              .o8
    #     .8"888.           ]8P'           888       .ooooo.  ooo. .oo.  .oo.   oo.ooooo.   888   .oooo.   .o888oo  .ooooo.   .oooo.o
    #    .8' `888.        <88b.            888      d88' `88b `888P"Y88bP"Y88b   888' `88b  888  `P  )88b    888   d88' `88b d88(  "8
    #   .88ooo8888.        `88b.           888      888ooo888  888   888   888   888   888  888   .oP"888    888   888ooo888 `"Y88b.
    #  .8'     `888.  o.   .88P            888      888    .o  888   888   888   888   888  888  d8(  888    888 . 888    .o o.  )88b
    # o88o     o8888o `8bd88P'            o888o     `Y8bod8P' o888o o888o o888o  888bod8P' o888o `Y888""8o   "888" `Y8bod8P' 8""888P'
    #                                                                            888
    #                                                                           o888o
    #     """

    title = """
     _    _____   _____                    _       _
    / \\  |___ /  |_   _|__ _ __ ___  _ __ | | __ _| |_ ___  ___
   / _ \\   |_ \\    | |/ _ \\ '_ ` _ \\| '_ \\| |/ _` | __/ _ \\/ __|
  / ___ \\ ___) |   | |  __/ | | | | | |_) | | (_| | ||  __/\\__ |
 /_/   \\_\\____/    |_|\\___|_| |_| |_| .__/|_|\\__,_|\\__\\___||___/
                                    |_|
"""

    #     title = """
    #  _____  _____    ____  _____  __  __  _____  ____   _____  ____  _____  _____
    # /  _  \/  _  \  /    \/   __\/  \/  \/  _  \/  _/  /  _  \/    \/   __\/  ___>
    # |  _  |>-<_  <  \-  -/|   __||  \/  ||   __/|  |---|  _  |\-  -/|   __||___  |
    # \__|__/\_____/   |__| \_____/\__ \__/\__/   \_____/\__|__/ |__| \_____/<_____/
    # """
    # Show welcome message
    # print(ui.display_header(title))
    print(title)

    # Get available templates with a spinner
    def fetch_templates():
        return templates.get_templates()

    templates_data = ui.display_spinner("Loading templates...", fetch_templates)

    if isinstance(templates_data, tuple):
        # Error occurred
        ui.display_error(templates_data[1])
        sys.exit(1)

    # Extract template information for display
    template_info = []
    for template in templates_data:
        name = template["name"]
        desc = template["description"]
        formatted = f"{name} - {desc}"
        template_info.append(formatted)

    # Display templates and let user select one
    print(ui.display_header("Select a Template"))
    selected_option, success = ui.get_user_choice("Choose a template:", template_info)

    if not success or not selected_option:
        ui.display_error("Template selection canceled")
        sys.exit(1)

    # Extract template name from the selected option
    selected_template = selected_option.split(" - ")[0]

    # Show selection confirmation
    print(ui.display_info(f"Selected template: {selected_template}", ui.PRIMARY_COLOR))

    # Get options for the selected template with a spinner
    def fetch_template_options():
        return templates.get_template_options(selected_template)

    template_options, error = ui.display_spinner(
        f"Loading template options for {selected_template}...", fetch_template_options
    )

    if error:
        ui.display_error(error)
        sys.exit(1)

    # Collect inputs based on template options
    collected_data = collect_inputs(template_options)

    # Display summary and confirmation
    display_summary(selected_template, collected_data)

    # Generate Nix attribute set
    nix_attr_set = nix.generate_nix_attr_set(collected_data)

    # Show the resulting Nix attribute set
    print(ui.display_header("Generated Nix Configuration"))
    print(ui.display_code(nix_attr_set, "nix"))

    # Ask for confirmation before building
    result, success = ui.get_user_choice(
        "Do you want to build with this configuration?", ["Yes", "No"]
    )

    if result == "Yes" and success:
        # Run the Nix build
        output_path = build_project(selected_template, nix_attr_set)

        if output_path:
            # Save the configuration for future reference
            print(output_path)
    else:
        ui.display_error("Build canceled by user")


if __name__ == "__main__":
    main()

from typing import Dict, Any
from cookiecutter.main import cookiecutter
import json
# import yaml
from utils.template.abs import TemplateConfig, TemplateClass
import utils.ui as ui

class CookiecutterTemplate(TemplateClass):
    def __init__(self, config: TemplateConfig):
        super().__init__(config)

    def collect_inputs(self) -> str:
        """Collect inputs from the selected template and return as JSON string to be used in the build process"""
        ui.display_header("Template Configuration")
        raw_config = self._fetch_template_options()
        if not raw_config:
            raise ValueError("Failed to load template configuration")
        collected_data =  ui.collect_template_inputs(raw_config)
        return json.dumps(collected_data)

    def build(self, config: str, output_dir: str) -> None:
        """Build the cookiecutter template"""
        try:
            options = json.loads(config)
            cookiecutter(
                f"gh:{self.config.organization}/{self.config.repository}",
                no_input=True,
                extra_context=options,
                output_dir=output_dir,
                checkout=self.config.branch,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to build template: {str(e)}")

    

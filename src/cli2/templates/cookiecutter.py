import json
from cookiecutter.main import cookiecutter
from .abs import TemplateConfig, TemplateClass

class CookiecutterTemplate(TemplateClass):
    def __init__(self, config: TemplateConfig):
        super().__init__(config)

    def build(self, output_dir: str) -> None:
        """Build the cookiecutter template"""
        try:
            # options = json.loads(config)
            # no_input = options != {}
            cookiecutter(
                f"gh:{self.config.organization}/{self.config.repository}",
                no_input=False,
                # extra_context=options,
                output_dir=output_dir,
                checkout=self.config.branch,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to build template: {str(e)}")
    
    def is_available(self):
        return True

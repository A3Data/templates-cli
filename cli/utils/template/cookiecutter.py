import json
from cookiecutter.main import cookiecutter
from utils.template.abs import TemplateConfig, TemplateClass

class CookiecutterTemplate(TemplateClass):
    def __init__(self, config: TemplateConfig):
        super().__init__(config)

    def encode_input(self,collected_data) -> str:
        """Encodes the collected data into a JSON string to be used by cookiecutter like cookiecutter.json"""
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

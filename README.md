# CLI para Geração de Templates

Este projeto é uma ferramenta de linha de comando (CLI) para geração de templates, projetada para facilitar a criação de estruturas de projetos reutilizáveis. A CLI suporta dois tipos principais de templates: **Cookiecutter** e **Nix**, permitindo flexibilidade e personalização para diferentes cenários.

## Instalação

Para instalar a CLI, execute o seguinte comando:
```bash
pip install git+https://github.com/A3Data/templates-cli.git
```

## Autenticação no GitHub

Para acessar repositórios privados de templates, é necessário autenticar-se no GitHub. Recomenda-se utilizar o [GitHub CLI (`gh`)](https://cli.github.com/):

No ubunto vc pode instalar pelo apt

```bash
sudo apt install gh
```
```bash
gh auth login
```

Siga as instruções para autenticar sua conta. Após isso, a CLI poderá acessar os repositórios necessários.

## Templates Disponíveis

Abaixo estão os templates atualmente suportados pela CLI, conforme configurado no arquivo templates.yaml:
1. batch - Batch processing template <https://github.com/A3Data/templates-eml/tree/batch>
2. lambda - AWS Lambda template <https://github.com/A3Data/templates-eml/tree/lambda>
3. buora-oficial - Buora Oficial Templates <https://github.com/A3Data/buora-oficial-templates/tree/main>
4. buora_infra - Buora Oficial Infra <https://github.com/A3Data/buora_infra/tree/template/cookiecutter>
5. ubq-data-infra - Ubique Data Infra <https://github.com/A3Data/data-infrastructure/tree/cookiecutter>
6. ubq-data-image - Ubique Data Image <https://github.com/A3Data/data-image/tree/cookiecutteer>
7. ubq-data-pipeline - Ubique Data Pipeline <https://github.com/A3Data/data-pipeline/tree/cookiecutter>
## Como Usar

Após instalar a CLI, você pode executar o comando principal para iniciar a ferramenta:
```bash
a3t
```
Siga as instruções interativas para selecionar um template e configurar seu projeto.

Também é necessario ter acesso aos repositorios dos templates para poder gerar eles usando a cli, caso vc não tenha acesso entre em contato com a equipe de soluções e inovação da A3 Data


## Outra documentação

1. [Criando Templates](./docs/CREATING_TEMPLATES.md)

2. [Desenvolvimento e Contribuição para a cli](./docs/DEVELOPMENT.md)
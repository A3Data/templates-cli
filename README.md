# CLI para Geração de Templates

Este projeto é uma ferramenta de linha de comando (CLI) para geração de templates, projetada para facilitar a criação de estruturas de projetos reutilizáveis. A CLI suporta dois tipos principais de templates: **Cookiecutter** e **Nix**, permitindo flexibilidade e personalização para diferentes cenários.

## Instalação

Para instalar a CLI, execute o seguinte comando:
```bash
pip install git+https://github.com/A3DAndre/templates-cli.git
```
## Templates Disponíveis

Abaixo estão os templates atualmente suportados pela CLI, conforme configurado no arquivo templates.yaml:

### Templates Cookiecutter

1. batch-cookie  
   Descrição: Template para processamento em batch.  
   Organização: A3DAndre  
   Repositório: template-batch  
   Branch: main  
   Caminho de Configuração: cookiecutter.yaml  

2. lambda-cookie  
   Descrição: Template para projetos AWS Lambda.  
   Organização: A3DAndre  
   Repositório: template-lambda  
   Branch: main  
   Caminho de Configuração: cookiecutter.yaml  

3. buora-cookie  
   Descrição: Template para projetos Buora.  
   Organização: A3DAndre  
   Repositório: template-buora  
   Branch: main  
   Caminho de Configuração: cookiecutter.yaml  

### Templates Nix

1. poc  
   Descrição: Template para projetos de prova de conceito (Proof of Concept).  
   Organização: A3DAndre  
   Repositório: demo  
   Branch: main  
   Caminho de Configuração: templates/poc/config.yaml  

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
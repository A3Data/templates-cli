# Guia de Desenvolvimento

## Estrutura do Projeto

Todo codigo da cli se encontra na pasta src no seguinte formato

```
cli/              # Diretório principal do projeto
├── cli.py        # Ponto de entrada da aplicação
├── utils/        # Utilitários e funções auxiliares
│   ├── template/ # Template Builders
│   └── ui.py
└── pyproject.toml # Configuração do Poetry e dependências
```

## Ambiente de Desenvolvimento

### Usando devenv (Recomendado)

1. [Instale o Nix](https://github.com/DeterminateSystems/nix-installer):
```bash
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | \
  sh -s -- install
```

2. Instable o devenv 
```bash
nix-shell -p devenv # para instalar temporariamente na shell atual

# ou para instalar usando nix-env
# se vc usar flakes:
nix-env -iA nixpkgs.devenv
# se não flakes:
nix profile install nixpkgs#devenv # se vc usou o instalador do passo 1 utilize essa opção
```
2. Habilite o ambiente de desenvolvimento:
```bash
devenv shell # automaticamente configura python o poetry e as dependencias do projeto, assim como os git hooks
```

O arquivo `devenv.nix` já está configurado com:
- Python e Poetry
- Pre-commit hooks (ruff e ruff-format)
- Pacotes necessários (git, python, poetry, ...)


Rodando a cli localmente
```bash
python -m src.cli.cli
```

Ou atravez do atalho do devenv
```bash
cli
```


### Usando Poetry (Alternativa)

Se preferir não usar o devenv, você pode usar o Poetry diretamente:

1. Instale o Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Configure o ambiente virtual:
```bash
poetry install
```

3. Ative o ambiente virtual:
```bash
poetry shell
```

## Templates

Para criar novos templates, consulte o arquivo [CREATING_TEMPLATES.md](CREATING_TEMPLATES.md).

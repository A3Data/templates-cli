# Guia de Criação de Templates

Este guia explica como criar e gerenciar templates no sistema templates-cli. Templates são estruturas de projeto reutilizáveis que ajudam a manter consistência e melhores práticas em diferentes projetos.

## Estrutura Geral

Os templates devem seguir uma estrutura consistente para garantir compatibilidade com o sistema de templates. Cada template deve incluir:

- Um projeto no github contendo os arquivos do template
- Arquivos de configuração para o construtor de template escolhido (Nix ou Cookiecutter)
- Documentação explicando o propósito e uso do template
- Quaisquer scripts ou utilitários necessários
- Arquivos de configuração padrão e exemplos

## Tipos de Template

Atualmente, o sistema suporta dois tipos de construtores de templates:

1. Templates Cookiecutter
2. Templates baseados em Nix


### Arquivo de Configuração do Template

Um arquivo .yaml será usado para configurar o template, ele deve seguir o seguinte formato:

```yaml
stringOptionName:
  type: string
  prompt: "Qual é o nome do projeto?"
  default: "Demo da daily de título pro README"
  option: "stringOptionName" # opcional para opções nix

# retornará um array com todas as opções selecionadas
listCheckboxOptionName:
  type: checkbox
  prompt: "Exemplo de um prompt de lista checkbox"
  default: ["Opção 1"]
  option: "options.listCheckboxOptionName" # opcional para opção nix
  list:
    - "Opção 1"
    - "Opção 2"
    - "Opção 3"

# retornará apenas a opção selecionada como uma string
listOptionName:
  type: radio
  prompt: "Exemplo de um prompt radio"
  default: "Opção 1"
  option: "options.listOptionName" # opcional para opções nix
  list:
    - "Opção 1"
    - "Opção 2"
    - "Opção 3"

# retornará verdadeiro ou falso
booleanOptionName:
  type: boolean
  prompt: "Exemplo de um prompt booleano?"
  default: "false"
  option: "options.booleanOptionName" # opcional para opções nix
```


### Templates Cookiecutter

Templates Cookiecutter são mais flexíveis e focam na estruturação de projetos. Eles são ideais quando:

- Você precisa de renderização dinâmica de templates
- Seu projeto requer entrada do usuário durante a criação
- Você quer manter múltiplas variações de uma estrutura de projeto

Para criar um template Cookiecutter:

1. Crie um arquivo `cookiecutter.yaml` com variáveis padrão, perguntas personalizadas que serão usadas para configurar o template via CLI
2. Opcionalmente crie um `cookiecutter.json` para ser usado com o cookiecutter vanilla
3. Estruture seu template usando sintaxe Jinja2 para conteúdo dinâmico
4. Adicione hooks para etapas de pré/pós geração, se necessário

Exemplo de estrutura para um template Cookiecutter:
```
template/
├── cookiecutter.json
├── cookiecutter.yaml
├── hooks/
│   ├── pre_gen_project.py
│   └── post_gen_project.py
└── {{cookiecutter.project_name}}/
    └── ... (arquivos específicos do projeto)
```

### Templates baseados em Nix

TODO:



## Adicionar template na cli

Para adicionar o template na cli é necessario adicionar as informações do repositorio assim como a localização do arquivo de [configuração templates.yaml](../templates.yaml) na raiz desse repsitorio

## Melhores Práticas

1. **Documentação**: Sempre inclua:
   - Arquivo README explicando o uso do template
   - Requisitos e pré-requisitos
   - Opções de configuração
   - Exemplos do resultado gerado

2. **Testes**:
   - Teste a geração do template com diferentes entradas
   - Verifique se os projetos gerados funcionam como esperado
   - Inclua configurações de exemplo

3. **Manutenção**:
   - Mantenha as dependências atualizadas
   - Documente mudanças que quebram compatibilidade
   - Mantenha compatibilidade retroativa quando possível

4. **Configuração**:
   - Use padrões sensatos
   - Documente todas as opções de configuração
   - Inclua configurações de exemplo

## Validação de Template

Antes de enviar um novo template:

1. Teste o processo de geração do template
2. Verifique se todos os scripts e ferramentas funcionam no projeto gerado
3. Verifique se a documentação está completa e precisa
4. Garanta que o template segue os padrões de codificação do projeto

## Exemplos

Você pode encontrar templates de exemplo no diretório `output/` deste projeto. Estes servem como implementações de referência e pontos de partida para novos templates.
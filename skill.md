# Skill do Projeto: Padrões de Desenvolvimento e Engenharia

Este documento define as diretrizes, ferramentas, padrões de código e comandos obrigatórios para o desenvolvimento deste projeto. Ele serve como guia de instrução para desenvolvedores e agentes de Inteligência Artificial que operem nesta base de código.

---

## 1. Visão Geral e Princípios
- **Linguagem Principal:** Python 3.12+
- **Foco:** Qualidade de código, automação de testes, padronização e documentação contínua.
- **Diretório de Código-fonte:** `src/`
- **Diretório de Testes:** `tests/`
- **Diretório de Documentação:** `docs/`

---

## 2. Gerenciamento de Versão do Python (`pyenv`)
O versionamento do Python deve ser controlado via **pyenv** para garantir consistência entre ambientes de desenvolvimento e CI/CD.

- **Definir versão local do projeto:**
  ```bash
  pyenv local 3.12.10
  ```
- **Verificar versão ativa:**
  ```bash
  pyenv which python
  python --version
  ```
- O arquivo `.python-version` na raiz do repositório deve ser versionado e respeitado.

---

## 3. Gerenciamento de Dependências e Ambiente Virtual (`poetry`)
Todo o ciclo de vida de dependências e ambientes virtuais deve ser gerenciado exclusivamente através do **Poetry**.

### Configuração do Ambiente Virtual
- O Poetry deve criar o ambiente virtual (`.venv`) obrigatoriamente dentro da pasta raiz do projeto:
  ```bash
  poetry config virtualenvs.in-project true
  ```

### Instalação de Dependências
- Criar/sincronizar o ambiente e instalar todas as dependências:
  ```bash
  poetry install
  ```
- Adicionar dependência de produção:
  ```bash
  poetry add <nome-do-pacote>
  ```
- Adicionar dependência de desenvolvimento:
  ```bash
  poetry add --group dev <nome-do-pacote>
  ```

### Execução de Comandos
- Todo comando, script ou ferramenta CLI deve ser executado obrigatoriamente dentro do contexto do Poetry:
  ```bash
  poetry run <comando>
  ```
- Ou ativando o ambiente virtual:
  ```bash
  source .venv/bin/activate
  ```

---

## 4. Linting, Formatação e Qualidade de Código (`ruff`)
O **Ruff** é a ferramenta padrão e única para análise estática de código (linter) e formatação (formatter).

### Regras
- O código deve seguir a **PEP 8** e ter tipagem estática (Type Hints).
- Imports devem ser ordenados automaticamente (compatível com isort).
- Nenhuma alteração pode ser submetida com violações de lint.

### Comandos Obrigatórios
- **Verificar problemas de linting e corrigir automaticamente os seguros:**
  ```bash
  poetry run ruff check . --fix
  ```
- **Formatar todo o código do projeto:**
  ```bash
  poetry run ruff format .
  ```
- **Checagem estrita para CI/validação:**
  ```bash
  poetry run ruff check .
  poetry run ruff format --check .
  ```

---

## 5. Testes Unitários e Cobertura Mínima (`pytest` + `pytest-cov`)
A suíte de testes deve utilizar **pytest** e monitorar a cobertura com **pytest-cov**.

### Requisito Mandatório de Cobertura
- **Meta de Cobertura:** É **obrigatório** cobrir no mínimo **50%** de todo o código localizado dentro do diretório `src/`.
- Qualquer nova funcionalidade ou refatoração deve ser acompanhada de testes unitários que mantenham ou aumentem essa métrica.

### Comandos de Teste
- **Executar testes simples:**
  ```bash
  poetry run pytest
  ```
- **Executar testes com relatório e validação de cobertura mínima de 50%:**
  ```bash
  poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=50
  ```
- **Gerar relatório HTML de cobertura (opcional):**
  ```bash
  poetry run pytest --cov=src --cov-report=html
  ```

---

## 6. Documentação do Projeto (`mkdocs-material`)
A documentação do projeto é gerada estaticamente com **MkDocs** utilizando o tema **Material for MkDocs**.

### Estrutura Esperada
```text
├── mkdocs.yml          # Arquivo central de configuração
└── docs/
    ├── index.md        # Página inicial da documentação
    └── ...             # Guias, referências e páginas adicionais
```

### Comandos de Documentação
- **Iniciar servidor de desenvolvimento local (live reload):**
  ```bash
  poetry run mkdocs serve
  ```
- **Construir a versão de produção (arquivos estáticos):**
  ```bash
  poetry run mkdocs build
  ```
- **Publicar no GitHub Pages (se configurado):**
  ```bash
  poetry run mkdocs gh-deploy
  ```

---

## 7. Tabela Rápida de Comandos para IA / Desenvolvedor

| Ação | Ferramenta | Comando |
| :--- | :--- | :--- |
| Setar versão Python | `pyenv` | `pyenv local 3.12.10` |
| Configurar `.venv` local | `poetry` | `poetry config virtualenvs.in-project true` |
| Instalar dependências | `poetry` | `poetry install` |
| Adicionar pacote dev | `poetry` | `poetry add --group dev <pacote>` |
| Verificar e corrigir lint | `ruff` | `poetry run ruff check . --fix` |
| Formatar código | `ruff` | `poetry run ruff format .` |
| Rodar testes (min 50% cov) | `pytest` | `poetry run pytest --cov=src --cov-fail-under=50` |
| Servidor de documentação | `mkdocs` | `poetry run mkdocs serve` |
| Build da documentação | `mkdocs` | `poetry run mkdocs build` |

---

## 8. Checklist de Validação para o Agente de IA
Sempre que concluir uma alteração no código ou criar um novo módulo:
1. [ ] Certificar-se de que os pacotes foram instalados via `poetry`.
2. [ ] Executar `poetry run ruff check . --fix` e garantir 0 erros de lint.
3. [ ] Executar `poetry run ruff format .` para formatação consistente.
4. [ ] Escrever/atualizar testes em `tests/`.
5. [ ] Executar `poetry run pytest --cov=src --cov-fail-under=50` e confirmar que a cobertura mínima de 50% foi atingida.
6. [ ] Atualizar ou criar a documentação correspondente em `docs/` se houver nova funcionalidade.


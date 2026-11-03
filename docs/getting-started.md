# Guia de Início Rápido (Getting Started)

Este guia orienta a configuração do ambiente de desenvolvimento e a execução do projeto seguindo estritamente as regras da **`skill.md`**.

---

## 1. Pré-requisitos

- **pyenv** para gerenciar a versão do Python.
- **Poetry** (>= 2.0) instalado no sistema.

---

## 2. Configuração do Python com `pyenv`

Fixe a versão do Python no repositório:

```bash
pyenv local 3.12.10
python --version
```

A saída esperada deve ser `Python 3.12.x`.

---

## 3. Instalação do Ambiente com `Poetry`

Configure o Poetry para criar o ambiente virtual `.venv` na raiz do projeto e instale todas as dependências:

```bash
poetry config virtualenvs.in-project true
poetry install
```

---

## 4. Executando o Dashboard Streamlit

Para iniciar o dashboard localmente:

```bash
poetry run streamlit run src/app.py
```

O dashboard será aberto no navegador padrão através da URL `http://localhost:8501`.

---

## 5. Qualidade de Código (Lint e Format)

Verifique e formate o código utilizando o **Ruff**:

```bash
# Verificar e corrigir violações de lint
poetry run ruff check . --fix

# Formatar o código
poetry run ruff format .
```

---

## 6. Execução de Testes e Cobertura

Execute a suíte de testes unitários garantindo a cobertura mínima mandatória de 50% em `src/`:

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=50
```

---

## 7. Servidor de Documentação

Inicie o servidor de documentação com *live reload*:

```bash
poetry run mkdocs serve
# ou: poetry run task docs
```

Para gerar a compilação estática de produção:

```bash
poetry run task docs_build
```

---

## 8. Tabela de Atalhos Taskipy

| Comando | Descrição |
| :--- | :--- |
| `poetry run task test` | Executa a suíte de testes com cobertura mínima de 50% |
| `poetry run task lint` | Checa linting e formatação com Ruff |
| `poetry run task format` | Formata o código e corrige violações com Ruff |
| `poetry run task docs` | Inicia o servidor local do MkDocs com live-reload |
| `poetry run task docs_build` | Valida build estrito da documentação |
| `poetry run task run` | Inicia a aplicação Streamlit |

---

## 9. Pipeline de CI no GitHub Actions

O repositório possui integração contínua automatizada em `.github/workflows/ci.yml`.

A cada `push` ou `pull request` direcionado à branch `main` ou `master`, os seguintes jobs são executados em paralelo:

1. **`lint` (Ruff):** Validação estrita de lint e conformidade de formatação.
2. **`test` (Pytest):** Execução de todos os testes unitários e barreira de cobertura mínima (>= 50%), seguido de smoke test do Streamlit.
3. **`docs` (MkDocs):** Build estrito da documentação técnica para prevenir links quebrados e falhas estruturais.

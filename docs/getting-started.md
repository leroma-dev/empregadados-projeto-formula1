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
```

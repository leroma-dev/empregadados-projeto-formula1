# OpenF1 Analytics & Interactive Dashboard 🏎️

[![CI Pipeline](https://github.com/leroma-dev/empregadados-projeto-formula1/actions/workflows/ci.yml/badge.svg)](https://github.com/leroma-dev/empregadados-projeto-formula1/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12.10-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/packaging-poetry-cyan.svg)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Coverage](https://img.shields.io/badge/coverage-%3E%3D50%25-green.svg)](https://pytest-cov.readthedocs.io/)
[![Documentation](https://img.shields.io/badge/docs-MkDocs%20Material-red.svg)](https://squidfunk.github.io/mkdocs-material/)

Aplicação analítica e dashboard interativo em Python para extração, validação tipada, análise estatística e visualização gráfica de dados históricos e em tempo real da Fórmula 1 (temporadas de 2023 em diante), consumindo os dados oficiais fornecidos pela **OpenF1 API**.

---

## 🚀 Funcionalidades Principais

- **Cliente HTTP OpenF1 Resiliente:** Integração completa respeitando o limite do *Community Tier* (3 req/s e 30 req/min), retries com *exponential backoff* e cache em memória.
- **Modelagem Tipada com Pydantic v2:** Schemas fortemente validados para GPs, Sessões, Pilotos, Voltas, Stints de Pneus, Telemetria e Clima.
- **Métricas Analíticas:**
  - Identificação de volta mais rápida geral e por piloto.
  - Setores ideais (S1, S2, S3) e ritmo de corrida (*race pace*).
  - Análise de degradação e linha do tempo de estratégia de pneus.
  - Comparativo direto entre companheiros de equipe (*teammate battle*).
- **Dashboard Streamlit Interativo:**
  - **Visão Geral:** KPIs, classificação oficial com cores das escuderias e gráfico de posições ganhas/perdidas em relação ao grid de largada.
  - **Ritmo e Voltas:** Evolução temporal dos tempos de volta por piloto e timeline de stints.
  - **Telemetria Comparativa:** Gráficos sincronizados curva a curva de velocidade, acelerador e freio com alinhamento por distância no circuito.
- **Documentação Técnica Completa:** Portal com Material for MkDocs.

---

## 🛠️ Tecnologias e Padrões (Conforme `skill.md`)

- **Python:** `3.12.10` gerenciado via `pyenv`
- **Dependências & Ambiente Virtual:** `Poetry` (com `.venv` na raiz)
- **Frontend / Dashboard:** `Streamlit` e `Plotly`
- **Validação de Dados:** `Pydantic v2`
- **Qualidade de Código:** `Ruff` (Linter & Formatter unificados)
- **Testes & Cobertura:** `Pytest` e `pytest-cov` (cobertura mínima de 50% em `src/`)
- **Documentação:** `MkDocs Material`

---

## 🏁 Instalação e Execução

### 1. Configurar Versão do Python
```bash
pyenv local 3.12.10
python --version
```

### 2. Instalar Dependências no `.venv`
```bash
poetry config virtualenvs.in-project true
poetry install
```

### 3. Iniciar o Dashboard Streamlit
```bash
poetry run task run
# ou: poetry run streamlit run src/app.py
```

### 4. Executar Testes Unitários e Checagem de Cobertura (Min 50%)
```bash
poetry run task test
# ou: poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=50
```

### 5. Linting e Formatação com Ruff
```bash
poetry run task lint    # Checagem estrita de lint e formatação
poetry run task format  # Correção e formatação automática
```

### 6. Documentação Técnica
```bash
# Iniciar servidor local com live-reload:
poetry run task docs
# ou: poetry run mkdocs serve

# Gerar build estático de produção:
poetry run task docs_build
# ou: poetry run mkdocs build --strict
```

### 7. Comandos de Automação (Taskipy Cheat Sheet)
| Comando | Ação Executada |
| :--- | :--- |
| `poetry run task test` | Executa testes com pytest e barreira de cobertura de 50% |
| `poetry run task lint` | Checa linting e conformidade de formatação com Ruff |
| `poetry run task format` | Formata todo o código e corrige violações com Ruff |
| `poetry run task docs` | Inicia o servidor local do MkDocs com live-reload |
| `poetry run task docs_build` | Compila o build estático estrito da documentação |
| `poetry run task run` | Inicia o dashboard interativo Streamlit |
| `poetry run task pre-commit` | Executa todos os hooks de pre-commit manualmente |

### 8. Pre-commit (Hooks Locais)

Os hooks de pre-commit garantem qualidade de código em **cada commit** antes de chegar ao repositório remoto.

```bash
# Instalar os hooks no repositório local (necessário uma única vez):
poetry run pre-commit install

# Executar todos os hooks manualmente em todos os arquivos:
poetry run task pre-commit
# ou: poetry run pre-commit run --all-files

# Atualizar todos os hooks para as versões mais recentes:
poetry run pre-commit autoupdate
```

**Hooks configurados em [`.pre-commit-config.yaml`](.pre-commit-config.yaml):**
- **Ruff Lint** (`ruff`): lint automático com correção (`--fix`).
- **Ruff Format** (`ruff-format`): formatação automática de código.
- **Trailing whitespace**: remove espaços em branco no fim das linhas.
- **End of file fixer**: garante que arquivos terminam com newline.
- **YAML / TOML validation**: valida sintaxe de arquivos de configuração.
- **Merge conflict check**: detecta markers de conflito esquecidos.
- **Large files**: bloqueia arquivos acima de 1 MB.
- **Debug statements**: impede commits com `pdb`, `breakpoint()`, etc.

---

## 🔄 Pipeline de Integração Contínua (CI/CD)

O projeto possui uma esteira automatizada no **GitHub Actions** configurada em `.github/workflows/ci.yml`. A pipeline é disparada a cada `push` e `pull request` nas branches `main` e `master`, além de permitir execução manual via `workflow_dispatch`.

A esteira executa 3 jobs paralelos e isolados com cache de dependências Poetry:

1. **Lint & Code Formatting (`lint`):**
   - Valida tipagem estática e conformidade com a PEP 8 via `poetry run task lint`.
   - Executa checagem de formatação e ordenação de imports com Ruff.
2. **Unit Tests & Coverage (`test`):**
   - Executa toda a suíte de testes unitários com mocks via `poetry run task test`.
   - Aplica a barreira de falha mandatória de **cobertura mínima de 50%** em `src/` (`pytest-cov`).
   - Executa *smoke test* de inicialização do ponto de entrada do Streamlit (`src/app.py`).
3. **Documentation Build (`docs`):**
   - Valida compilação estrita da documentação técnica via `poetry run task docs_build` (`mkdocs build --strict`).
   - Garante ausência de links quebrados, avisos ou inconsistências no MkDocs.

---

## 📂 Estrutura do Projeto

```text
.
├── .github/                      # Workflows do GitHub Actions
│   └── workflows/
│       └── ci.yml                # Pipeline automatizada de CI
├── .python-version               # Versão do Python fixada (3.12.10)
├── pyproject.toml                # Dependências e configurações de ferramentas
├── mkdocs.yml                    # Configuração da documentação MkDocs
├── README.md                     # Visão geral do projeto
├── doc_api.md                    # Documentação resumida da OpenF1 API
├── skill.md                      # Diretrizes e regras de engenharia obrigatórias
├── plan.md                       # Plano arquitetural e de implementação
├── docs/                         # Documentação técnica estática
├── src/                          # Código-fonte da aplicação
│   ├── app.py                    # Ponto de entrada do Streamlit
│   ├── client/                   # Cliente HTTP, RateLimiter e endpoints OpenF1
│   ├── models/                   # Schemas tipados Pydantic v2
│   ├── services/                 # Regras de negócio e cálculos estatísticos
│   ├── components/               # Componentes visuais e gráficos Plotly
│   └── views/                    # Páginas e abas do Dashboard
└── tests/                        # Testes unitários com pytest
```

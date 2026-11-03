# Skill do Projeto: Padrões de Desenvolvimento e Engenharia

Este documento define as diretrizes, tecnologias, padrões de código e comandos obrigatórios para o desenvolvimento deste projeto. Ele serve como guia operacional e mandatório tanto para desenvolvedores quanto para assistentes de Inteligência Artificial.

---

## 1. Visão Geral e Arquitetura
- **Linguagem:** Python 3.12+ (gerenciado via `pyenv`)
- **Gerenciador de Dependências & Ambiente:** Poetry
- **Interface e Apresentação (Frontend/Dashboard):** Streamlit
- **Qualidade de Código (Lint & Format):** Ruff
- **Testes Unitários e Cobertura:** Pytest (`pytest-cov` com mínimo de 50% de cobertura em `src/`)
- **Documentação Técnica:** MkDocs com tema Material (`mkdocs-material`)

### Estrutura Padrão de Diretórios
```text
.
├── .python-version       # Versão do Python fixada pelo pyenv
├── pyproject.toml        # Configuração do projeto e dependências (Poetry)
├── skill.md              # Guia de padrões e regras operacionais
├── doc_api.md            # Documentação dos endpoints da API
├── plan.md               # Planejamento das fases do projeto
├── docs/                 # Documentação técnica em Markdown (MkDocs)
│   └── index.md
├── mkdocs.yml            # Configuração do MkDocs Material
├── src/                  # Código-fonte da aplicação e dashboards
│   ├── app.py            # Ponto de entrada do dashboard Streamlit
│   └── ...
└── tests/                # Testes unitários com pytest
    └── ...
```

---

## 2. Gerenciamento de Versão do Python (`pyenv`)
A versão do Python deve ser rigorosamente padronizada utilizando o **pyenv**, garantindo paridade entre o ambiente de desenvolvimento e produção.

- **Definir versão local do projeto:**
  ```bash
  pyenv local 3.12.10
  ```
- **Verificar versão ativa:**
  ```bash
  pyenv which python
  python --version
  ```
- O arquivo `.python-version` gerado na raiz deve ser sempre mantido e respeitado.

---

## 3. Gerenciamento de Dependências e Ambiente Virtual (`poetry`)
Todas as dependências e o ambiente virtual devem ser gerenciados **exclusivamente através do Poetry**.

### Configuração do Ambiente Virtual (`.venv`)
- O ambiente virtual deve obrigatoriamente residir dentro da pasta raiz do projeto:
  ```bash
  poetry config virtualenvs.in-project true
  ```

### Instalação de Pacotes
- Criar/sincronizar o ambiente e instalar todas as dependências:
  ```bash
  poetry install
  ```
- Adicionar dependência de produção:
  ```bash
  poetry add <pacote>
  ```
- Adicionar dependência de desenvolvimento:
  ```bash
  poetry add --group dev <pacote>
  ```

### Regra de Execução de Comandos
- **Nenhum comando Python ou ferramenta CLI deve ser executado fora da venv.**
- Use sempre o prefixo `poetry run`:
  ```bash
  poetry run <comando>
  ```
- Ou ative a venv antes de executar:
  ```bash
  source .venv/bin/activate
  ```

---

## 4. Camada de Apresentação e Visualização (`streamlit`)
O **Streamlit** é o framework padrão para construção de dashboards interativos e visualização de dados da Fórmula 1.

### Diretrizes de Implementação
- O ponto de entrada da aplicação Streamlit deve estar localizado em `src/` (ex: `src/app.py` ou `src/main.py`).
- Separe lógica de negócio/consumo de APIs das páginas visuais e componentes do Streamlit.
- Utilize cache (`@st.cache_data` / `@st.cache_resource`) para chamadas a APIs e processamento pesado.

### Comandos de Execução
- **Executar a aplicação Streamlit:**
  ```bash
  poetry run streamlit run src/app.py
  ```
- **Executar com recarga automática e porta customizada:**
  ```bash
  poetry run streamlit run src/app.py --server.port 8501 --server.runOnSave true
  ```

---

## 5. Qualidade de Código, Linting e Formatação (`ruff`)
O **Ruff** é o linter e formatador de código único e obrigatório do projeto.

### Regras
- Código deve seguir as convenções da **PEP 8** e possuir tipagem estática (*Type Hints*).
- Imports devem ser ordenados automaticamente (estilo `isort`).
- Nenhuma alteração pode ser submetida com violações de lint pendentes.

### Comandos Obrigatórios
- **Verificar problemas de linting e aplicar correções automáticas:**
  ```bash
  poetry run ruff check . --fix
  ```
- **Formatar todo o código do projeto:**
  ```bash
  poetry run ruff format .
  ```
- **Modo estrito para validação/CI (sem alterar arquivos):**
  ```bash
  poetry run ruff check .
  poetry run ruff format --check .
  ```

---

## 6. Testes Unitários e Cobertura Mínima (`pytest` + `pytest-cov`)
A suíte de testes deve utilizar **pytest** com o plugin **pytest-cov** para monitoramento de cobertura.

### Requisito Mandatório de Cobertura
- **Meta de Cobertura Mínima:** É **obrigatório** cobrir no mínimo **50%** de todo o código localizado em `src/`.
- A execução dos testes deve falhar automaticamente caso a cobertura fique abaixo de 50%.
- Funções utilitárias, clientes de API e lógica de processamento de dados devem possuir testes com mocks adequados.

### Comandos de Testes
- **Executar testes e validar cobertura mínima de 50%:**
  ```bash
  poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=50
  ```
- **Executar suíte rápida de testes:**
  ```bash
  poetry run pytest
  ```
- **Gerar relatório HTML de cobertura:**
  ```bash
  poetry run pytest --cov=src --cov-report=html
  ```

---

## 7. Documentação Técnica (`mkdocs-material`)
A documentação do projeto é gerada estaticamente com o **MkDocs** utilizando o tema **Material for MkDocs**.

### Estrutura
- Arquivo central de configuração: `mkdocs.yml` na raiz do repositório.
- Documentos técnicos e guias em formato Markdown: pasta `docs/`.

### Comandos de Documentação
- **Iniciar servidor de desenvolvimento local (Live Preview):**
  ```bash
  poetry run mkdocs serve
  ```
- **Construir arquivos estáticos para produção:**
  ```bash
  poetry run mkdocs build
  ```
- **Publicar no GitHub Pages (se aplicável):**
  ```bash
  poetry run mkdocs gh-deploy
  ```

---

## 8. Tabela Rápida de Comandos (CLI Cheat Sheet)

| Categoria | Ação | Ferramenta | Comando |
| :--- | :--- | :--- | :--- |
| **Python** | Fixar versão local | `pyenv` | `pyenv local 3.12.10` |
| **Ambiente** | Criar `.venv` no projeto | `poetry` | `poetry config virtualenvs.in-project true` |
| **Ambiente** | Instalar dependências | `poetry` | `poetry install` |
| **Ambiente** | Adicionar dependência prod | `poetry` | `poetry add <pacote>` |
| **Ambiente** | Adicionar dependência dev | `poetry` | `poetry add --group dev <pacote>` |
| **Frontend** | Iniciar app Streamlit | `taskipy` / `streamlit` | `poetry run task run` (ou `poetry run streamlit run src/app.py`) |
| **Qualidade** | Checar e validar lint | `taskipy` / `ruff` | `poetry run task lint` (ou `poetry run ruff check .`) |
| **Qualidade** | Formatar código | `taskipy` / `ruff` | `poetry run task format` (ou `poetry run ruff format .`) |
| **Testes** | Testar com cobertura (min 50%) | `taskipy` / `pytest` | `poetry run task test` (ou `poetry run pytest --cov=src ...`) |
| **Docs** | Servidor de documentação | `taskipy` / `mkdocs` | `poetry run task docs` (ou `poetry run mkdocs serve`) |
| **Docs** | Gerar build dos docs | `taskipy` / `mkdocs` | `poetry run task docs_build` (ou `poetry run mkdocs build`) |

---

## 9. Checklist de Validação (Definition of Done)
Antes de finalizar qualquer tarefa, submeter commits ou aprovar pull requests, execute e valide o seguinte checklist:

1. [x] **Ambiente:** Dependências instaladas e atualizadas no `.venv` via `poetry`.
2. [x] **Lint:** `poetry run ruff check . --fix` executado com zero advertências/erros.
3. [x] **Formatação:** `poetry run ruff format .` executado para padronização.
4. [x] **Testes & Cobertura:** `poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=50` com 100% de testes passando e cobertura em `src/` >= 50%.
5. [x] **Frontend:** Streamlit inicializando sem erros (`poetry run streamlit run ...`).
6. [x] **Documentação:** Páginas e guias em `docs/` atualizados e build validado (`poetry run mkdocs build`).

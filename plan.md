# Plano de Desenvolvimento do Projeto Fórmula 1 (`plan.md`)

Este documento estabelece o plano arquitetural, de engenharia e operacional para a construção do projeto **empregadados-projeto-formula1**. O planejamento foi estruturado a partir da união das especificações técnicas da **OpenF1 API** ([`doc_api.md`](doc_api.md)) com as regras de governança, padrões de código e ferramentas obrigatórias definidas na [**`skill.md`**](skill.md).

---

## 1. Visão Geral e Objetivos do Projeto

### 1.1. Propósito
Desenvolver uma aplicação analítica e dashboard interativo em Python para extração, validação, análise estatística e visualização de dados históricos e em tempo real da Fórmula 1 (temporadas de 2023 em diante), consumindo os dados oficiais fornecidos pela **OpenF1 API**.

### 1.2. Principais Entregáveis
1. **Cliente HTTP OpenF1 Resiliente:**
   - Módulo robusto para consumo da OpenF1 API respeitando os limites estritos do *Community Tier* (máximo de 3 req/s e 30 req/min).
   - Suporte a retries com *exponential backoff*, tratamento de erros (HTTP 429, timeouts) e cache em memória.
   - Suporte nativo a operadores (`=`, `<`, `<=`, `>`, `>=`) e parâmetro `latest`.
2. **Modelagem de Dados e Tipagem Estrita (Pydantic v2):**
   - Schemas fortemente tipados para validar dados retornados da API (GPs, sessões, pilotos, voltas, telemetria, paradas de box, stints de pneus e clima).
3. **Camada de Serviços e Métricas:**
   - Agregação hierárquica (`meetings` ➔ `sessions` ➔ `drivers`, `laps`, `stints`, `pit`).
   - Cálculo de estatísticas essenciais: volta mais rápida, ritmo de corrida (*race pace*), degradação e estratégia de pneus, deltas entre companheiros de equipe e telemetria comparativa.
4. **Dashboard Interativo em Streamlit:**
   - Interface web moderna para visualização de dados, gráficos de telemetria (velocidade, RPM, aceleração, freio, marcha), comparações de voltas e linha do tempo de stints de pneus.
   - Caching eficiente com `@st.cache_data` e `@st.cache_resource` para não esgotar as cotas de requisição da API.
5. **Documentação Técnica Completa (MkDocs Material):**
   - Portal estático com guia de início rápido, arquitetura do sistema, referência do cliente OpenF1 e guia do dashboard.
6. **Qualidade e Cobertura Contínua:**
   - Conformidade absoluta com a `skill.md`: linter/formatter `ruff`, tipagem estática e testes unitários com cobertura mínima mandatória de **50%** em `src/` via `pytest` e `pytest-cov`.

---

## 2. Tecnologias e Padrões Obrigatórios (Conforme `skill.md`)

| Pilar | Tecnologia / Ferramenta | Padrão / Diretriz Operacional |
| :--- | :--- | :--- |
| **Versão Python** | Python 3.12.10 | Fixado via `pyenv local 3.12.10` e mantido em `.python-version`. |
| **Gerenciador de Dependências** | Poetry (>= 2.0) | `.venv` isolado na raiz (`poetry config virtualenvs.in-project true`). |
| **Interface / Dashboard** | Streamlit | Ponto de entrada em `src/app.py`, uso de `@st.cache_data` e componentes visuais desacoplados. |
| **Qualidade de Código** | Ruff | PEP 8, Type Hints, imports ordenados (`ruff check . --fix` e `ruff format .`). |
| **Testes e Cobertura** | Pytest + Pytest-cov | Cobertura mínima de **50%** em `src/` (`--cov-fail-under=50`) com mocks das chamadas HTTP. |
| **Documentação Técnica** | MkDocs + Material | Documentação em `docs/` com configuração em `mkdocs.yml`. |
| **Cliente HTTP** | `httpx` / `requests` | Timeout configurado, headers limpos e lógica de rate limiting. |
| **Validação de Dados** | `pydantic` (v2) | Schemas de dados estritos com validação em tempo de execução. |
| **Visualização de Dados** | `plotly` / `pandas` | Gráficos interativos de telemetria, tempos de volta e stints. |

---

## 3. Arquitetura da Solução e Estrutura de Diretórios

O projeto adota uma arquitetura em camadas modular e desacoplada, separando o consumo de rede, regras de negócio e interface de apresentação:

```text
empregadados-projeto-formula1/
├── .python-version               # Versão do Python fixada (3.12.10)
├── pyproject.toml                # Dependências, configurações do Ruff, Pytest e Poetry
├── poetry.lock                   # Lockfile de versões determinísticas
├── mkdocs.yml                    # Configuração da documentação MkDocs Material
├── README.md                     # Visão geral e guia rápido do projeto
├── doc_api.md                    # Especificação resumida da OpenF1 API
├── skill.md                      # Regras, padrões de engenharia e governança
├── plan.md                       # Este plano de execução
│
├── docs/                         # Documentação técnica estática (MkDocs)
│   ├── index.md                  # Apresentação do projeto e badges
│   ├── getting-started.md        # Instalação com pyenv e poetry
│   ├── architecture.md           # Desenho da arquitetura e fluxo de dados
│   ├── api-client.md             # Uso e métodos do cliente OpenF1
│   └── dashboard.md              # Guia de uso do Dashboard Streamlit
│
├── src/                          # Código-fonte da aplicação
│   ├── __init__.py
│   ├── app.py                    # Ponto de entrada da aplicação Streamlit
│   │
│   ├── client/                   # Camada de integração com a OpenF1 API
│   │   ├── __init__.py
│   │   ├── base.py               # Cliente HTTP base com Rate Limiter e Retries
│   │   ├── endpoints.py          # Métodos específicos para cada endpoint da OpenF1
│   │   └── exceptions.py         # Exceções personalizadas (RateLimitError, APIError)
│   │
│   ├── models/                   # Schemas e validação tipada (Pydantic v2)
│   │   ├── __init__.py
│   │   ├── meeting.py            # Schemas de Grande Prêmio e circuito
│   │   ├── session.py            # Schemas de sessões (Treino, Quali, Corrida)
│   │   ├── driver.py             # Schemas de pilotos e equipes
│   │   ├── lap.py                # Schemas de voltas e tempos de setor
│   │   ├── stint.py              # Schemas de stints e compostos de pneus
│   │   ├── telemetry.py          # Schemas de telemetria (car_data, speed, rpm)
│   │   └── result.py             # Schemas de resultado e classificação final
│   │
│   ├── services/                 # Lógica de negócio e cálculos analíticos
│   │   ├── __init__.py
│   │   ├── session_service.py    # Consolidação hierárquica dos dados de sessão
│   │   ├── stats_service.py      # Cálculos estatísticos (voltas rápidas, médias, deltas)
│   │   └── telemetry_service.py  # Processamento e alinhamento de telemetria
│   │
│   ├── components/               # Componentes reutilizáveis para Streamlit
│   │   ├── __init__.py
│   │   ├── sidebar.py            # Seletores de ano, GP, sessão e pilotos
│   │   ├── kpis.py               # Cards de métricas rápidas (tempo da pole, vencedor, etc.)
│   │   └── charts.py             # Gráficos Plotly (telemetria, tempos de volta, stints)
│   │
│   └── views/                    # Páginas e abas do Dashboard Streamlit
│       ├── __init__.py
│       ├── session_overview.py   # Resumo da sessão e classificação
│       ├── lap_analysis.py       # Comparativo de voltas e ritmo
│       └── telemetry_view.py     # Análise de telemetria curva a curva
│
└── tests/                        # Suíte de testes unitários com pytest
    ├── __init__.py
    ├── conftest.py               # Fixtures compartilhadas e mocks de respostas JSON
    ├── test_client.py            # Testes do cliente HTTP, rate limit e retries
    ├── test_models.py            # Testes de parsing e validação Pydantic
    ├── test_services.py          # Testes de regras de negócio e métricas
    └── test_components.py        # Testes de componentes utilitários e formatação
```

---

## 4. Estratégia de Integração com a OpenF1 API (`doc_api.md`)

### 4.1. Hierarquia de Chamadas
O fluxo de extração seguirá a ordem recomendada pela documentação oficial:

```
[1] /meetings (Localizar meeting_key filtrando por ano ou nome)
       │
       ▼
[2] /sessions (Obter session_key da Corrida, Quali ou Treino)
       │
       ├───────────────────┬───────────────────┬───────────────────┐
       ▼                   ▼                   ▼                   ▼
   /drivers              /laps               /pit               /stints
(Lista e cores)    (Voltas e tempos)     (Paradas no box)   (Estratégia pneus)
       │                   │
       ▼                   ▼
/session_result       /car_data (Telemetria)
 (Classificação)    (Filtrado por piloto e volta)
```

### 4.2. Tratamento do Rate Limit do Community Tier
- **Regras da API:** Máximo de 3 requisições por segundo e 30 por minuto.
- **Implementação no Cliente (`src/client/base.py`):**
  1. **Token Bucket / Leaky Bucket:** Limitador interno em memória que controla as chamadas para não exceder 3 req/s e 30 req/min.
  2. **Throttling Automático:** Intervalo mínimo de 0,35s entre requisições consecutivas.
  3. **Backoff Exponencial:** Interceptador que trata respostas HTTP 429 aguardando com jitter antes de tentar novamente.
  4. **Camada de Cache do Streamlit:** Chamadas com parâmetros imutáveis (sessões passadas) utilizam `@st.cache_data(ttl=3600)` para eliminar requisições redundantes.

### 4.3. Filtros e Operadores Especiais
- O cliente suportará passagem transparente de operadores (`<`, `>`, `<=`, `>=`) com devida codificação de URL (`%3C`, `%3E`, etc.).
- Suporte nativo ao identificador especial `latest` para sessões recentes.

---

## 5. Fases de Execução do Projeto (Roadmap)

### Fase 1: Setup do Ambiente e Governança Base
- [ ] **1.1. Ajuste de Versão Python e pyproject.toml:**
  - Fixar versão com `pyenv local 3.12.10` e gerar/validar `.python-version`.
  - Corrigir o campo `requires-python` no `pyproject.toml` para `"^3.12"` (substituindo o atual `>=3.15`).
- [ ] **1.2. Configuração do Poetry e Instalação de Dependências:**
  - Garantir venv no projeto: `poetry config virtualenvs.in-project true`.
  - Adicionar dependências de produção:
    ```bash
    poetry add httpx pydantic pandas plotly streamlit
    ```
  - Adicionar dependências de desenvolvimento:
    ```bash
    poetry add --group dev ruff pytest pytest-cov pytest-mock mkdocs mkdocs-material
    ```
- [ ] **1.3. Configuração de Ruff e Pytest no `pyproject.toml`:**
  - Configurar `tool.ruff` (line-length 88, regras E, F, I, UP, etc.).
  - Configurar `tool.pytest.ini_options` e `tool.coverage` com barreira mínima de 50%.

---

### Fase 2: Cliente HTTP OpenF1 com Rate Limiting (`src/client/`)
- [ ] **2.1. Implementar Módulo de Exceções (`exceptions.py`):**
  - `OpenF1Error`, `RateLimitExceededError`, `ResourceNotFoundError`, `SessionNotFoundError`.
- [ ] **2.2. Implementar `RateLimiter` e Cliente Base (`base.py`):**
  - Implementar mecanismo de controle de taxa (3 req/s e 30 req/min).
  - Implementar método genérico `_get(endpoint, params)` com timeout e retry automático para HTTP 429.
- [ ] **2.3. Implementar Endpoints Específicos (`endpoints.py`):**
  - `get_meetings(year, meeting_key, country_name)`
  - `get_sessions(meeting_key, session_name, session_key)`
  - `get_drivers(session_key, driver_number)`
  - `get_laps(session_key, driver_number, lap_number)`
  - `get_pit_stops(session_key, driver_number)`
  - `get_stints(session_key, driver_number)`
  - `get_session_results(session_key, position)`
  - `get_weather(session_key)`
  - `get_car_data(session_key, driver_number, ...)`
- [ ] **2.4. Testes Unitários com Mocks (`tests/test_client.py`):**
  - Cobrir cenários de sucesso, erro de status code e ativação de rate limit (sem bater na API real).

---

### Fase 3: Modelagem e Validação Tipada (`src/models/`)
- [ ] **3.1. Criar Schemas Pydantic v2:**
  - `Meeting`: informações do evento, país, circuito e ano.
  - `Session`: detalhes da sessão (nome, tipo, data/hora).
  - `Driver`: número, sigla, nome completo, equipe, cor hex da equipe.
  - `Lap`: número da volta, duração total, setores S1/S2/S3, velocidades `st_speed` e flag de pit.
  - `Stint`: número do stint, composto (`SOFT`, `MEDIUM`, `HARD`, etc.), voltas percorridas.
  - `CarData`: telemetria de alta frequência (velocidade, RPM, acelerador, freio, marcha, DRS).
  - `SessionResult`: posição de largada, posição de chegada, pontos, status.
- [ ] **3.2. Testes dos Modelos (`tests/test_models.py`):**
  - Validação de payload JSON típico da OpenF1, campos opcionais/nulos e conversão de tipos.

---

### Fase 4: Serviços Analíticos e Agregações (`src/services/`)
- [ ] **4.1. `SessionService`:**
  - Métodos para extrair visão consolidada de um GP (sessão, grid, resultados e tempos).
- [ ] **4.2. `StatsService`:**
  - Identificação de volta mais rápida da sessão.
  - Média de tempo por stint e análise de consistência de ritmo.
  - Ganho/perda de posições em relação ao grid de largada.
- [ ] **4.3. `TelemetryService`:**
  - Processamento e interpolação de dados de telemetria de duas voltas para comparação gráfica direta (ex: comparação de volta rápida de dois pilotos rivais).
- [ ] **4.4. Testes dos Serviços (`tests/test_services.py`):**
  - Testes com datasets simulados cobrindo os cálculos estatísticos e regras de negócio.

---

### Fase 5: Dashboard Interativo em Streamlit (`src/app.py`, `components/`, `views/`)
- [ ] **5.1. Ponto de Entrada (`src/app.py`):**
  - Configuração de página (`st.set_page_config`), layout amplo (*wide*) e tema escuro personalizado com identidade F1.
  - Gerenciamento de estado e navegação entre visões.
- [ ] **5.2. Componentes de UI (`src/components/`):**
  - `sidebar.py`: Seleção encadeada de Temporada (Ano) ➔ GP (Meeting) ➔ Sessão (Quali/Race) ➔ Pilotos.
  - `kpis.py`: Métricas de destaque (Vencedor, Volta mais rápida, Temperatura de pista, Segurança na pista).
  - `charts.py`:
    - Gráfico de evolução de posições volta a volta.
    - Gráfico comparativo de voltas (Delta lap time).
    - Gráfico de estratégia de pneus (Timeline de compostos por volta).
    - Gráfico interativo de telemetria curva a curva (Velocidade x Distância/Tempo, Aceleração e Freio).
- [ ] **5.3. Páginas/Visões do Dashboard (`src/views/`):**
  - `session_overview.py`: Tabela de classificação com cores das equipes, gaps e pontos.
  - `lap_analysis.py`: Matriz de tempos, distribuição de voltas e consistência de stints.
  - `telemetry_view.py`: Comparativo lado a lado de telemetria entre dois pilotos.
- [ ] **5.4. Estratégia de Caching:**
  - Aplicar `@st.cache_data` com TTL em todas as funções de serviço e consulta à API.

---

### Fase 6: Documentação Técnica com MkDocs Material (`docs/` e `mkdocs.yml`)
- [ ] **6.1. Configuração do MkDocs (`mkdocs.yml`):**
  - Ativar tema `material` com paleta de cores F1 (primária vermelha, fundo escuro).
  - Configurar navegação, busca em português/inglês e extensões markdown.
- [ ] **6.2. Elaboração das Páginas em `docs/`:**
  - `index.md`: Apresentação geral, objetivos e screenshots do dashboard.
  - `getting-started.md`: Como clonar, instalar dependências (`poetry install`) e rodar.
  - `architecture.md`: Diagrama de componentes e integração com a OpenF1.
  - `api-client.md`: Como usar o cliente Python de forma independente.
  - `dashboard.md`: Guia de navegação no Streamlit.
- [ ] **6.3. Validação do Build:**
  - Executar `poetry run mkdocs build --strict` sem avisos ou links quebrados.

---

### Fase 7: Homologação Final de Qualidade e Cobertura (DoD)
- [ ] **7.1. Linting e Formatação Estrita:**
  - Executar `poetry run ruff check . --fix`.
  - Executar `poetry run ruff format .`.
  - Garantir zero alertas pendentes.
- [ ] **7.2. Validação da Cobertura de Testes (Mínimo 50%):**
  - Executar `poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=50`.
  - Garantir 100% dos testes passando e cobertura >= 50% em `src/`.
- [ ] **7.3. Teste de Inicialização do Streamlit:**
  - Executar `poetry run streamlit run src/app.py` garantindo inicialização limpa.

---

## 6. Critérios de Aceite (Definition of Done - DoD)

Uma tarefa ou fase do projeto só é considerada **concluída** após a validação do seguinte checklist:

1. [ ] **Ambiente:** Todas as dependências gerenciadas estritamente pelo Poetry dentro do `.venv`.
2. [ ] **Tipagem e Lint:** Código 100% tipado com *Type Hints*, validado com sucesso por `poetry run ruff check .`.
3. [ ] **Formatação:** Código formatado via `poetry run ruff format .`.
4. [ ] **Testes e Cobertura:** Suíte executada via `poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=50` com taxa de aprovação de 100% e cobertura em `src/` **>= 50%**.
5. [ ] **Dashboard Streamlit:** Aplicação Streamlit inicializando sem erros ou quebras de tela.
6. [ ] **Documentação:** Build estático do MkDocs compilado sem erros (`poetry run mkdocs build`).

---

## 7. Tabela Rápida de Comandos Operacionais (CLI Cheat Sheet)

| Categoria | Ação Desejada | Comando Obrigatório |
| :--- | :--- | :--- |
| **Python** | Fixar versão local do Python | `pyenv local 3.12.10` |
| **Ambiente** | Garantir `.venv` dentro do projeto | `poetry config virtualenvs.in-project true` |
| **Ambiente** | Instalar/atualizar dependências | `poetry install` |
| **Ambiente** | Adicionar pacote de produção | `poetry add <pacote>` |
| **Ambiente** | Adicionar pacote de desenvolvimento | `poetry add --group dev <pacote>` |
| **Frontend** | Iniciar Dashboard Streamlit | `poetry run streamlit run src/app.py` |
| **Qualidade** | Checar e corrigir lint com Ruff | `poetry run ruff check . --fix` |
| **Qualidade** | Formatar código com Ruff | `poetry run ruff format .` |
| **Testes** | Rodar testes com barreira de cobertura (min 50%) | `poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=50` |
| **Docs** | Iniciar servidor de documentação | `poetry run mkdocs serve` |
| **Docs** | Gerar build de produção dos docs | `poetry run mkdocs build` |

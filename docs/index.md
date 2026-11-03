# OpenF1 Analytics & Dashboard 🏎️

[![CI Pipeline](https://github.com/leroma-dev/empregadados-projeto-formula1/actions/workflows/ci.yml/badge.svg)](https://github.com/leroma-dev/empregadados-projeto-formula1/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12.10-blue.svg)](https://www.python.org/downloads/)
[![Coverage](https://img.shields.io/badge/coverage-%3E%3D50%25-green.svg)](https://pytest-cov.readthedocs.io/)

Bem-vindo à documentação oficial do projeto **OpenF1 Analytics & Dashboard**. Esta aplicação foi desenvolvida para extração, validação tipada, processamento estatístico e visualização interativa de dados históricos e em tempo real da Fórmula 1 (temporadas de 2023 em diante), utilizando a **OpenF1 API**.

---

## 🚀 Principais Funcionalidades

- **Cliente HTTP Resiliente:** Consumo da OpenF1 API com controle estrito de *rate limit* (3 req/s e 30 req/min), *exponential backoff* e cache inteligente.
- **Modelagem Tipada com Pydantic v2:** Schemas fortemente validados para Grandes Prêmios, Sessões, Pilotos, Voltas, Stints de Pneus, Telemetria e Clima.
- **Métricas e Estatísticas Avançadas:** Identificação de volta mais rápida geral e por piloto, melhores parciais de setor (S1, S2, S3), cálculo de ritmo de corrida (*race pace*) e duelo entre companheiros de equipe.
- **Dashboard Interativo em Streamlit:** Interface visual com tema escuro e identidade visual da F1, gráficos Plotly curva a curva e linha do tempo de estratégia de pneus.
- **Governança Estrita de Engenharia:** Conformidade total com a `skill.md`, linter e formatador `ruff`, e cobertura de testes unitários com barreira mínima de 50% via `pytest` e `pytest-cov`.

---

## 🛠️ Pilares Tecnológicos

| Ferramenta | Finalidade |
| :--- | :--- |
| **Python 3.12** | Linguagem base fixada via `.python-version` |
| **Poetry** | Gerenciador determinístico de dependências e ambiente `.venv` |
| **Streamlit** | Interface do usuário e dashboard analítico |
| **Plotly** | Visualizações e gráficos interativos |
| **Pydantic v2** | Validação de schemas e dados em tempo de execução |
| **HTTPX** | Cliente HTTP moderno com suporte a timeout e retries |
| **Ruff** | Linter e formatador de código único de altíssima velocidade |
| **Pytest + Pytest-cov** | Suíte de testes automatizados com cobertura garantida |
| **MkDocs Material** | Geração desta documentação técnica |
| **GitHub Actions** | Pipeline automatizada de Integração Contínua (CI) |


# Cliente OpenF1 (`src/client/`)

O módulo `src/client/` fornece uma biblioteca cliente completa em Python para comunicação com a **OpenF1 API**, projetada especificamente para operar com segurança nos limites do *Community Tier*.

---

## 1. Exemplo de Uso Rápido

```python
from src.client import OpenF1Client

# Instanciando o cliente
client = OpenF1Client()

# Consultando Grandes Prêmios de 2024
meetings = client.get_meetings(year=2024)
print(f"Total de GPs encontrados: {len(meetings)}")

# Consultando sessões do GP mais recente
if meetings:
    latest_gp = meetings[-1]
    sessions = client.get_sessions(meeting_key=latest_gp["meeting_key"])
    for s in sessions:
        print(f"Sessão: {s['session_name']} (Chave: {s['session_key']})")

client.close()
```

---

## 2. Controle de Taxa (*Rate Limiter*)

O plano gratuito da OpenF1 impõe:
- Máximo de **3 requisições por segundo**.
- Máximo de **30 requisições por minuto**.

A classe `RateLimiter` em `src/client/base.py` gerencia essas cotas através de filas deslizantes em memória de forma *thread-safe*:

```python
from src.client.base import RateLimiter

limiter = RateLimiter(
    max_per_second=3,
    max_per_minute=30,
    min_interval_seconds=0.35,
)

# Antes de qualquer chamada HTTP:
limiter.acquire()
```

---

## 3. Retries e Tolerância a Falhas

Caso a API retorne o código `HTTP 429 Too Many Requests`, o cliente intercepta a resposta e aplica *exponential backoff* com *jitter*, respeitando o cabeçalho `Retry-After` quando enviado pelo servidor.

---

## 4. Endpoints Suportados

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `get_meetings(...)` | `/meetings` | GPs e eventos do calendário |
| `get_sessions(...)` | `/sessions` | Sessões (Treinos, Quali, Corrida) |
| `get_drivers(...)` | `/drivers` | Pilotos participantes e equipes |
| `get_laps(...)` | `/laps` | Tempos de volta e setores S1, S2, S3 |
| `get_car_data(...)` | `/car_data` | Telemetria bruta (velocidade, rpm, aceleração) |
| `get_location(...)` | `/location` | Coordenadas 3D (X, Y, Z) no circuito |
| `get_pit_stops(...)` | `/pit` | Duração e voltas de paradas no box |
| `get_stints(...)` | `/stints` | Estratégia e compostos de pneus |
| `get_session_results(...)` | `/session_result` | Classificação e pontuação oficial |
| `get_weather(...)` | `/weather` | Temperatura da pista/ar e chuva |
| `get_team_radio(...)` | `/team_radio` | Links de áudios das equipes |

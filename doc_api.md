# Documentação Resumida da OpenF1 API

> **Fonte Oficial:** [https://openf1.org/docs/](https://openf1.org/docs/)  
> **Base URL:** `https://api.openf1.org/v1`

---

## 1. Visão Geral

A **OpenF1** é uma API aberta e comunitária que disponibiliza dados históricos e em tempo real sobre a Fórmula 1 (dados a partir da temporada de **2023** em diante). Os dados incluem telemetria de alta frequência dos carros, rádio de equipe, tempos de volta, paradas de box, mensagens da direção de prova e meteorologia.

### Características Principais
* **Acesso Livre (Community Tier):** Não requer autenticação nem chave de API (API Key) para dados históricos.
* **Formatos Suportados:** `JSON` (padrão) e `CSV` (adicionando `?csv=true`).
* **Streaming / Ao Vivo (Sponsor Tier):** Sessões ao vivo via REST em tempo real, WebSockets ou MQTT requerem token de patrocinador.
* **Rate Limits (Plano Gratuito):**
  * Máximo de **3 requisições por segundo**
  * Máximo de **30 requisições por minuto**

---

## 2. Parâmetros de Filtro e Operadores

A OpenF1 **não** utiliza paginação convencional (`page`, `offset`, `limit`). O controle do volume de dados é feito por meio de parâmetros de consulta (Query Parameters).

### Operadores de Comparação
Para campos numéricos e temporais, é possível usar operadores de comparação diretamente na URL:

| Operador | Significado | URL Encoded (Recomendado) | Exemplo de Uso |
| :---: | :---: | :---: | :--- |
| `=` | Igual a | `=` | `driver_number=1` |
| `<` | Menor que | `%3C` | `lap_number<10` |
| `<=` | Menor ou igual a | `%3C=` | `position<=3` ou `position%3C=3` |
| `>` | Maior que | `%3E` | `speed>300` ou `speed%3E300` |
| `>=` | Maior ou igual a | `%3E=` | `lap_duration>=90` ou `lap_duration%3E=90` |

### Parâmetro Especial `latest`
Você pode substituir o identificador numérico de sessão ou evento por `latest` para obter diretamente a sessão mais recente ou em andamento:
```http
https://api.openf1.org/v1/sessions?session_key=latest
https://api.openf1.org/v1/laps?session_key=latest&driver_number=1
```

---

## 3. Tabela Resumo dos Endpoints

| Endpoint | Descrição Principal | Filtros Mais Comuns |
| :--- | :--- | :--- |
| [`/meetings`](#1-meetings) | Fins de semana de GP (circuitos, país, ano) | `year`, `meeting_key`, `country_name` |
| [`/sessions`](#2-sessions) | Sessões do fim de semana (Treinos, Quali, Sprint, Corrida) | `session_key`, `meeting_key`, `session_name`, `year` |
| [`/drivers`](#3-drivers) | Informações cadastrais dos pilotos | `session_key`, `driver_number`, `team_name` |
| [`/laps`](#4-laps) | Tempos de voltas, setores (S1, S2, S3) e velocidades | `session_key`, `driver_number`, `lap_number` |
| [`/car_data`](#5-car_data) | Telemetria do carro (~3.7 Hz: acelerador, freio, velocidade, RPM, DRS, marcha) | `session_key`, `driver_number`, `date`, `speed` |
| [`/location`](#6-location) | Coordenadas espaciais (X, Y, Z) dos carros na pista | `session_key`, `driver_number`, `date` |
| [`/intervals`](#7-intervals) | Diferença de tempo entre carros e para o líder | `session_key`, `driver_number`, `gap_to_leader` |
| [`/position`](#8-position) | Histórico de posições ao longo da sessão | `session_key`, `driver_number`, `position` |
| [`/starting_grid`](#9-starting_grid) | Grid inicial de largada | `session_key`, `position`, `driver_number` |
| [`/pit`](#10-pit) | Entradas e tempos de paradas no pit stop | `session_key`, `driver_number`, `lap_number` |
| [`/stints`](#11-stints) | Composição de pneus e duração de stints | `session_key`, `driver_number`, `compound` |
| [`/race_control`](#12-race_control) | Bandeiras, safety car e mensagens oficiais da direção de prova | `session_key`, `flag`, `category`, `driver_number` |
| [`/weather`](#13-weather) | Condições climáticas (temperatura de pista/ar, chuva, vento) | `session_key`, `date` |
| [`/team_radio`](#14-team_radio) | Links de áudio das comunicações de rádio | `session_key`, `driver_number` |
| [`/session_result`](#15-session_result) | Classificação final e resultados da sessão | `session_key`, `position`, `driver_number` |
| [`/overtakes`](#16-overtakes) | Histórico de ultrapassagens registradas | `session_key`, `driver_number` |

---

## 4. Detalhamento dos Endpoints

### 1. `/meetings`
Retorna a lista de Grandes Prêmios e eventos.
* **Campos Principais:** `meeting_key`, `meeting_name`, `meeting_official_name`, `circuit_key`, `circuit_short_name`, `country_name`, `country_code`, `date_start`, `gmt_offset`, `year`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/meetings?year=2024"
  ```

### 2. `/sessions`
Retorna sessões específicas de um GP (ex: FP1, FP2, FP3, Qualifying, Sprint, Race).
* **Campos Principais:** `session_key`, `meeting_key`, `session_name`, `session_type`, `date_start`, `date_end`, `year`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/sessions?meeting_key=1230"
  ```

### 3. `/drivers`
Lista os pilotos registrados para uma sessão.
* **Campos Principais:** `driver_number`, `broadcast_name`, `full_name`, `name_acronym`, `team_name`, `team_colour`, `headshot_url`, `country_code`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/drivers?session_key=latest"
  ```

### 4. `/laps`
Tempos de volta e setores detalhados.
* **Campos Principais:** `lap_number`, `lap_duration`, `duration_sector_1`, `duration_sector_2`, `duration_sector_3`, `i1_speed`, `i2_speed`, `st_speed`, `is_pit_out_lap`, `date_start`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/laps?session_key=9161&driver_number=63&lap_number=8"
  ```

### 5. `/car_data`
Telemetria bruta do carro gravada em alta frequência (~3.7 Hz).
* **Campos Principais:** `date`, `driver_number`, `speed` (km/h), `rpm`, `throttle` (0-100), `brake` (0-100), `n_gear` (marcha), `drs` (código de ativação).
* > [!WARNING]
  > Este endpoint retorna volumes muito grandes de dados. Sempre filtre por `driver_number` e use intervalos de `date` ou tempos específicos.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/car_data?session_key=latest&driver_number=1&speed>=315"
  ```

### 6. `/location`
Posicionamento dos veículos no circuito através de coordenadas espaciais tridimensionais.
* **Campos Principais:** `date`, `driver_number`, `x`, `y`, `z`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/location?session_key=latest&driver_number=4"
  ```

### 7. `/intervals`
Diferenças de tempo entre pilotos e distâncias em relação ao líder.
* **Campos Principais:** `date`, `driver_number`, `gap_to_leader`, `interval`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/intervals?session_key=latest"
  ```

### 8. `/position`
Histórico das trocas de posição dos carros na pista.
* **Campos Principais:** `date`, `driver_number`, `position`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/position?session_key=latest&driver_number=16"
  ```

### 9. `/starting_grid`
Grid de alinhamento antes do início de uma corrida ou sprint.
* **Campos Principais:** `position`, `driver_number`, `lap_duration`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/starting_grid?session_key=7783&position<=3"
  ```

### 10. `/pit`
Informações sobre entradas nos boxes.
* **Campos Principais:** `driver_number`, `lap_number`, `pit_duration`, `date`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/pit?session_key=latest"
  ```

### 11. `/stints`
Estratégia de pneus e número de voltas percorridas com cada composto.
* **Campos Principais:** `stint_number`, `driver_number`, `compound` (`SOFT`, `MEDIUM`, `HARD`, `INTERMEDIATE`, `WET`), `tyre_age_at_start`, `lap_start`, `lap_end`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/stints?session_key=latest"
  ```

### 12. `/race_control`
Mensagens emitidas pela direção de prova durante a sessão.
* **Campos Principais:** `date`, `category` (ex: `Flag`, `SafetyCar`), `flag` (`GREEN`, `YELLOW`, `RED`, `CHEQUERED`), `scope`, `sector`, `message`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/race_control?session_key=latest&flag=YELLOW"
  ```

### 13. `/weather`
Condições meteorológicas coletadas periodicamente (~1 minuto).
* **Campos Principais:** `air_temperature`, `track_temperature`, `humidity`, `pressure`, `rainfall` (0 ou 1), `wind_speed`, `wind_direction`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/weather?session_key=latest"
  ```

### 14. `/team_radio`
Registros das transmissões de áudio entre pilotos e engenheiros.
* **Campos Principais:** `date`, `driver_number`, `recording_url` (link direto para o arquivo de áudio em `.mp3`).
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/team_radio?session_key=latest&driver_number=44"
  ```

### 15. `/session_result`
Classificação final oficial da sessão (publicada após o término).
* **Campos Principais:** `position`, `driver_number`, `points`, `grid_position`, `status`, `session_key`.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/session_result?session_key=7782&position<=3"
  ```

### 16. `/overtakes`
Eventos de ultrapassagens capturados durante a sessão.
* **Campos Principais:** dados identificando o piloto que ultrapassou, o ultrapassado e a volta do evento.
* **Exemplo:**
  ```bash
  curl "https://api.openf1.org/v1/overtakes?session_key=latest"
  ```

---

## 5. Fluxo Recomendado de Integração

Ao consumir a API para análises de dados ou dashboards, a sequência ideal de requisições costuma seguir esta hierarquia:

```
[1] /meetings (Descobrir o meeting_key do GP desejado)
       │
       ▼
[2] /sessions (Obter o session_key da Corrida ou Classificação)
       │
       ├───────────────────┬───────────────────┬───────────────────┐
       ▼                   ▼                   ▼                   ▼
  /drivers               /laps               /pit               /stints
(Lista e cores)    (Voltas e tempos)     (Paradas no box)   (Estratégia pneus)
       │
       ▼ (Avançado / Telemetria)
  /car_data ou /location
(Filtrado por piloto e volta)
```

---

## 6. Exemplos de Implementação

### Exemplo em Python (`requests`)

```python
import time
import requests

BASE_URL = "https://api.openf1.org/v1"

def get_latest_session_drivers():
    # 1. Busca os dados da sessão mais recente
    sessions_url = f"{BASE_URL}/sessions?session_key=latest"
    session_data = requests.get(sessions_url).json()
    if not session_data:
        print("Nenhuma sessão encontrada.")
        return

    session = session_data[0]
    session_key = session["session_key"]
    print(f"Sessão: {session['session_name']} - {session['location']} ({session['year']})")

    # Respeita o rate limit
    time.sleep(0.5)

    # 2. Busca os pilotos participantes
    drivers_url = f"{BASE_URL}/drivers?session_key={session_key}"
    drivers = requests.get(drivers_url).json()

    print(f"\nPilotos ({len(drivers)}):")
    for d in drivers:
        print(f"#{d['driver_number']} - {d['full_name']} ({d['team_name']})")

if __name__ == "__main__":
    get_latest_session_drivers()
```

### Exemplo de Exportação Direta para CSV

Você pode baixar qualquer tabela diretamente em formato tabular compatível com Excel e Pandas:
```bash
curl -o voltas_sessao.csv "https://api.openf1.org/v1/laps?session_key=latest&csv=true"
```


# Guia de Uso do Dashboard Streamlit

O Dashboard interativo do projeto foi desenvolvido com foco na facilidade de navegação, experiência visual inspirada na transmissão oficial da Fórmula 1 e economia de cotas de API através de cache local.

---

## 1. Inicializando a Aplicação

Execute o comando padrão definido na `skill.md`:

```bash
poetry run streamlit run src/app.py
```

---

## 2. Estrutura de Navegação

### Barra Lateral (Sidebar)
1. **Temporada:** Escolha o ano do campeonato (2023 ou 2024).
2. **Grande Prêmio:** Lista com os GPs do calendário da temporada.
3. **Sessão:** Selecione entre treinos livres (FP1, FP2, FP3), classificação (Qualifying), corrida sprint ou a corrida principal (Race).

---

### Abas Principais

#### 1. 🏆 Visão Geral da Sessão (`session_overview.py`)
- **Cartões de Métricas (KPIs):** Vencedor da corrida, tempo da melhor volta, temperatura da pista e ar, e número total de voltas completadas.
- **Tabela de Classificação:** Posição de chegada, número do carro, piloto, equipe, posição no grid de largada, variação de posições, pontos conquistados e status final.
- **Gráfico de Variação de Grid:** Gráfico horizontal colorido indicando pilotos que ganharam (verde) ou perderam (vermelho) posições.

#### 2. ⏱️ Ritmo e Voltas (`lap_analysis.py`)
- **Painel de Setores:** Identificação dos melhores tempos dos setores 1, 2 e 3 e seus respectivos pilotos.
- **Comparativo de Ritmo:** Gráfico interativo com a progressão volta a volta de cada piloto selecionado com as cores oficiais das equipes.
- **Estratégia de Pneus:** Linha do tempo empilhada mostrando quais compostos (Macio, Médio, Duro, Intermediário, Chuva) foram usados por volta em cada stint.
- **Duelo entre Companheiros de Equipe:** Tabela comparativa direta de tempos e posições finais entre pilotos da mesma escuderia.

#### 3. ⚡ Telemetria Comparativa (`telemetry_view.py`)
- **Seleção Direta:** Escolha dois pilotos rivais para comparar.
- **Gráficos Curva a Curva:** Subplots sincronizados de:
  - Velocidade (km/h) e velocidade delta.
  - Pressão no pedal do acelerador (0 a 100%).
  - Pressão no pedal do freio (0 a 100%).
- **Alinhamento por Distância:** O módulo interpola a distância percorrida no circuito, permitindo analisar com precisão os pontos de frenagem e reaceleração de cada piloto.


# Relatório 2

## Avaliação de Desempenho da Rede SDN (Latência e Vazão)

### 1. Objetivo 

Atribuição: realizar os experimentos de desempenho sobre a rede SDN previamente configurada, com foco na **avaliação de latência e vazão** entre os hosts da topologia.

O controlador SDN (POX) e a topologia Mininet já se encontravam configurados e funcionais, sendo utilizados como infraestrutura base para os testes.

------------------------------------------------------------------------

### 2. Ambiente Experimental

-   Emulador de rede: **Mininet**
-   Controlador SDN: **POX (forwarding.l2_learning)**
-   Protocolo de controle: **OpenFlow**
-   Switches: **Open vSwitch**
-   Ferramentas de medição:
    -   `ping` (latência)
    -   `iperf` (vazão)

------------------------------------------------------------------------

### 3. Topologia Considerada

A topologia utilizada possui: 
- 3 hosts (h1, h2, h3) 
- 3 switches (s1, s2, s3) 
- Um host conectado a cada switch 
- Enlaces com capacidade de
**100 Mbps** 
- Atrasos configurados nos links (10 ms e 15 ms)

Os caminhos entre os hosts diferem em número de saltos e atraso acumulado, permitindo observar o impacto topológico no desempenho.

------------------------------------------------------------------------

### 4. Medição de Latência (B.1)

A latência foi medida utilizando o comando `ping`, com 10 pacotes ICMP enviados entre os pares de hosts.

#### 4.1 Resultados Observados

-   **h1 → h2**: menor latência média
-   **h1 → h3**: maior latência inicial
-   **h2 → h3**: latência intermediária

Em todos os casos, observou-se que o primeiro pacote apresentou maior latência (por volta de 3 a 5ms), enquanto os pacotes subsequentes apresentaram tempos significativamente menores (por volta de ~0.06ms).

#### 4.2 Análise

Esse comportamento é atribuído ao processo de aprendizado do controlador SDN. Inicialmente, ocorre flooding para descoberta dos endereços MAC. Após o aprendizado, regras de fluxo são instaladas nos switches, reduzindo a latência nos pacotes seguintes.

------------------------------------------------------------------------

### 5. Medição de Vazão (B.2)

A vazão foi medida com a ferramenta `iperf`, utilizando conexões TCP com duração de 10 segundos.

#### 5.1 Resultados Obtidos

  Comunicação          Vazão Média
  -------------------- -------------
  h1 → h2              \~94.8 Mbps
  h1 → h3              \~93.2 Mbps
  h2 → h3              \~95.1 Mbps
  h2 → h3 (variação)   \~74.6 Mbps

#### 5.2 Análise

Os valores medidos se aproximam da capacidade máxima dos enlaces, indicando que a rede SDN opera de forma eficiente.

A redução observada em um dos testes (74.6 Mbps) está associada a maior RTT e atraso acumulado no caminho, evidenciando o impacto da latência no desempenho do protocolo TCP.

------------------------------------------------------------------------

### 6. Impacto Topológico nos Resultados

Os experimentos demonstraram que a topologia da rede influencia diretamente o desempenho: 
- Caminhos com **menos saltos** apresentam menor latência e maior estabilidade. 
- Caminhos com **maior número de enlaces e maior atraso acumulado** resultam em maior latência inicial e possível redução de vazão.

Mesmo em um ambiente SDN, o desempenho final da comunicação depende fortemente das características físicas e lógicas da topologia.

------------------------------------------------------------------------

### 7. Conclusão

Os testes realizados permitiram avaliar de forma clara o desempenho da rede SDN em termos de latência e vazão.
Os resultados confirmam que: 
- O controlador SDN funciona corretamente após o período de aprendizado. 
- A vazão alcança valores próximos ao limite configurado dos enlaces.
- A topologia e os atrasos configurados exercem influência direta no desempenho.

Esses dados servem como base para a análise final e discussão desenvolvidas na etapa seguinte do projeto.
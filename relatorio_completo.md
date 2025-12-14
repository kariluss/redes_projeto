# Relatório Completo

### 1. Objetivos

- Implantar uma topologia de rede real no mininet (Rede IPE/RNP, Cesnet, Geant, Internet2 ou outra), onde há um host atrelado a cada switch da rede.
- Configurar um controlador SDN para possibilitar comunicação entre os hosts e monitorar tráfego em cada switch.
- Realizar a comunicação de cada um dos hosts da rede com algum outro host existente.
- Avaliar o desempenho de comunicação entre os nós, considerando latência e vazão.

------------------------------------------------------------------------

### 2. Instalação do Mininet

O Mininet é um emulador de rede que permite a criação de redes virtuais para testes de SDN.

Ele foi instalado no ambiente WSL no Windows 11, seguindo os passos padrão:

``` bash
sudo apt update
sudo apt install mininet
```

Após a instalação, a versão foi validada com:

``` bash
mn --version
```

------------------------------------------------------------------------

### 3. Instalação do POX

O POX é um controlador SDN escrito em Python, utilizado para gerenciar redes de software definidas.

Foi obtido via repositório git:

``` bash
git clone https://github.com/noxrepo/pox.git
```

O controlador é executado com o módulo de aprendizado de camada 2:

``` bash
cd pox
./pox.py forwarding.l2_learning
```

------------------------------------------------------------------------

### 4. Topologia Utilizada

A topologia utilizada faz parte do escopo de testes iniciais, contendo:

-   3 switches
-   3 hosts
-   Controlador externo POX
-   Links de 100 Mbps com atraso de 10--15 ms

### 4.1. Código da Topologia
O código da topologia está disponível em: [topo_projeto.py](topo_projeto.py)

Primeiro houve a importação da classe Topo do Mininet, que é usada para criar topologias personalizadas.
``` python
from mininet.topo import Topo
```

Classe foi definida como TopoProjeto, que herda da classe Topo. Após a implementação da build(), houve a criação dos switches.
- addSwitch cria um switch virtual OpenFlow.
- s1, s2 e s3 são os switches criados.
``` python
s1 = self.addSwitch("s1")
s2 = self.addSwitch("s2")
s3 = self.addSwitch("s3")
```

Então a criação dos hosts.
- addHost cria um host virtual.
- h1, h2 e h3 são os hosts criados.
- eles serão os usados para criar o tráfego (ping, iperf, etc)
``` python
h1 = self.addHost("h1")
h2 = self.addHost("h2")
h3 = self.addHost("h3")
```

Então a criação dos links. Os links são criados entre os hosts e switches, e entre os switches. Os links entre switches têm atraso e largura de banda definidos.
- addLink cria um link entre dois dispositivos.
- delay define o atraso do link em milissegundos.
- bw define a largura de banda do link em Mbps, sendo 100Mbps para esse projeto.
``` python
self.addLink(h1, s1)
self.addLink(h2, s2)
self.addLink(h3, s3)

self.addLink(s1, s2, delay="10ms", bw=100)
self.addLink(s2, s3, delay="15ms", bw=100)
```

A topologia foi iniciada com:

``` bash
sudo mn --custom topo_projeto.py --topo topoprojeto --switch ovsbr --controller=none --link tc
```

------------------------------------------------------------------------

### 5. Validação da Rede (Ping)

Após a criação da topologia, realizou‑se o teste de conectividade:

``` bash
mininet> pingall
```

Resultado obtido: 
- **0% de pacotes perdidos** 
- Conectividade plena entre h1, h2 e h3

Esse teste valida: 
- funcionamento dos links
- switches conectados ao controlador
- regras de fluxo sendo instaladas

------------------------------------------------------------------------

### 6. Log do Controlador POX

O controlador POX exibiu corretamente:

-   Mensagens de inicialização
-   Conexão dos switches
-   Instalação automática de fluxos
-   Tabelas de aprendizado MAC

Essas mensagens confirmam que o controlador está recebendo eventos OpenFlow da rede Mininet.

------------------------------------------------------------------------

### 7. Conclusão da criação do ambiente

O ambiente de testes SDN está funcional, com:

-   Mininet operando corretamente
-   POX ativo e recebendo eventos
-   Switches e hosts intercomunicando
-   Fluxos de aprendizado funcionando
-   Nenhuma perda de pacotes nos testes

Este ambiente agora está disponível para as próximas atividades do projeto (implementação de controladores customizados, métricas, tabelas de fluxo, gráficos etc.).

------------------------------------------------------------------------

### 8. Ambiente Experimental Final

-   Emulador de rede: **Mininet**
-   Controlador SDN: **POX (forwarding.l2_learning)**
-   Protocolo de controle: **OpenFlow**
-   Switches: **Open vSwitch**
-   Ferramentas de medição:
    -   `ping` (latência)
    -   `iperf` (vazão)

Resultados mostrados aqui servem como base para as análises de desempenho e comparação com outros controladores. Eles podem não resultar nos mesmos resultados mostrados no vídeo graças ao fato de que houve aprendizado por parte do controlador.

------------------------------------------------------------------------

### 9. Topologia Considerada Para os Testes

A topologia utilizada possui: 
- 3 hosts (h1, h2, h3) 
- 3 switches (s1, s2, s3) 
- Um host conectado a cada switch 
- Enlaces com capacidade de **100 Mbps** 
- Atrasos configurados nos links (10 ms e 15 ms)

Os caminhos entre os hosts diferem em número de saltos e atraso acumulado, permitindo observar o impacto topológico no desempenho.

------------------------------------------------------------------------

### 10. Medição de Latência

A latência foi medida utilizando o comando `ping`, com 10 pacotes ICMP enviados entre os pares de hosts.

``` bash
mininet> h1 ping -c 10 h2
mininet> h1 ping -c 10 h3
mininet> h2 ping -c 10 h3
```

#### 10.1 Resultados Observados

-   **h1 → h2**: menor latência média
-   **h1 → h3**: maior latência inicial
-   **h2 → h3**: latência intermediária

Em todos os casos, observou-se que o primeiro pacote apresentou maior latência (por volta de 3 a 5ms), enquanto os pacotes subsequentes apresentaram tempos significativamente menores (por volta de ~0.06ms).

#### 10.2 Análise

Esse comportamento é atribuído ao processo de aprendizado do controlador SDN. Inicialmente, ocorre flooding para descoberta dos endereços MAC. Após o aprendizado, regras de fluxo são instaladas nos switches, reduzindo a latência nos pacotes seguintes.

------------------------------------------------------------------------

### 11. Medição de Vazão

A vazão foi medida com a ferramenta `iperf`, utilizando conexões TCP com duração de 10 segundos.

``` bash
mininet> h2 iperf -s &
mininet> h1 iperf -c h2 -t 10
mininet> h3 iperf -s &
mininet> h1 iperf -c h3 -t 10
mininet> h2 iperf -c h3 -t 10
```

#### 11.1 Resultados Obtidos

| Comunicação        | Vazão Média |
|-------------------|-------------|
| h1 → h2           | ~94.8 Mbps  |
| h1 → h3           | ~93.2 Mbps  |
| h2 → h3           | ~95.1 Mbps  |
| h2 → h3 (variação)| ~74.6 Mbps  |

#### 11.2 Análise

Os valores medidos se aproximam da capacidade máxima dos enlaces, indicando que a rede SDN opera de forma eficiente.

A redução observada em um dos testes (74.6 Mbps) está associada a maior RTT e atraso acumulado no caminho, evidenciando o impacto da latência no desempenho do protocolo TCP.

------------------------------------------------------------------------

### 12. Impacto Topológico nos Resultados

Os experimentos demonstraram que a topologia da rede influencia diretamente o desempenho: 
- Caminhos com **menos saltos** apresentam menor latência e maior estabilidade. 
- Caminhos com **maior número de enlaces e maior atraso acumulado** resultam em maior latência inicial e possível redução de vazão.

Mesmo em um ambiente SDN, o desempenho final da comunicação depende fortemente das características físicas e lógicas da topologia.

------------------------------------------------------------------------

### 13. Conclusão da anáslie de resultados

Os testes realizados permitiram avaliar de forma clara o desempenho da rede SDN em termos de latência e vazão.
Os resultados confirmam que: 
- O controlador SDN funciona corretamente após o período de aprendizado. 
- A vazão alcança valores próximos ao limite configurado dos enlaces.
- A topologia e os atrasos configurados exercem influência direta no desempenho.

Esses dados servem como base para a análise final e discussão desenvolvidas na etapa seguinte do projeto.

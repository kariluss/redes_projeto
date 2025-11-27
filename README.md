# Relatório Primeiros Passos (Pedro Muniz)

## Configuração e Validação do Ambiente SDN com Mininet e POX

### 1. Objetivo

Atribuição: preparar, configurar e validar o ambiente de experimentação
SDN utilizado pelo grupo, garantindo que a topologia, switches, hosts e
controlador SDN estejam funcionando corretamente.\
Este passo foca exclusivamente no ambiente base: **Mininet**, **POX** e
**testes de conectividade**.

------------------------------------------------------------------------

### 2. Instalação do Mininet

O Mininet é um emulador de rede que permite a criação de redes virtuais
para testes de SDN.

Ele foi instalado no ambiente WSL no Windows 11, seguindo os passos
padrão:

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

O POX é um controlador SDN escrito em Python, utilizado para gerenciar
redes de software definidas.

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

A topologia foi iniciada com:

``` bash
sudo mn --topo=linear,3 --mac --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk
```

------------------------------------------------------------------------

### 5. Validação da Rede (Ping)

Após a criação da topologia, realizou‑se o teste de conectividade:

``` bash
mininet> pingall
```

Resultado obtido: - **0% de pacotes perdidos** - Conectividade plena
entre h1, h2 e h3

Esse teste valida: - funcionamento dos links\
- switches conectados ao controlador\
- regras de fluxo sendo instaladas

------------------------------------------------------------------------

### 6. Log do Controlador POX

O controlador POX exibiu corretamente:

-   Mensagens de inicialização\
-   Conexão dos switches\
-   Instalação automática de fluxos\
-   Tabelas de aprendizado MAC

Essas mensagens confirmam que o controlador está recebendo eventos
OpenFlow da rede Mininet.

------------------------------------------------------------------------

### 7. Conclusão

O ambiente de testes SDN está funcional, com:

-   Mininet operando corretamente\
-   POX ativo e recebendo eventos\
-   Switches e hosts intercomunicando\
-   Fluxos de aprendizado funcionando\
-   Nenhuma perda de pacotes nos testes

Este ambiente agora está disponível para as próximas atividades
do projeto (implementação de controladores customizados,
métricas, tabelas de fluxo, gráficos etc.).

------------------------------------------------------------------------

### 8. Evidências (Prints)

Os prints coletados incluem:

1.  Execução do Mininet\
2.  Resultado do pingall (0% dropped)\
3.  Execução do POX com logs de fluxos sendo instalados

(As imagens devem ser anexadas na versão final do relatório.)

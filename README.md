# Citizen Assist AI: orientação sobre energia elétrica para comércios pequenos

Global Solution 2 - 2026 FIAP - Pensamento Computacional e Automação com Python + Soluções em Energias Renováveis e Sustentáveis

## Integrantes
Arthur de Oliveira Carvalho | 573499
Gabriel Henrique S. de Melo Rodrigues | 573093
Andrey Crence Fernandes | 573840

## Público e problema

Público: donos de comércios pequenos que dependem de energia elétrica (padarias, mercadinhos, lojas, salões).

Problema: a informação sobre conta de luz, bandeiras tarifárias, reajustes, energia solar e economia de energia está espalhada, em linguagem técnica e, às vezes, em páginas que parecem oficiais e não são.

Solução: um assistente de terminal que responde com base em informações verificadas, mostrando a fonte, a data de verificação e as limitações, sem coletar dados pessoais.

## ODS relacionados

ODS 7 (energia limpa e acessível), ODS 12 (consumo e produção responsáveis) e ODS 13 (ação contra a mudança do clima).

## Como executar

Precisa de Python 3 (sem bibliotecas externas).

python main.py

(No Windows, se 'python' não funcionar, use 'py main.py'.) Menu: 1 perguntar, 2 navegar por categorias, 3 ver indicadores, 4 exportar CSV, 0 sair (pede nota de 1 a 5). Para ver a conta da parte de energia: 'python calculos_energia.py'.

Para testar do zero: apague 'data/historico.json', 'data/notas.json' e 'data/atendimentos.csv'. Eles são recriados sozinhos. **Não apague** 'data/base_conhecimento.json'.

## Regra de pontuação (busca por regras)

A pergunta e as palavras-chave são normalizadas (minúsculas, sem acento, sem pontuação). Cada orientação recebe pontos:

+3 por palavra-chave da orientação que aparece na pergunta;

+1 por palavra da pergunta (4 letras ou mais) que aparece no título.

Confiança **ALTA** com 6 pontos ou mais, **MÉDIA** de 3 a 5, e abaixo de 3 o assistente diz que não encontrou e sugere outras palavras ou as categorias. 'buscar()' devolve uma lista de tuplas '(pontos, orientacao)', da maior para a menor. Mostra a melhor e até duas parecidas. Não alteramos os pesos do enunciado.

## Integração com a SERS (Energias Renováveis)

As orientações 11 a 15 vêm da análise de energia: comparação entre trocar lâmpadas por LED e instalar energia solar, impacto em CO2 e onde um comércio gasta mais energia. Dados, cálculos, justificativas e limitações estão em ['ENERGIA.md'](ENERGIA.md). Os números do assistente saem de 'calculos_energia.py'.

## Fontes
Veja ['FONTES.md'](FONTES.md). Cada orientação mostra a fonte e a data de verificação na tela. O que é estimativa está marcado como estimativa.

## Uso de IA generativa

Parte do código e da pesquisa de dados foi feita com apoio de IA generativa. A equipe conferiu os dados, as contas e as referências e entende o código, como mostrado no vídeo.

## Resultado do teste com usuários (PCP)

Em 18/11/2026, o assistente foi usado em **3 sessões** (3 notas de facilidade), somando **18 atendimentos** (5 por pergunta livre e 13 por navegação de categorias). Sem nomes nem dados pessoais. Os arquivos estão em 'data/historico.json', 'data/atendimentos.csv' e 'data/notas.json'.

Indicador | Resultado
Resposta encontrada (%) | 100%
Taxa de acerto: ajudou (%) | 94% (17 de 18)
Tempo médio para encontrar | 38,4 s
Tentativas por atendimento | 1,2
Facilidade de uso (1 a 5) | 4,0 (notas 4, 3 e 5)

**Dúvidas sem solução:** "a bandeira é a mesma para todos os comércios?". O assistente achou a orientação 1 (bandeira de novembro), mas ela não respondeu a pergunta, e a pessoa marcou que não ajudou.

**Melhoria feita a partir do teste:** a orientação 5 ("A bandeira vale para todo comércio?") já respondia essa dúvida, mas faltavam palavras-chave para ela ser encontrada. Acrescentamos "a bandeira e a mesma", "mesma para todos", "para todos os comercios" e "bandeira para todos". Depois da mudança, a mesma pergunta passou a obter a orientação 5 com 11 pontos (antes, a melhor era a orientação 1 com 4 pontos).

**Outra observação:** a pergunta sobre usar os créditos da energia solar para abater a conta precisou de 3 tentativas (277 s). A base não tem uma orientação específica sobre créditos de energia. Fica como melhoria futura.

Os resultados da parte de energia estão em 'ENERGIA.md', seção 6.

## Limitações

O assistente só responde com o que está na base de 15 orientações. Fora dela, diz que não encontrou. Não há orientação específica sobre créditos de energia solar.

Os cálculos de energia usam um caso hipotético (20 tubos, 12 h/dia, 26 dias/mês), marcado como estimativa. Não garantem economia real.

Não foi possível entrevistar donos de comércio, então os dados de uso são estimativas declaradas, apoiadas em dados públicos.

Tarifas, bandeiras e regras mudam. Confira a data de verificação de cada resposta.

Este assistente NÃO é um canal oficial.

## Vídeos
- Vídeo técnico (PCP): [LINK]
- Vídeo da SERS: [LINK]

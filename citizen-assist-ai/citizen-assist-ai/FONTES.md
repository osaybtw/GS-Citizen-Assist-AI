# Fontes dos dados (pesquisa em 12/11/2026)

Legenda: [OFICIAL] = site do governo/Aneel/Planalto. [DISTRIBUIDORA] = comunicado da própria empresa. [NOTÍCIA] = imprensa (não oficial).

| Dado | Valor | Fonte |
|---|---|---|
| Valores das bandeiras | amarela R$ 0,01885/kWh; vermelha 1 R$ 0,04463/kWh; vermelha 2 R$ 0,07877/kWh | [OFICIAL] https://www.gov.br/aneel/pt-br/assuntos/tarifas/bandeiras-tarifarias |
| Quem paga bandeira | consumidores cativos, exceto sistemas isolados | [OFICIAL] mesma página |
| Bandeira de novembro/2026 | Verde, 2º mês seguido, anunciada em 30/10/2026 | [OFICIAL, agência pública] https://agenciabrasil.ebc.com.br/economia/noticia/2026-10/aneel-mantem-bandeira-tarifaria-verde-em-novembro |
| Histórico 2026 | verde jan-abr; amarela maio (e junho) | [OFICIAL] https://www.gov.br/aneel/pt-br/assuntos/noticias/2026/bandeira-tarifaria-em-junho-permanece-amarela |
| Histórico 2026 | outubro volta à verde (vinha da amarela) | [OFICIAL] https://www.gov.br/aneel/pt-br/assuntos/noticias/2026/outubro-tera-bandeira-verde-contas-de-luz-sem-custo-extra (link e título lidos na página inicial da Aneel; abra para confirmar) |
| Datas de anúncio (27/11 e 23/12) | - | [NOTÍCIA] https://itabiraonline.com.br/?p=226756 . Confirmar em https://www.gov.br/aneel/pt-br/calendario-de-atividades/acionamento-bandeiras |
| Enel SP | efeito médio 10,18%; baixa tensão 8,97% (residências e pequenos comércios); desde 04/07/2026 | [DISTRIBUIDORA] https://www.enel.com.br/pt-saopaulo/midia/press/d202607-aneel-aprova-reajuste-tarifario-da-enel-sp-novo-valor-passa-a-valer-a-partir-de-julho.html |
| EDP SP 3,16% / CPFL Piratininga 5,41%, desde 23/10/2026 | - | [NOTÍCIA] https://cenarioenergia.com.br/2026/10/14/aneel-aprova-reajustes-tarifarios-das-distribuidoras-edp-sp-e-cpfl-piratininga/ |
| Microgeração até 75 kW (CA), fontes renováveis | - | [OFICIAL] https://www2.aneel.gov.br/cedoc/ren20231059.html e https://planalto.gov.br/ccivil_03/_Ato2019-2022/2022/Lei/L14300.htm |
| Solicitação de acesso: formulário padronizado; distribuidora não pode pedir documentos além dos indicados | - | [OFICIAL] https://www2.aneel.gov.br/cedoc/ren20231059.html |
| Fio B: 60% (2026), 75% (2027), 90% (2028), sistemas após 07/01/2023 | - | [NOTÍCIA/ACADÊMICO] https://www.correio24horas.com.br/economia/planejando-gastar-r-15-mil-em-placas-solares-saiba-por-que-a-conta-de-luz-nao-zera-0926 e https://repositorio.ufgd.edu.br/jspui/bitstream/prefix/6717/1/AnnyIsabeleSilva%20-%20OrlandoMoreiraJunior.pdf |
| Votação da regulamentação adiada | jul/2026 | [NOTÍCIA] https://canalsolar.com.br/aneel-adia-votacao-para-analisar-melhor-a-regulamentacao-da-lei-14-300/ |

## Números que NÃO são dados reais
- 1.000 kWh/mês na orientação 2 (campo calculo): consumo de EXEMPLO, marcado como estimativa no campo premissas. Troque por um dado real.
- Contas aritméticas: 1.000 kWh x R$ 0,01885 = R$ 18,85; x R$ 0,04463 = R$ 44,63; x R$ 0,07877 = R$ 78,77.

## O que ainda NÃO tem fonte confiável (não inventei)
1. Tarifa em R$/kWh da classe comercial (B3) da sua distribuidora.
2. Custo de instalação de sistema solar para comércio.
3. Consumo típico de equipamentos (geladeira, ar-condicionado, iluminação).
Os itens 1 a 3 são necessários para a comparação de duas alternativas da SERS.

## Itens a confirmar nas páginas oficiais
- Percentuais do Fio B na Lei 14.300 (art. 27): abra a lei no Planalto e confira.
- EDP SP e CPFL Piratininga: procurar a notícia no site da Aneel.

## Energia (SERS), pesquisa de 17/11/2026
Veja `ENERGIA.md` e `calculos_energia.py`. Resumo dos dados novos:
- Tarifa B3 Enel SP R$ 0,78938/kWh: https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html (tabela oficial da distribuidora; REH Aneel 3.596/2026)
- Tubo LED T8 18 W Procel: https://www.glight.com.br/produto/902/t8-tubular-procel/ (fabricante)
- Preço LED R$ 42,70: https://arquivos.trf5.jus.br/TRF5/Dispensa_Licitacao/2025/09/09/20250909_0B4927_2_Mapa_Comparativo_de_Precos.PDF (preço de contratação pública; leitura do PDF: 8.540 / 200 unidades)
- Preço solar R$ 3,62/Wp (2 kWp, jun/2026): pv magazine Brasil, estudo da Greener
- Fator de CO2: MCTI (abr/2025) e TCC UFRJ citando o MCTI (2024)
- Estimativas (marcadas como tal): 20 tubos de 36 W, 12 h/dia, 26 dias/mês, sol 4,6 kWh/m²/dia, desempenho 0,80, Fio B R$ 0,15/kWh.

# Contribuição da SERS (Energias Renováveis e Sustentáveis) ao Citizen Assist AI

Esta pasta mostra a parte de energia do projeto. O código dos cálculos está em `calculos_energia.py`, e os resultados aparecem no assistente nas orientações **11 a 14** de `data/base_conhecimento.json`.

## 1. Contexto
- **Público:** donos de comércios pequenos em São Paulo (área da Enel SP).
- **Necessidade:** reduzir o gasto com energia elétrica, começando pela iluminação.
- **Como o assistente ajuda:** responde em linguagem simples se compensa trocar por LED ou instalar energia solar, mostrando a conta, as fontes e as limitações.

**Sobre os dados do comércio:** não foi possível entrevistar donos de comércio a tempo. Por isso o caso estudado (20 tubos, 12 h/dia, 26 dias/mês) é uma **estimativa declarada**, e não a medição de um comércio real. Para mostrar que a iluminação é um bom ponto de partida, usamos dados públicos (orientação 15): a iluminação responde por 18% a 44% do consumo em comércio e serviços, e a refrigeração por 40% a 50% em lojas de alimentos (fontes em `FONTES.md`). Quem quiser aplicar ao próprio comércio deve trocar `N_TUBOS`, `HORAS_DIA` e `DIAS_MES` em `calculos_energia.py`.

## 2. Dados usados
| Dado | Valor | Tipo | Origem |
|---|---|---|---|
| Tarifa B3 Enel SP (TUSD 472,42 + TE 316,96 R$/MWh) | R$ 0,78938/kWh, sem impostos, vigente de 04/07/2026 a 03/07/2027 | Real | https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html |
| Tubo LED T8 Procel | 18 W, 2200 lm, 25.000 h | Real | https://www.glight.com.br/produto/902/t8-tubular-procel/ |
| Preço do tubo LED T8 18 W | R$ 42,70/unidade (set/2025) | Real | https://arquivos.trf5.jus.br/TRF5/Dispensa_Licitacao/2025/09/09/20250909_0B4927_2_Mapa_Comparativo_de_Precos.PDF |
| Preço do sistema solar de 2 kWp | R$ 3,62/Wp (jun/2026) | Real | http://www.pv-magazine-brasil.com/2026/09/25/sistemas-fotovoltaicos-ficam-ate-7-mais-caros-no-1o-semestre-de-2026-aponta-greener/ |
| Fator de emissão do SIN | 0,0289 tCO2/MWh (média de abr/2025) a 0,0545 (2024) | Real | https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/noticias/2025/06/mcti-publica-fatores-de-emissao-de-co2-da-geracao-de-energia-eletrica-no-brasil-para-2025 e https://www.ltc.coppe.ufrj.br/src/uploads/2026/07/tcc_pedro_finalizado.pdf |
| Tubo fluorescente | 36 W | **Estimativa** | potência nominal comum, ver premissas |
| 20 tubos, 12 h/dia, 26 dias/mês (312 h/mês) | - | **Estimativa** | hipótese da equipe (comércio pequeno) |
| Sol em São Paulo | 4,6 kWh/m²/dia | **Estimativa** | https://www.opsenergia.com/blog/atlas-solar-brasil (confirmar no CRESESB SunData) |
| Desempenho do sistema solar | 0,80 | **Estimativa** | premissa usual |
| Fio B pago em 2026 | R$ 0,15/kWh (60% de ~R$ 0,25) | **Estimativa** | https://descarbonizesolucoes.com.br/blog/fio-b (fonte não oficial) |

## 3. Cálculos (período de referência: 5 anos; mesma necessidade: iluminação)
Resultados de `python calculos_energia.py`:

| | A) Trocar por LED | B) Solar (2 kWp) |
|---|---|---|
| Energia | 224,64 → 112,32 kWh/mês | gera 220,80 kWh/mês |
| Economia | 112,32 kWh = R$ 88,66/mês | R$ 141,18/mês |
| Investimento | R$ 854,00 (20 x R$ 42,70) | R$ 7.240,00 (2.000 Wp x R$ 3,62) |
| Retorno | 9,6 meses | 51,3 meses (4,3 anos) |
| Ganho líquido em 5 anos | R$ 4.465,79 | R$ 1.230,51 |
| CO2 evitado | 3,2 a 6,1 kg/mês | 6,4 a 12,0 kg/mês |

## 4. Justificativa das recomendações
- **Custo:** o LED custa cerca de 8 vezes menos e se paga em menos de 1 ano. O solar é mais caro e leva mais de 4 anos.
- **Viabilidade:** trocar tubos é rápido e não precisa de aprovação. O solar exige projeto, solicitação de acesso à distribuidora (formulário padronizado da Aneel, REN 1.059/2023) e telhado adequado.
- **Impacto ambiental:** a rede elétrica brasileira já emite pouco CO2, então o ganho ambiental dos dois é pequeno, e o solar evita cerca do dobro porque gera mais energia.
- **Recomendação:** primeiro LED. Depois, avaliar solar para o consumo que sobrar.

## 5. Limitações
- Os números valem para um caso hipotético e não garantem economia real.
- Não inclui mão de obra, reator, impostos, manutenção, troca de inversor, reajustes de tarifa nem a taxa mínima da conta.
- A regra do Fio B pode mudar (a Aneel adiou a votação de regulamentação em julho de 2026).
- Dados de sol e preços variam por local e fornecedor. Confirme com orçamentos.

## 6. Testes com usuários (preencher com os testes reais)
| Situação testada | Comentário recebido (sem nomes) | Ajuste feito |
|---|---|---|
| (ex.: pergunta sobre LED) | | |

## 7. Referências
Veja `FONTES.md` para a lista completa com as URLs.

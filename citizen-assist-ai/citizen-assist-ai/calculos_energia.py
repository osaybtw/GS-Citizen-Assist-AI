"""calculos_energia.py - Contribuição da SERS (Energias Renováveis) ao Citizen Assist AI.

Compara duas alternativas para a MESMA necessidade (iluminação de um comércio
pequeno), no MESMO período de referência (5 anos):
  A) Eficiência: trocar tubos fluorescentes T8 de 36 W por tubos LED T8 de 18 W
  B) Fonte renovável: instalar um sistema solar fotovoltaico conectado à rede
     para gerar a energia da iluminação atual.

Rode:  python calculos_energia.py
As orientações 11 a 14 de data/base_conhecimento.json usam estes mesmos números.

REAL = dado publicado com fonte.  ESTIMATIVA = hipótese da equipe (trocar pelos
dados do comércio real quando houver).
"""

# ------------------------------------------------------------------ DADOS REAIS
TARIFA_KWH = 0.78938          # R$/kWh, Enel SP, B3 (TUSD 472,42 + TE 316,96 R$/MWh), sem impostos
                              # REH ANEEL 3.596/2026, vigente 04/07/2026 a 03/07/2027
                              # Fonte: https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html
POTENCIA_LED_W = 18           # W, tubo LED T8 120 cm, 2200 lm, 25.000 h de vida (Procel)
                              # Fonte: https://www.glight.com.br/produto/902/t8-tubular-procel/
PRECO_LED_REAIS = 42.70       # R$/unidade, mapa de preços TRF5, set/2025 (LED T8 18 W/120 cm)
                              # Fonte: https://arquivos.trf5.jus.br/TRF5/Dispensa_Licitacao/2025/09/09/20250909_0B4927_2_Mapa_Comparativo_de_Precos.PDF
PRECO_SOLAR_2KWP_RS_WP = 3.62 # R$/Wp, sistema de 2 kWp, jun/2026 (Greener)
                              # Fonte: http://www.pv-magazine-brasil.com/2026/09/25/sistemas-fotovoltaicos-ficam-ate-7-mais-caros-no-1o-semestre-de-2026-aponta-greener/
FATOR_CO2_MIN = 0.0289        # tCO2/MWh, SIN, média de abr/2025 (MCTI)
FATOR_CO2_MAX = 0.0545        # tCO2/MWh, SIN, ano 2024 (MCTI, citado em TCC da UFRJ)
                              # Fontes: https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/noticias/2025/06/mcti-publica-fatores-de-emissao-de-co2-da-geracao-de-energia-eletrica-no-brasil-para-2025
                              #         https://www.ltc.coppe.ufrj.br/src/uploads/2026/07/tcc_pedro_finalizado.pdf

# ------------------------------------------------------------------ ESTIMATIVAS
N_TUBOS = 20                  # ESTIMATIVA: comércio pequeno com 20 tubos
POTENCIA_FLUOR_W = 36         # ESTIMATIVA: tubo fluorescente T8 120 cm de 36 W (sem perda do reator)
HORAS_DIA = 12                # ESTIMATIVA: horas acesas por dia
DIAS_MES = 26                 # ESTIMATIVA: dias de funcionamento por mês
HSP = 4.6                     # ESTIMATIVA: horas de sol pleno, São Paulo capital (kWh/m2/dia)
                              # (Atlas Solar Brasil 2026 cita 4,6; confirmar no CRESESB SunData)
DESEMPENHO = 0.80             # ESTIMATIVA: taxa de desempenho do sistema (perdas)
FIO_B_PAGO = 0.15             # ESTIMATIVA: R$/kWh de Fio B pago em 2026 (60% de ~R$ 0,25 na Enel SP)
                              # Fonte não oficial: https://descarbonizesolucoes.com.br/blog/fio-b
ANOS = 5                      # período de referência comum


def calcular():
    horas_mes = HORAS_DIA * DIAS_MES
    kwh_antes = N_TUBOS * POTENCIA_FLUOR_W / 1000 * horas_mes
    kwh_led = N_TUBOS * POTENCIA_LED_W / 1000 * horas_mes

    # Alternativa A: LED
    kwh_eco_a = kwh_antes - kwh_led
    eco_a_mes = kwh_eco_a * TARIFA_KWH
    invest_a = N_TUBOS * PRECO_LED_REAIS
    payback_a = invest_a / eco_a_mes

    # Alternativa B: solar dimensionado para a energia da iluminação atual
    kwh_kwp_mes = HSP * 30 * DESEMPENHO
    kwp = round(kwh_antes / kwh_kwp_mes)            # arredonda para kWp inteiro
    kwh_solar = kwp * kwh_kwp_mes
    eco_b_mes = kwh_solar * (TARIFA_KWH - FIO_B_PAGO)
    invest_b = kwp * 1000 * PRECO_SOLAR_2KWP_RS_WP
    payback_b = invest_b / eco_b_mes

    r = {
        "horas_mes": horas_mes,
        "kwh_antes": kwh_antes, "kwh_led": kwh_led,
        "A_kwh_eco_mes": kwh_eco_a, "A_eco_mes": eco_a_mes,
        "A_invest": invest_a, "A_payback_meses": payback_a,
        "A_eco_5anos": eco_a_mes * 12 * ANOS - invest_a,
        "A_co2_kg_mes": (kwh_eco_a / 1000 * FATOR_CO2_MIN * 1000,
                         kwh_eco_a / 1000 * FATOR_CO2_MAX * 1000),
        "B_kwp": kwp, "B_kwh_mes": kwh_solar, "B_eco_mes": eco_b_mes,
        "B_invest": invest_b, "B_payback_meses": payback_b,
        "B_eco_5anos": eco_b_mes * 12 * ANOS - invest_b,
        "B_co2_kg_mes": (kwh_solar / 1000 * FATOR_CO2_MIN * 1000,
                         kwh_solar / 1000 * FATOR_CO2_MAX * 1000),
    }
    return r


if __name__ == "__main__":
    for chave, valor in calcular().items():
        if isinstance(valor, tuple):
            valor = f"{valor[0]:.2f} a {valor[1]:.2f}"
        elif isinstance(valor, float):
            valor = f"{valor:.2f}"
        print(f"{chave:18s} {valor}")

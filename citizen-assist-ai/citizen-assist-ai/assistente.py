"""assistente.py - Classe Assistente do Citizen Assist AI.

Quem conversa com o cidadao: faz o atendimento, guarda o historico em
data/historico.json, calcula indicadores e exporta data/atendimentos.csv.
O assistente NUNCA pede nome, CPF, telefone ou e-mail.
"""

import csv
import json
import os
import time
from datetime import datetime

from base_conhecimento import BaseConhecimento

AVISO = "este assistente NÃO é um canal oficial."
CAMPOS_CSV = ["data", "origem", "pergunta", "id_orientacao",
              "encontrou", "ajudou", "tentativas", "tempo_segundos"]


def tem_dado_pessoal(texto):
    """True se o texto tem 8 ou mais digitos no total ou um '@'."""
    digitos = sum(1 for c in texto if c.isdigit())
    return digitos >= 8 or "@" in texto


def ler(prompt):
    """input() que nunca derruba o programa (Ctrl+C / fim de entrada = '0')."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "0"


def ler_sim_nao(prompt):
    """Repete ate receber 's' ou 'n'. Devolve True/False."""
    while True:
        resposta = ler(prompt).lower()
        if resposta in ("s", "n"):
            return resposta == "s"
        print("Responda apenas com s ou n.")


class Assistente:
    """Atendimento, historico e indicadores."""

    def __init__(self, nome, base, pasta_dados="data"):
        self.nome = nome
        self.base = base                      # objeto BaseConhecimento (composicao)
        self.pasta_dados = pasta_dados
        self.caminho_historico = os.path.join(pasta_dados, "historico.json")
        self.caminho_csv = os.path.join(pasta_dados, "atendimentos.csv")
        self.caminho_notas = os.path.join(pasta_dados, "notas.json")
        self.historico = self._carregar_lista(self.caminho_historico)
        self.notas = self._carregar_lista(self.caminho_notas)

    # ------------------------------------------------------------ arquivos
    def _carregar_lista(self, caminho):
        """Le uma lista JSON. Arquivo ausente ou corrompido -> lista vazia."""
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            return dados if isinstance(dados, list) else []
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return []

    def _salvar_lista(self, lista, caminho):
        try:
            os.makedirs(self.pasta_dados, exist_ok=True)
            with open(caminho, "w", encoding="utf-8") as arquivo:
                json.dump(lista, arquivo, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: não foi possível salvar em", caminho)

    # ------------------------------------------------------------ registro
    def registrar(self, origem, pergunta, id_orientacao, encontrou,
                  ajudou, tentativas, tempo):
        """Guarda um atendimento no historico e no arquivo JSON."""
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,                   # "pergunta" ou "categoria"
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
        }
        self.historico.append(atendimento)
        self._salvar_lista(self.historico, self.caminho_historico)

    # ----------------------------------------------------------- perguntar
    def perguntar(self):
        """Atendimento por texto livre (busca com pontuacao)."""
        inicio = time.time()
        tentativas = 0
        ultima = ""

        while True:
            texto = ler("\nDigite sua dúvida (0 para voltar): ")
            if texto == "0":
                if tentativas > 0:       # desistiu sem resolver: registra
                    self.registrar("pergunta", ultima, None, False, False,
                                   tentativas, round(time.time() - inicio, 1))
                return
            if not texto:
                print("Digite uma dúvida ou 0 para voltar.")
                continue
            if tem_dado_pessoal(texto):
                # nao registra e nao conta como tentativa
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            ultima = texto
            resultados = self.base.buscar(texto)
            nivel = self.base.confianca(resultados[0][0]) if resultados else None

            if nivel is None:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras (ex.: 'bandeira', 'reajuste',"
                      " 'energia solar') ou navegue pelas categorias.")
                continue

            pontos, melhor = resultados[0]
            print(f"\nConfiança da resposta: {nivel} ({pontos} pontos)")
            melhor.exibir()

            alternativas = [o for p, o in resultados[1:3] if p >= 1]
            if alternativas:
                print("\nOrientações parecidas:")
                for o in alternativas:
                    print(f"  - {o.titulo}")

            ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            tempo = round(time.time() - inicio, 1)
            self.registrar("pergunta", texto, melhor.id, True, ajudou,
                           tentativas, tempo)
            if ajudou:
                return
            # nao ajudou: reinicia o relogio e deixa tentar de novo
            inicio = time.time()
            tentativas = 0
            print("Tudo bem. Tente reescrever a dúvida.")

    # ------------------------------------------------------------- navegar
    def navegar(self):
        """Atendimento por categorias. 0 volta em todas as telas."""
        categorias = self.base.categorias()
        if not categorias:
            print("Não há categorias disponíveis.")
            return

        while True:
            print("\nCategorias:")
            for i, cat in enumerate(categorias, start=1):
                print(f"  {i}. {cat}")
            print("  0. Voltar")
            escolha = ler("Escolha uma categoria: ")
            if escolha == "0":
                return
            if not escolha.isdigit() or not 1 <= int(escolha) <= len(categorias):
                print("Opção inválida. Digite um número da lista.")
                continue
            self._navegar_orientacoes(categorias[int(escolha) - 1])

    def _navegar_orientacoes(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        while True:
            print(f"\n{categoria}:")
            for i, o in enumerate(orientacoes, start=1):
                print(f"  {i}. {o.titulo}")
            print("  0. Voltar")
            escolha = ler("Escolha uma orientação: ")
            if escolha == "0":
                return
            if not escolha.isdigit() or not 1 <= int(escolha) <= len(orientacoes):
                print("Opção inválida. Digite um número da lista.")
                continue

            inicio = time.time()
            o = orientacoes[int(escolha) - 1]
            o.exibir()
            ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar("categoria", categoria, o.id, True, ajudou, 1,
                           round(time.time() - inicio, 1))

    # ---------------------------------------------------------- indicadores
    def indicadores(self):
        """Calcula e imprime os indicadores do historico."""
        total = len(self.historico)
        print("\n=== Indicadores ===")
        if total == 0:
            print("Ainda não há atendimentos registrados.")
            return

        encontrados = [a for a in self.historico if a.get("encontrou")]
        ajudaram = [a for a in self.historico if a.get("ajudou")]
        pct_encontrou = 100 * len(encontrados) / total
        pct_ajudou = 100 * len(ajudaram) / total
        tentativas = sum(a.get("tentativas", 0) for a in self.historico) / total

        print(f"Atendimentos: {total}")
        print(f"Resposta encontrada: {pct_encontrou:.0f}%")
        print(f"Taxa de acerto (ajudou): {pct_ajudou:.0f}%")
        if encontrados:
            media = sum(a.get("tempo_segundos", 0) for a in encontrados) / len(encontrados)
            print(f"Tempo médio para encontrar: {media:.1f} s")
        else:
            print("Tempo médio para encontrar: sem dados")
        print(f"Tentativas por atendimento: {tentativas:.1f}")

        if self.notas:
            valores = [n.get("nota", 0) for n in self.notas]
            print(f"Facilidade de uso (1 a 5): {sum(valores) / len(valores):.1f}")
        else:
            print("Facilidade de uso (1 a 5): sem notas ainda")

        sem_solucao = []
        for a in self.historico:
            if a.get("origem") == "pergunta" and (not a.get("encontrou") or not a.get("ajudou")):
                if a.get("pergunta") not in sem_solucao:
                    sem_solucao.append(a.get("pergunta"))
        print("Dúvidas sem solução:")
        if sem_solucao:
            for pergunta in sem_solucao:
                print(f"  - {pergunta}")
        else:
            print("  nenhuma")

    # ----------------------------------------------------------- exportacao
    def exportar_csv(self):
        """Exporta o historico para data/atendimentos.csv (csv.DictWriter)."""
        try:
            os.makedirs(self.pasta_dados, exist_ok=True)
            with open(self.caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV,
                                          extrasaction="ignore")
                escritor.writeheader()
                for atendimento in self.historico:
                    escritor.writerow(atendimento)
            print(f"CSV exportado: {self.caminho_csv} ({len(self.historico)} linhas)")
        except OSError:
            print("Aviso: não foi possível exportar o CSV.")

    # ----------------------------------------------------------------- nota
    def pedir_nota(self):
        """Ao sair, pede a facilidade de uso de 1 a 5."""
        while True:
            resposta = ler("De 1 a 5, quão fácil foi usar o assistente? (0 para pular): ")
            if resposta == "0":
                return
            if resposta.isdigit() and 1 <= int(resposta) <= 5:
                self.notas.append({"data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                   "nota": int(resposta)})
                self._salvar_lista(self.notas, self.caminho_notas)
                return
            print("Digite um número de 1 a 5.")

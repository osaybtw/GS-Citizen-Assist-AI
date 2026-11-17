"""base_conhecimento.py - Classe BaseConhecimento e funcao normalizar().

Le data/base_conhecimento.json, cria objetos Orientacao e busca a melhor
orientacao para uma pergunta usando pontuacao (busca por regras).
"""

import json

from orientacao import Orientacao

# ---------------------------------------------------------------- normalizacao
ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}


def normalizar(texto):
    """Minusculas, sem acento e sem pontuacao.

    Devolve o texto com um espaco no comeco e outro no fim, para que
    ' sus ' so case com a palavra inteira (e nao com 'sustentavel').
    """
    texto = str(texto).lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


# ------------------------------------------------------------------ pontuacao
PONTOS_PALAVRA_CHAVE = 3     # palavra-chave da orientacao que aparece na pergunta
PONTOS_PALAVRA_TITULO = 1    # palavra da pergunta (4+ letras) que aparece no titulo
MIN_LETRAS_TITULO = 4
LIMITE_ALTA = 6              # melhor orientacao com 6+ pontos -> ALTA
LIMITE_MEDIA = 3             # 3 a 5 pontos -> MEDIA; abaixo disso, nao encontrou


class BaseConhecimento:
    """Conjunto de todas as orientacoes."""

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []   # lista de objetos Orientacao

    # ----------------------------------------------------------------- carregar
    def carregar(self):
        """Le o JSON e cria os objetos Orientacao.

        Nunca derruba o programa: arquivo ausente, JSON corrompido ou
        registro invalido apenas geram um aviso. Devolve True se carregou
        pelo menos uma orientacao.
        """
        self.orientacoes = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Aviso: arquivo '{self.caminho}' não encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Aviso: o arquivo '{self.caminho}' está corrompido.")
            return False
        except OSError:
            print(f"Aviso: não foi possível ler '{self.caminho}'.")
            return False

        if not isinstance(dados, list):
            print("Aviso: a base de conhecimento deve ser uma lista de registros.")
            return False

        ignorados = 0
        for registro in dados:
            try:
                self.orientacoes.append(Orientacao.de_dicionario(registro))
            except ValueError as erro:
                ignorados += 1
                print(f"Aviso: registro ignorado ({erro}).")

        if ignorados:
            print(f"Aviso: {ignorados} registro(s) ignorado(s).")
        return len(self.orientacoes) > 0

    # --------------------------------------------------------------- categorias
    def categorias(self):
        """Lista de categorias, sem repetir, na ordem em que aparecem."""
        lista = []
        for o in self.orientacoes:
            if o.categoria not in lista:
                lista.append(o.categoria)
        return lista

    def por_categoria(self, categoria):
        """Orientacoes de uma categoria."""
        return [o for o in self.orientacoes if o.categoria == categoria]

    # ------------------------------------------------------------------ pontuar
    def pontuar(self, pergunta, orientacao):
        """Pontos de UMA orientacao para a pergunta.

        +3 por palavra-chave da orientacao que aparece na pergunta
        +1 por palavra da pergunta (4+ letras) que aparece no titulo
        """
        texto = normalizar(pergunta)
        titulo = normalizar(orientacao.titulo)
        pontos = 0

        for chave in orientacao.palavras_chave:
            if normalizar(chave) in texto:
                pontos += PONTOS_PALAVRA_CHAVE

        palavras = []
        for palavra in texto.split():
            if len(palavra) >= MIN_LETRAS_TITULO and palavra not in palavras:
                palavras.append(palavra)   # cada palavra conta uma vez
        for palavra in palavras:
            if f" {palavra} " in titulo:
                pontos += PONTOS_PALAVRA_TITULO

        return pontos

    # ------------------------------------------------------------------- buscar
    def buscar(self, pergunta):
        """Lista de tuplas (pontos, orientacao), da maior para a menor.

        So entram orientacoes com pelo menos 1 ponto.
        """
        resultado = []
        for o in self.orientacoes:
            pontos = self.pontuar(pergunta, o)
            if pontos > 0:
                resultado.append((pontos, o))
        resultado.sort(key=lambda tupla: tupla[0], reverse=True)
        return resultado

    @staticmethod
    def confianca(pontos):
        """'ALTA', 'MEDIA' ou None (nao encontrou) conforme os pontos."""
        if pontos >= LIMITE_ALTA:
            return "ALTA"
        if pontos >= LIMITE_MEDIA:
            return "MEDIA"
        return None

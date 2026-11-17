"""orientacao.py - Classe Orientacao do Citizen Assist AI.

Cada objeto Orientacao representa UM registro de data/base_conhecimento.json.
Publico atendido: donos de comercios pequenos (mercadinhos, padarias,
lojas, salões etc.) que dependem de energia eletrica.

Alem dos 9 campos obrigatorios da GS de PCP, a classe aceita 3 campos
opcionais usados na contribuicao de Energias Renovaveis (SERS):
  - calculo:     texto curto mostrando a conta/estimativa (com unidades)
  - premissas:   dados e hipoteses usados na conta (identifica estimativas)
  - limitacoes:  condicoes em que a estimativa NAO vale
"""

AVISO = "este assistente NÃO é um canal oficial."

CAMPOS_OBRIGATORIOS = (
    "id", "categoria", "titulo", "palavras_chave", "resposta",
    "documentos", "onde", "fonte", "verificado_em",
)


class Orientacao:
    """Guarda os dados de uma orientacao e sabe exibi-la na tela."""

    def __init__(self, id, categoria, titulo, palavras_chave, resposta,
                 documentos, onde, fonte, verificado_em,
                 calculo="", premissas="", limitacoes=""):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave      # lista de str (sem acento)
        self.resposta = resposta
        self.documentos = documentos              # lista de str
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em
        # campos opcionais (energia)
        self.calculo = calculo
        self.premissas = premissas
        self.limitacoes = limitacoes

    @classmethod
    def de_dicionario(cls, dados):
        """Cria uma Orientacao a partir de um dicionario do JSON.

        Levanta ValueError se faltar algum campo obrigatorio ou se o
        registro nao cumprir as regras minimas (3 palavras-chave e fonte).
        Quem chama (BaseConhecimento.carregar) trata o erro e ignora o
        registro ruim, para o programa nunca travar.
        """
        if not isinstance(dados, dict):
            raise ValueError("registro nao e um dicionario")

        faltando = [c for c in CAMPOS_OBRIGATORIOS if c not in dados]
        if faltando:
            raise ValueError("campos ausentes: " + ", ".join(faltando))

        if not isinstance(dados["palavras_chave"], list) \
                or len(dados["palavras_chave"]) < 3:
            raise ValueError("minimo de 3 palavras-chave")
        if not isinstance(dados["documentos"], list):
            raise ValueError("'documentos' deve ser uma lista")
        if not str(dados["fonte"]).strip():
            raise ValueError("orientacao sem fonte")

        return cls(
            id=dados["id"],
            categoria=dados["categoria"],
            titulo=dados["titulo"],
            palavras_chave=dados["palavras_chave"],
            resposta=dados["resposta"],
            documentos=dados["documentos"],
            onde=dados["onde"],
            fonte=dados["fonte"],
            verificado_em=dados["verificado_em"],
            calculo=dados.get("calculo", ""),
            premissas=dados.get("premissas", ""),
            limitacoes=dados.get("limitacoes", ""),
        )

    def exibir(self):
        """Imprime a orientacao completa, com fonte, data e aviso."""
        print(f"\n>> {self.titulo}  [{self.categoria}]")
        print(self.resposta)

        if self.documentos:
            print("Documentos necessários:")
            for doc in self.documentos:
                print(f"  - {doc}")
        else:
            print("Documentos necessários: nenhum")

        print(f"Onde: {self.onde}")

        # bloco de energia (so aparece se a orientacao tiver calculo)
        if self.calculo:
            print(f"Cálculo: {self.calculo}")
        if self.premissas:
            print(f"Premissas: {self.premissas}")
        if self.limitacoes:
            print(f"Limitações: {self.limitacoes}")

        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print(f"Aviso: {AVISO}")

    def __str__(self):
        return f"[{self.id}] {self.titulo} ({self.categoria})"

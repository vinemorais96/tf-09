from abc import ABC, abstractmethod


class Medivel(ABC):
    @abstractmethod
    def tamanho(self):
        pass


class Item(Medivel):
    __slots__ = ("__nome", "__pai")

    def __init__(self, nome, pai=None):
        self.__nome = nome
        self.__pai = pai
        if pai is not None:
            pai.adicionar(self)

    @property
    def nome(self):
        return self.__nome

    @property
    def pai(self):
        return self.__pai

    def mover_para(self, novo_pai):
        if self.__pai is not None:
            self.__pai.remover(self)
        self.__pai = novo_pai
        if novo_pai is not None:
            novo_pai.adicionar(self)

    @property
    def caminho(self):
        if self.__pai is None:
            return self.__nome
        return f"{self.__pai.caminho}/{self.__nome}"

    @abstractmethod
    def mostrar(self, recuo=0):
        pass


class Arquivo(Item):
    __slots__ = ("__conteudo",)

    def __init__(self, nome, conteudo="", pai=None):
        super().__init__(nome, pai)
        self.__conteudo = conteudo

    @property
    def conteudo(self):
        return self.__conteudo

    def tamanho(self):
        return len(self.__conteudo)

    def mostrar(self, recuo=0):
        espacos = " " * recuo
        print(f"{espacos}{self.nome} ({self.tamanho()} bytes)")


class Pasta(Item):
    __slots__ = ("__filhos",)

    def __init__(self, nome, pai=None):
        super().__init__(nome, pai)
        self.__filhos = []

    def adicionar(self, item):
        self.__filhos.append(item)

    def remover(self, item):
        self.__filhos.remove(item)

    def tamanho(self):
        total = 0
        for filho in self.__filhos:
            total += filho.tamanho()
        return total

    def mostrar(self, recuo=0):
        espacos = " " * recuo
        print(f"{espacos}[{self.nome}]")
        for filho in self.__filhos:
            filho.mostrar(recuo + 2)


class Lixeira(Medivel):
    __slots__ = ("__itens",)

    def __init__(self):
        self.__itens = []

    def jogar_fora(self, item):
        self.__itens.append(item)

    def tamanho(self):
        total = 0
        for item in self.__itens:
            total += item.tamanho()
        return total


class Atalho(Item):
    """
    Representa um atalho (link simbolico) na arvore de arquivos.
    Herda de Item, aproveitando nome, pai, mover_para e caminho.
    """
    __slots__ = ("__destino",)

    def __init__(self, nome, destino, pai=None):
        super().__init__(nome, pai)
        self.__destino = None
        self.redirecionar(destino)

    @property
    def destino(self):
        """Expoe apenas a leitura do item de destino apontado pelo atalho."""
        return self.__destino

    def redirecionar(self, novo_destino):
        """
        Unica forma permitida de alterar o destino do atalho.
        Impede referencias circulares para si mesmo ou para qualquer pasta ancestral.
        """
        if novo_destino is self:
            raise ValueError("O atalho nao pode apontar para si mesmo.")

        ancestral = self.pai
        while ancestral is not None:
            if novo_destino is ancestral:
                raise ValueError("O atalho nao pode apontar para uma pasta ancestral.")
            ancestral = ancestral.pai

        self.__destino = novo_destino

    def tamanho(self):
        """Polimorfismo: um atalho ocupa sempre exatamente 1 byte fixo."""
        return 1

    def mostrar(self, recuo=0):
        """Exibe o atalho formatado com o caminho absoluto do seu destino."""
        espacos = " " * recuo
        print(f"{espacos}{self.nome} -> {self.__destino.caminho}")


def espaco_total(mediveis):
    total = 0
    for medivel in mediveis:
        total += medivel.tamanho()
    return total


def tentar(descricao, acao):
    print(f"Tentativa: {descricao}")
    try:
        acao()
        print("  -> Sucesso (inesperado)")
    except Exception as erro:
        print(f"  -> Falhou como esperado: {type(erro).__name__}: {erro}")


if __name__ == "__main__":
    disco = Pasta("C:")
    usuarios = Pasta("Users", disco)
    usuario = Pasta("vinicius", usuarios)
    desktop = Pasta("Desktop", usuario)
    projetos = Pasta("Projetos", usuario)

    documento = Arquivo("relatorio.txt", "Conteudo confidencial do relatorio", desktop)
    script = Arquivo("automacao.py", "print('Ola Mundo')", desktop)

    # 1 atalho para arquivo e 1 atalho para pasta independente
    atalho_arquivo = Atalho("atalho_relatorio.lnk", documento, desktop)
    atalho_pasta = Atalho("atalho_projetos.lnk", projetos, desktop)

    print("=== Arvore de Arquivos Completa ===")
    disco.mostrar()
    print()

    lixeira = Lixeira()
    arquivo_lixo = Arquivo("antigo.log", "dados temporarios descartados")
    lixeira.jogar_fora(arquivo_lixo)

    total_calculado = espaco_total([documento, desktop, lixeira])
    print(f"Espaco total (arquivo + pasta com atalhos + lixeira): {total_calculado} bytes")
    print()

    print("=== Testes de Falhas Esperadas ===")
    def atribuir_destino_direto():
        atalho_arquivo.destino = script

    tentar("Modificar atalho.destino diretamente por atribuicao", atribuir_destino_direto)

    def apontar_para_si_mesmo():
        atalho_arquivo.redirecionar(atalho_arquivo)

    tentar("Redirecionar atalho para si mesmo", apontar_para_si_mesmo)

    def apontar_para_pasta_pai():
        atalho_arquivo.redirecionar(desktop)

    tentar("Redirecionar atalho para a pasta onde esta contido", apontar_para_pasta_pai)
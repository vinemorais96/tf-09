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
        
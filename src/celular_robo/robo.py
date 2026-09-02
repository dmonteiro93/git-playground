# RoboColetor + QuantidadeValida — enunciado, Seção 2.1.
#
# `Robo` (posição, __init_subclass__/_registro, avancar/girar, estrategia/modo,
# Observer) já vem pronto em robo_base.py — não precisa reescrever, só importar:
#
from celular_robo.robo_base import Robo, Coordenada, Direcao
from celular_robo.estrategias import RotaColeta
#
# TODO: implemente aqui.
# - RoboColetor(Robo): reaproveita Coordenada (x, y) por herança — não precisa
#   redeclarar. Adicione o que for específico da coleta (ex.: bandeja).
# - QuantidadeValida: descriptor novo (mesmo protocolo de Coordenada/Percentual
#   em robo_base.py), validando que a quantidade coletada de um item nunca é
#   negativa nem passa do pedido.
# - __str__/__repr__ (robô) e __len__ (bandeja — quantos itens já coletados).

    

class QuantidadeValida:
    def __set_name__(self, owner, name):
        self.nome = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.nome]

    def __set__(self, instance, valor):
        if valor < 0:
            raise ValueError("O pedido não pode ser menor que 0!")
        if valor > instance.quantidade_requerida:
            raise ValueError("A quantidade não pode ser maior que o pedido!")
        instance.__dict__[self.nome] = valor

class ItemPedido:
    quantidade_coletada = QuantidadeValida()

    def __init__(self, codinome, quantidade_requerida, posicao,
                 fragil=False, urgente=False):
        self.codinome = codinome
        self.quantidade_requerida = quantidade_requerida
        self.posicao = tuple(posicao)
        self.fragil = fragil
        self.urgente = urgente
        self.quantidade_coletada = 0

    def __repr__(self):
        return (
            f"ItemPedido(codinome={self.codinome!r}, "
            f"quantidade={self.quantidade_coletada}, "
            f"posicao={self.posicao}, "
            f"fragil={self.fragil}, "
            f"urgente={self.urgente})"
        )

    def __str__(self):
        return f"{self.codinome}: {self.quantidade_coletada} unidade(s)"


class Pedido:
    def __init__(self, lote, itens : list):
        self.lote = lote
        self.itens = itens

    def __repr__(self):
        return f"Pedido(lote={self.lote!r}, itens={self.itens!r})"

    def __str__(self):
        return f"Lote: {self.lote}\nItens: {self.itens}"

class Bandeja:
    def __init__(self, itens):
        self.itens = {} if itens is None else itens

    def __len__(self):
        return sum(item.quantidade_coletada for item in self.itens.values())

    def adicionar(self, item):
        self.itens[item.codinome] = item

    def remover(self,item):
        self.itens.pop(item.codinome)

class RoboColetor(Robo):
    estrategia: RotaColeta

    def __init__(self, nome, bandeja, x=0, y=0, direcao=Direcao.LESTE, obstaculos=None, bateria=100, alcance_sensor=1, alcance_radio=5, estrategia=None, modo=None):
        super().__init__(nome, x, y, direcao, obstaculos, bateria, alcance_sensor, alcance_radio, estrategia, modo)
        self.bandeja = bandeja

    def __len__(self):
        return len(self.bandeja)
        
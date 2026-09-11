# Command — ComandoColeta — enunciado, Seção 2.3.
#
# Herde de `Comando` (comandos_base.py — ABC com registro automático):
#
#   from celular_robo.comandos_base import Comando
#
# TODO: implemente aqui. ComandoColeta(Comando): __init__(codinome, posicao,
# quantidade), com .executar(robo) e .desfazer(robo) (remove o item da
# bandeja, decrementa a contagem coletada).

from celular_robo.comandos_base import Comando
from celular_robo.robo import RoboColetor, ItemPedido


def criar_comandos_do_pedido(pedido):
        comandos = []
        for item in pedido.itens:
            comando = ComandoColeta(item)
            comandos.append(comando)
        return comandos

def executar_pedido(robo):
    comandos = criar_comandos_do_pedido(robo.pedido)

    for comando in comandos:
        robo.executar_comando(comando)


class ComandoColeta(Comando):
    def __init__(self, codinome, posicao=None, quantidade=None):
        if isinstance(codinome, ItemPedido):
            self.item = codinome
            self.codinome = codinome.codinome
            self.posicao = codinome.posicao
            self.quantidade = codinome.quantidade_requerida
        else:
            self.codinome = codinome
            self.posicao = tuple(posicao)
            self.quantidade = quantidade
            self.item = None

    def __repr__(self):
        return (
            f"ComandoColeta("
            f"{self.quantidade} de {self.codinome} "
            f"na posicao {self.posicao})"
        )

    def executar(self, robo: RoboColetor):
        if self.item is None:
            self.item = next(
                item
                for item in robo.pedido.itens
                if item.codinome == self.codinome
            )

        coletou = robo.modo.executar_coleta(robo, self.item)

        if coletou:
            robo.notificar("coleta")

            if robo.pedido.pedido_pronto():
                robo.notificar("Bandeja Pronta")

    def desfazer(self, robo: RoboColetor):
        robo.bandeja.remover(self.item)
        self.item.quantidade_coletada -= self.quantidade

    
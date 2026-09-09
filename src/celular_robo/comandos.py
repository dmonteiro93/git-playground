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
from celular_robo.robo import RoboColetor
from celular_robo.robo import RoboColetor, ItemPedido, Pedido

class ComandoColeta(Comando):
    def __init__(self, item : ItemPedido):
        self.item = item

    def __repr__(self):
            return (
                    f"ComandoColeta("
                    f"Coletados {self.item.quantidade} "
                    f"de {self.item.codinome} "
                    f"na posicao {self.item.posicao})"
    )
    def executar(self, robo : RoboColetor):
        robo.estrategia.coletar(robo, self.item)
        if robo.pedido.pedido_pronto():
             robo.notificar("Bandeja Pronta")

    def desfazer(self, robo: RoboColetor):
        robo.bandeja.remover(self.item)
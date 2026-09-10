# Strategy — RotaDireta, RotaComDuplaConferencia — enunciado, Seção 2.3.
# (Não confundir com estrategias_base.py — genérico do curso, não editar. Ao
# contrário de Command/Observer/State, aqui você NÃO herda de `Estrategia`:
# escreva sua própria base, ver TODO abaixo — motivo em estrategias_base.py.)
#
# TODO: implemente aqui. Considere uma base comum (RotaColeta) com
# __init_subclass__ registrando cada rota, ver Seção 2.2 (metaprogramação
# aplicada a uma segunda hierarquia).

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from celular_robo.robo import RoboColetor

from celular_robo.robo_base import Direcao


class RotaColeta(ABC):
    _registro_rotas = {}

    def __init_subclass__(cls, nome=None,**kwargs):
        super().__init_subclass__(**kwargs)

        if nome is not None:
            RotaColeta._registro_rotas[nome] = cls


    def _ir_ate_item(self, robo : RoboColetor, item):
            xitem,yitem = item.posicao
            while robo.x != xitem or robo.y != yitem:
                if robo.x > xitem: #Estou a direita do item que quero coletar
                    robo.girar_ate(Direcao.OESTE)
                    if not robo.avancar():
                        raise RuntimeError("Não foi possível avançar até o item.")
                elif robo.x < xitem: #Estou a esquerda do item que quero coletar
                    robo.girar_ate(Direcao.LESTE)
                    if not robo.avancar():
                        raise RuntimeError("Não foi possível avançar até o item.")
                if robo.y > yitem: #Estou acima do item que quero coletar
                    robo.girar_ate(Direcao.SUL)
                    if not robo.avancar():
                        raise RuntimeError("Não foi possível avançar até o item.")
                elif robo.y < yitem: #Estou abaixo do item que quero coletar
                    robo.girar_ate(Direcao.NORTE)
                    if not robo.avancar():
                        raise RuntimeError("Não foi possível avançar até o item.")

class RotaDireta(RotaColeta, nome="direta"):
    def coletar(self, robo, item):
        self._ir_ate_item(robo, item)

        item.quantidade_coletada = item.quantidade_requerida
        robo.bandeja.adicionar(item)

class RotaComDuplaConferencia(RotaColeta, nome="dupla_conferencia"):
    def coletar(self, robo, item):
        self._ir_ate_item(robo, item)

        if robo.posicao != item.posicao:
            raise RuntimeError("Item não está na posição esperada.")

        item.quantidade_coletada = item.quantidade_requerida
        robo.bandeja.adicionar(item)
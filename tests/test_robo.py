import pytest

from celular_robo.robo import Bandeja, ItemPedido, Pedido, RoboColetor
from celular_robo.robo_base import Direcao
from celular_robo.fabrica import criar_robo_configurado


def test_item_pedido_inicia_com_quantidade_coletada_zero():
    item = ItemPedido("Projeto Aurora", 3, (2, 4))
    assert item.quantidade_coletada == 0


def test_quantidade_coletada_nao_pode_ser_negativa():
    item = ItemPedido("Projeto Aurora", 3, (2, 4))
    with pytest.raises(ValueError):
        item.quantidade_coletada = -1


def test_quantidade_coletada_nao_pode_exceder_a_requerida():
    item = ItemPedido("Projeto Aurora", 3, (2, 4))
    with pytest.raises(ValueError):
        item.quantidade_coletada = 4


def test_pedido_pronto_somente_quando_todos_os_itens_estao_completos():
    item1 = ItemPedido("Aurora", 2, (1, 1))
    item2 = ItemPedido("Vesper", 1, (2, 2))
    pedido = Pedido("Lote-1", [item1, item2])

    assert pedido.pedido_pronto() is False
    item1.quantidade_coletada = 2
    assert pedido.pedido_pronto() is False
    item2.quantidade_coletada = 1
    assert pedido.pedido_pronto() is True


def test_bandeja_soma_quantidades_coletadas():
    item1 = ItemPedido("Aurora", 2, (1, 1))
    item2 = ItemPedido("Vesper", 3, (2, 2))
    item1.quantidade_coletada = 2
    item2.quantidade_coletada = 1

    bandeja = Bandeja(None)
    bandeja.adicionar(item1)
    bandeja.adicionar(item2)

    assert len(bandeja) == 3


def test_robo_coletor_reaproveita_posicao_e_direcao_da_base():
    robo = criar_robo_configurado(
        "RoboColetor", "Coletor-1",
        estrategia_nome="direta", area_nome="centro_padrao",
    )
    assert robo.posicao == (0, 0)
    assert robo.direcao is Direcao.LESTE
    assert isinstance(robo, RoboColetor)


def test_robo_coletor_len_retorna_quantidade_na_bandeja():
    robo = criar_robo_configurado(
        "RoboColetor", "Coletor-1",
        estrategia_nome="direta", area_nome="centro_padrao",
    )
    item = ItemPedido("Aurora", 2, (1, 1))
    item.quantidade_coletada = 2
    robo.bandeja.adicionar(item)
    assert len(robo) == 2

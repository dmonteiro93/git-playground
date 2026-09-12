import pytest

from celular_robo.excecoes import PedidoInvalido
from celular_robo.modelo_features import validar_pedido
from celular_robo.robo import ItemPedido, Pedido


def test_pedido_com_codinome_inexistente():
    item = ItemPedido("ProjetoInexistente", 1, (0, 0))
    pedido = Pedido("Lote-1", [item])
    disponibilidade = {"Aurora": 10, "Vesper": 5}

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)


def test_pedido_com_quantidade_maior_que_disponivel():
    item = ItemPedido("Aurora", 11, (0, 0))
    pedido = Pedido("Lote-1", [item])
    disponibilidade = {"Aurora": 10, "Vesper": 5}

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)


def test_pedido_vazio_e_invalido():
    pedido = Pedido("Lote-1", [])
    disponibilidade = {"Aurora": 10, "Vesper": 5}

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)


def test_pedido_misto_com_urgente_e_fragil_e_invalido():
    item_urgente = ItemPedido("Aurora", 1, (0, 0), urgente=True)
    item_fragil = ItemPedido("Vesper", 1, (1, 1), fragil=True)
    pedido = Pedido("Lote-1", [item_urgente, item_fragil])
    disponibilidade = {"Aurora": 10, "Vesper": 5}

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)


def test_pedido_urgente_exige_rota_direta():
    item = ItemPedido("Aurora", 1, (0, 0), urgente=True)
    pedido = Pedido("Lote-1", [item])

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, {"Aurora": 10}, "dupla_conferencia")


def test_pedido_fragil_exige_dupla_conferencia():
    item = ItemPedido("Aurora", 1, (0, 0), fragil=True)
    pedido = Pedido("Lote-1", [item])

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, {"Aurora": 10}, "direta")


def test_pedido_urgente_com_rota_direta_e_valido():
    item = ItemPedido("Aurora", 1, (0, 0), urgente=True)
    pedido = Pedido("Lote-1", [item])
    validar_pedido(pedido, {"Aurora": 10}, "direta")


def test_pedido_fragil_com_dupla_conferencia_e_valido():
    item = ItemPedido("Aurora", 1, (0, 0), fragil=True)
    pedido = Pedido("Lote-1", [item])
    validar_pedido(pedido, {"Aurora": 10}, "dupla_conferencia")

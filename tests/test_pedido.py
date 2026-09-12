# TODO: seus testes de pedido — enunciado, Seção 2.7 (pytest.raises(PedidoInvalido),
# conflito fragil+urgente de Seção 2.4).
import pytest

from celular_robo.excecoes import PedidoInvalido
from celular_robo.modelo_features import validar_pedido
from celular_robo.robo import ItemPedido, Pedido


def test_pedido_com_codinome_inexistente():
    item = ItemPedido(
        "ProjetoInexistente",
        1,
        (0, 0)
    )

    pedido = Pedido(
        "Lote-1",
        [item]
    )

    disponibilidade = {
        "Aurora": 10,
        "Vesper": 5,
    }

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)

# TODO: seus testes de pedido — enunciado, Seção 2.7 (pytest.raises(PedidoInvalido),
# conflito fragil+urgente de Seção 2.4).
import pytest

from celular_robo.excecoes import PedidoInvalido
from celular_robo.modelo_features import validar_pedido
from celular_robo.robo import ItemPedido, Pedido


def test_pedido_com_codinome_inexistente():
    item = ItemPedido(
        "ProjetoInexistente",
        1,
        (0, 0)
    )

    pedido = Pedido(
        "Lote-1",
        [item]
    )

    disponibilidade = {
        "Aurora": 10,
        "Vesper": 5,
    }

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)

def test_pedido_com_quantidade_maior_que_disponivel():
    item = ItemPedido(
        "Aurora",
        11,
        (0, 0)
    )

    pedido = Pedido(
        "Lote-1",
        [item]
    )

    disponibilidade = {
        "Aurora": 10,
        "Vesper": 5,
    }

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)


def test_pedido_vazio_e_invalido():
    pedido = Pedido("Lote-1", [])

    disponibilidade = {
        "Aurora": 10,
        "Vesper": 5,
    }

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)


def test_pedido_misto_com_urgente_e_fragil_e_invalido():
    item_urgente = ItemPedido(
        "Aurora",
        1,
        (0, 0),
        urgente=True
    )

    item_fragil = ItemPedido(
        "Vesper",
        1,
        (1, 1),
        fragil=True
    )

    pedido = Pedido(
        "Lote-1",
        [item_urgente, item_fragil]
    )

    disponibilidade = {
        "Aurora": 10,
        "Vesper": 5,
    }

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)

def test_pedido_com_codinome_inexistente():
    item = ItemPedido(
        "ProjetoInexistente",
        1,
        (0, 0)
    )

    pedido = Pedido(
        "Lote-1",
        [item]
    )

    disponibilidade = {
        "Aurora": 10,
        "Vesper": 5,
    }

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)

def test_pedido_com_quantidade_maior_que_disponivel():
    item = ItemPedido(
        "Aurora",
        11,
        (0, 0)
    )

    pedido = Pedido(
        "Lote-1",
        [item]
    )

    disponibilidade = {
        "Aurora": 10,
        "Vesper": 5,
    }

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)


def test_pedido_vazio_e_invalido():
    pedido = Pedido("Lote-1", [])

    disponibilidade = {
        "Aurora": 10,
        "Vesper": 5,
    }

    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido, disponibilidade)
# TODO: seus testes de configuração/LPS — enunciado, Seção 2.7 (pytest.raises,
# @pytest.mark.parametrize cobrindo estratégia×área).
import pytest

from celular_robo import robo
from celular_robo.modelo_features import validar_configuracao, validar_pedido
from celular_robo.robo import Pedido, ItemPedido
from celular_robo.excecoes import PedidoInvalido
from celular_robo.fabrica import criar_robo_configurado
from celular_robo.modelo_features import RotaColeta
from celular_robo.excecoes import ConfiguracaoInvalida
from celular_robo.modos import ModoColetando, ModoAguardandoVerificacao
from celular_robo.observadores import EquipeDeTestes, RegistroAuditoria

@pytest.mark.parametrize(
    "estrategia, area, deve_criar",
    [
        ("direta", "centro_padrao", True),
        ("dupla_conferencia", "centro_padrao", True),
        ("direta", "area_quarentena", False),
    ],
)
def test_contrato_criar_ou_recusar(estrategia, area, deve_criar):
    if deve_criar:
        robo = criar_robo_configurado(
        "RoboColetor",
        "Teste",
        estrategia_nome=estrategia,
        area_nome=area,
    )
        classe_esperada = RotaColeta._registro_rotas[estrategia]
        assert isinstance(robo.estrategia, classe_esperada)
    else:
        with pytest.raises(ConfiguracaoInvalida):
            criar_robo_configurado(
                "RoboColetor",
                "Teste",
                estrategia_nome=estrategia,
                area_nome=area,
            )

def test_area_quarentena_possui_obstaculos():
    robo = criar_robo_configurado(
        "RoboColetor",
        "Coletor-Teste",
        estrategia_nome="dupla_conferencia",
        area_nome="area_quarentena",
    )

    assert len(robo.obstaculos) > 0

def test_robo_coletor_comeca_no_modo_coletando():
    robo = criar_robo_configurado(
        "RoboColetor",
        "Coletor-Teste",
        estrategia_nome="direta",
        area_nome="centro_padrao",
    )

    assert isinstance(robo.modo, ModoColetando)

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


@pytest.mark.parametrize(
    "estrategia,area",
    [
        ("direta", "centro_padrao"),
        ("dupla_conferencia", "centro_padrao"),
        ("dupla_conferencia", "area_quarentena"),
    ],
)
def test_combinacoes_validas_de_estrategia_e_area(estrategia, area):
    validar_configuracao(
        "RoboColetor",
        estrategia,
        area,
    )


def test_rota_direta_na_area_quarentena_e_invalida():
    with pytest.raises(ConfiguracaoInvalida):
        validar_configuracao(
            "RoboColetor",
            "direta",
            "area_quarentena",
        )
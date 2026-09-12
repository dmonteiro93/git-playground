import pytest

from celular_robo.estrategias import RotaColeta, RotaDireta, RotaComDuplaConferencia
from celular_robo.excecoes import ErroColeta
from celular_robo.fabrica import criar_robo_configurado
from celular_robo.robo import ItemPedido


def test_rotas_de_coleta_sao_registradas_automaticamente():
    assert RotaColeta._registro_rotas["direta"] is RotaDireta
    assert RotaColeta._registro_rotas["dupla_conferencia"] is RotaComDuplaConferencia


@pytest.mark.parametrize("estrategia_nome", ["direta", "dupla_conferencia"])
def test_rotas_coletam_item_e_atualizam_bandeja(estrategia_nome):
    robo = criar_robo_configurado(
        "RoboColetor", "Coletor-1",
        estrategia_nome=estrategia_nome, area_nome="centro_padrao",
    )
    item = ItemPedido("Aurora", 2, (2, 3))

    robo.estrategia.coletar(robo, item)

    assert item.quantidade_coletada == 2
    assert robo.bandeja.itens["Aurora"] is item
    assert robo.posicao == (2, 3)


def test_rota_falha_ao_encontrar_obstaculo():
    robo = criar_robo_configurado(
        "RoboColetor", "Coletor-1",
        estrategia_nome="direta", area_nome="centro_padrao",
    )
    robo.obstaculos = {(1, 0)}
    item = ItemPedido("Aurora", 1, (2, 0))

    with pytest.raises(ErroColeta):
        robo.estrategia.coletar(robo, item)

    assert item.quantidade_coletada == 0
    assert "Aurora" not in robo.bandeja.itens

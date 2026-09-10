# TODO: teste da transição ModoColetando -> ModoAguardandoVerificacao
# disparada pelo Observer quando a bandeja completa — enunciado, Seção 2.7.
import pytest

from celular_robo.robo import ItemPedido, Pedido
from celular_robo.comandos import ComandoColeta
from celular_robo.fabrica import criar_robo_configurado
from celular_robo.modos import ModoAguardandoVerificacao, ModoColetando
from celular_robo.observadores import EquipeDeTestes, RegistroAuditoria

def test_bandeja_pronta_muda_modo():
    robo = criar_robo_configurado(
        "RoboColetor",
        "Coletor-Teste",
        estrategia_nome="direta",
        area_nome="centro_padrao",
    )

    equipe = EquipeDeTestes()
    robo.adicionar_observador(equipe)

    assert isinstance(robo.modo, ModoColetando)

    robo.notificar("Bandeja Pronta")

    assert isinstance(robo.modo, ModoAguardandoVerificacao)

def test_registro_auditoria():
    robo = criar_robo_configurado(
            "RoboColetor",
            "Coletor-Teste",
            estrategia_nome="direta",
            area_nome="centro_padrao",
        )
    registro = RegistroAuditoria()
    robo.adicionar_observador(registro)

    robo.notificar("Bandeja Pronta")

    assert registro.eventos[0][0] == "Bandeja Pronta"

def test_modo_coletando_esta_apto_para_operar():
    modo = ModoColetando()

    assert modo.apto_para_operar() is True

def test_modo_aguardando_verificacao_nao_esta_apto_para_operar():
    modo = ModoAguardandoVerificacao()

    assert modo.apto_para_operar() is False


def test_comando_nao_coleta_quando_aguardando_verificacao():
    robo = criar_robo_configurado(
        "RoboColetor",
        "Coletor-Teste",
        estrategia_nome="direta",
        area_nome="centro_padrao",
    )

    robo.modo = ModoAguardandoVerificacao()

    item = ItemPedido(
        "Projeto Aurora",
        2,
        (1, 1),
        fragil=False,
        urgente=False,
    )

    pedido = Pedido("Lote-Teste", [item])
    robo.receber_pedido(pedido)

    comando = ComandoColeta(item)
    comando.executar(robo)

    assert item.quantidade_coletada == 0

def test_comando_coleta_quando_apto():
    robo = criar_robo_configurado(
        "RoboColetor",
        "Coletor-Teste",
        estrategia_nome="direta",
        area_nome="centro_padrao",
    )

    robo.modo = ModoColetando()

    item = ItemPedido(
        "Projeto Aurora",
        2,
        (1, 1),
        fragil=False,
        urgente=False,
    )

    pedido = Pedido("Lote-Teste", [item])
    robo.receber_pedido(pedido)

    comando = ComandoColeta(item)
    comando.executar(robo)

    assert item.quantidade_coletada == item.quantidade_requerida
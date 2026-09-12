# TODO: teste da transição ModoColetando -> ModoAguardandoVerificacao
# disparada pelo Observer quando a bandeja completa — enunciado, Seção 2.7.
import pytest

from celular_robo.estrategias import RotaDireta
from celular_robo.excecoes import PedidoInvalido
from celular_robo.modelo_features import validar_pedido
from celular_robo.persistencia import ler_catalogo, montar_pedido_de_json, montar_robo_de_config
from celular_robo.robo import ItemPedido, Pedido
from celular_robo.comandos import (
    ComandoColeta,
    criar_comandos_do_pedido,
    executar_pedido,
)
from celular_robo.fabrica import criar_robo_configurado
from celular_robo.modos import ModoAguardandoVerificacao, ModoColetando
from celular_robo.observadores import RegistroAuditoria

def test_desfazer_coleta_remove_da_bandeja_e_reverte_quantidade():
    robo = criar_robo_configurado(
        "RoboColetor",
        "Coletor-Teste",
        estrategia_nome="direta",
        area_nome="centro_padrao",
    )

    item = ItemPedido(
        "Projeto Aurora",
        2,
        (3, 4),
        fragil=False,
        urgente=False,
    )

    pedido = Pedido("Lote de Testes", [item])
    robo.receber_pedido(pedido)

    comando = ComandoColeta(item)

    comando.executar(robo)

    assert item.quantidade_coletada == 2
    assert "Projeto Aurora" in robo.bandeja.itens

    comando.desfazer(robo)

    assert item.quantidade_coletada == 0
    assert "Projeto Aurora" not in robo.bandeja.itens


def test_rejeicao_retorna_para_coletando_e_mantem_itens():
    robo = criar_robo_configurado(
        "RoboColetor",
        "Coletor-Teste",
        estrategia_nome="direta",
        area_nome="centro_padrao",
    )

    item1 = ItemPedido(
        "Projeto Aurora",
        2,
        (3, 4),
        fragil=False,
        urgente=False,
    )

    item2 = ItemPedido(
        "Projeto Vesper",
        1,
        (5, 2),
        fragil=False,
        urgente=False,
    )

    pedido = Pedido("Lote de Testes", [item1, item2])
    robo.receber_pedido(pedido)
    auditoria = RegistroAuditoria()
    robo.adicionar_observador(auditoria)

    comando = ComandoColeta(item1)
    comando.executar(robo)

    assert item1.quantidade_coletada == 2
    assert "Projeto Aurora" in robo.bandeja.itens

    robo.modo = ModoAguardandoVerificacao()

    robo.verificar_bandeja(False)

    assert isinstance(robo.modo, ModoColetando)
    assert item1.quantidade_coletada == 2
    assert "Projeto Aurora" in robo.bandeja.itens
    assert robo.pedido is pedido

    assert any(
        evento == "pedido_rejeitado"
        for evento, dados in auditoria.eventos
    )


def test_ler_catalogo(tmp_path):
    caminho = tmp_path / "catalogo.json"

    caminho.write_text(
        """
        {
            "Projeto Aurora": 10,
            "Projeto Vesper": 5,
            "Projeto Orion": 8
        }
        """,
        encoding="utf-8",
    )

    catalogo = ler_catalogo(caminho)

    assert catalogo == {
        "Projeto Aurora": 10,
        "Projeto Vesper": 5,
        "Projeto Orion": 8,
    }
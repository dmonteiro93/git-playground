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

def test_modo_coletando_permite_coleta():
    modo = ModoColetando()
    assert hasattr(modo, "executar_coleta")


def test_modo_aguardando_verificacao_bloqueia_coleta():
    modo = ModoAguardandoVerificacao()
    assert hasattr(modo, "executar_coleta")

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


def test_criar_comandos_do_pedido_cria_um_comando_para_cada_item():
    item1 = ItemPedido(
        "Projeto Aurora",
        2,
        (3, 4),
        fragil=False,
        urgente=True,
    )

    item2 = ItemPedido(
        "Projeto Vesper",
        1,
        (7, 2),
        fragil=True,
        urgente=False,
    )

    pedido = Pedido("Lote de Testes", [item1, item2])

    comandos = criar_comandos_do_pedido(pedido)

    assert len(comandos) == 2

    assert isinstance(comandos[0], ComandoColeta)
    assert isinstance(comandos[1], ComandoColeta)

    assert comandos[0].item is item1
    assert comandos[1].item is item2

    assert comandos[0].codinome == "Projeto Aurora"
    assert comandos[0].posicao == (3, 4)
    assert comandos[0].quantidade == 2

    assert comandos[1].codinome == "Projeto Vesper"
    assert comandos[1].posicao == (7, 2)
    assert comandos[1].quantidade == 1


def test_executar_pedido_processa_comandos_em_ordem():
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

    executar_pedido(robo)

    assert item1.quantidade_coletada == 2
    assert item2.quantidade_coletada == 1

    assert "Projeto Aurora" in robo.bandeja.itens
    assert "Projeto Vesper" in robo.bandeja.itens

    assert len(robo._historico_comandos) == 2

    assert robo._historico_comandos[0].item is item1
    assert robo._historico_comandos[1].item is item2

    assert robo._historico_comandos[0].codinome == "Projeto Aurora"
    assert robo._historico_comandos[1].codinome == "Projeto Vesper"

def test_desfazer_ultimo_comando_remove_do_historico():
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

    executar_pedido(robo)

    assert len(robo._historico_comandos) == 2
    assert len(robo.bandeja) == 3

    resultado = robo.desfazer_ultimo_comando()

    assert resultado is True
    assert len(robo._historico_comandos) == 1

    assert item2.quantidade_coletada == 0
    assert "Projeto Vesper" not in robo.bandeja.itens

    assert item1.quantidade_coletada == 2
    assert "Projeto Aurora" in robo.bandeja.itens

def test_observer_muda_para_aguardando_verificacao_quando_bandeja_pronta():
    robo = criar_robo_configurado(
        "RoboColetor",
        "Coletor-Teste",
        estrategia_nome="direta",
        area_nome="centro_padrao",
    )
    assert isinstance(robo.modo, ModoColetando)

    robo.notificar("Bandeja Pronta")

    assert isinstance(robo.modo, ModoAguardandoVerificacao)

def test_pedido_urgente_exige_rota_direta():
    item = ItemPedido(
        "Aurora",
        1,
        (0, 0),
        urgente=True
    )

    pedido = Pedido("Lote-1", [item])

    disponibilidade = {"Aurora": 10}

    with pytest.raises(PedidoInvalido):
        validar_pedido(
            pedido,
            disponibilidade,
            "dupla_conferencia"
        )


def test_pedido_fragil_exige_dupla_conferencia():
    item = ItemPedido(
        "Aurora",
        1,
        (0, 0),
        fragil=True
    )

    pedido = Pedido("Lote-1", [item])

    disponibilidade = {"Aurora": 10}

    with pytest.raises(PedidoInvalido):
        validar_pedido(
            pedido,
            disponibilidade,
            "direta"
        )

def test_pedido_urgente_com_rota_direta_e_valido():
    item = ItemPedido(
        "Aurora",
        1,
        (0, 0),
        urgente=True
    )

    pedido = Pedido("Lote-1", [item])

    validar_pedido(
        pedido,
        {"Aurora": 10},
        "direta"
    )


def test_pedido_fragil_com_dupla_conferencia_e_valido():
    item = ItemPedido(
        "Aurora",
        1,
        (0, 0),
        fragil=True
    )

    pedido = Pedido("Lote-1", [item])

    validar_pedido(
        pedido,
        {"Aurora": 10},
        "dupla_conferencia"
    )

def test_montar_robo_de_config_cria_robo_configurado():
    config = {
        "tipo": "RoboColetor",
        "nome": "Coletor-Teste",
        "estrategia": "direta",
        "area": "centro_padrao",
    }

    robo = montar_robo_de_config(config)

    assert robo.nome == "Coletor-Teste"
    assert isinstance(robo.estrategia, RotaDireta)
    assert robo.obstaculos == set()

def test_montar_pedido_de_json(tmp_path):
    caminho = tmp_path / "pedido.json"

    caminho.write_text(
        """
        {
            "lote": "Lote-1",
            "itens": [
                {
                    "codinome": "Projeto Aurora",
                    "quantidade_requerida": 2,
                    "posicao": [3, 4],
                    "fragil": false,
                    "urgente": true
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    pedido = montar_pedido_de_json(caminho)

    assert pedido.lote == "Lote-1"
    assert len(pedido.itens) == 1

    item = pedido.itens[0]
    assert item.codinome == "Projeto Aurora"
    assert item.quantidade_requerida == 2
    assert item.posicao == (3, 4)
    assert item.fragil is False
    assert item.urgente is True

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
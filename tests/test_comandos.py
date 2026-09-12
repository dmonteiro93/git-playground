from celular_robo.comandos import ComandoColeta, criar_comandos_do_pedido, executar_pedido
from celular_robo.fabrica import criar_robo_configurado
from celular_robo.modos import ModoAguardandoVerificacao
from celular_robo.robo import ItemPedido, Pedido


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
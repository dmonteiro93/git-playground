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



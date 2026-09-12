from celular_robo.fabrica import criar_robo_configurado
from celular_robo.modos import ModoAguardandoVerificacao, ModoColetando
from celular_robo.observadores import EquipeDeTestes, RegistroAuditoria
from celular_robo.robo import ItemPedido, Pedido


def criar_robo():
    return criar_robo_configurado(
        "RoboColetor", "Coletor-1",
        estrategia_nome="direta", area_nome="centro_padrao",
    )


def test_equipe_de_testes_muda_para_aguardando_verificacao():
    robo = criar_robo()
    equipe = EquipeDeTestes()
    robo.adicionar_observador(equipe)

    robo.notificar("Bandeja Pronta")

    assert isinstance(robo.modo, ModoAguardandoVerificacao)


def test_modo_aguardando_bloqueia_nova_coleta():
    robo = criar_robo()
    item = ItemPedido("Aurora", 1, (1, 1))
    robo.receber_pedido(Pedido("Lote-1", [item]))
    robo.modo = ModoAguardandoVerificacao()

    assert robo.modo.executar_coleta(robo, item) is False
    assert item.quantidade_coletada == 0


def test_verificacao_aprovada_retorna_ao_modo_coletando():
    robo = criar_robo()
    robo.modo = ModoAguardandoVerificacao()

    assert robo.verificar_bandeja(True) is True
    assert isinstance(robo.modo, ModoColetando)


def test_verificacao_rejeitada_retorna_ao_modo_coletando_e_notifica():
    robo = criar_robo()
    auditoria = RegistroAuditoria()
    robo.adicionar_observador(auditoria)
    robo.modo = ModoAguardandoVerificacao()

    assert robo.verificar_bandeja(False) is False
    assert isinstance(robo.modo, ModoColetando)
    assert any(evento == "pedido_rejeitado" for evento, _ in auditoria.eventos)


def test_registro_auditoria_armazena_eventos_e_dados():
    auditoria = RegistroAuditoria()
    robo = criar_robo()

    robo.adicionar_observador(auditoria)
    robo.notificar("coleta", codinome="Aurora")

    assert len(auditoria.eventos) == 1
    evento, dados = auditoria.eventos[0]
    assert evento == "coleta"
    assert dados["codinome"] == "Aurora"
    assert dados["robo"] is robo

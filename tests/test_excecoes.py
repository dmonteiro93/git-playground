from celular_robo.excecoes import ConfiguracaoInvalida, ErroColeta, PedidoInvalido


def test_excecoes_especificas_herdam_de_erro_coleta():
    assert issubclass(ConfiguracaoInvalida, ErroColeta)
    assert issubclass(PedidoInvalido, ErroColeta)

from celular_robo.excecoes import (
    ConfiguracaoInvalida,
    ErroColeta,
    PedidoInvalido,
)


def test_excecoes_especificas_herdam_de_erro_coleta():
    assert issubclass(ConfiguracaoInvalida, ErroColeta)
    assert issubclass(PedidoInvalido, ErroColeta)


def test_erro_coleta_aceita_mensagem():
    erro = ErroColeta("Falha durante a coleta.")

    assert str(erro) == "Falha durante a coleta."


def test_configuracao_invalida_aceita_mensagem():
    erro = ConfiguracaoInvalida("Configuração não permitida.")

    assert str(erro) == "Configuração não permitida."


def test_pedido_invalido_aceita_mensagem():
    erro = PedidoInvalido("Pedido não atende aos requisitos.")

    assert str(erro) == "Pedido não atende aos requisitos."
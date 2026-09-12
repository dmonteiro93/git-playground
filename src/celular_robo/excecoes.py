# Hierarquia de exceções — enunciado, Seção 2.5.
#
# TODO: implemente aqui. ErroColeta(Exception) como base;
# ConfiguracaoInvalida(ErroColeta) e PedidoInvalido(ErroColeta) como as duas
# subclasses (ver Seção 2.5 pra critério de qual usar em cada caso).
class ErroColeta(Exception):
    """Exceção base para erros relacionados ao sistema de coleta."""


class ConfiguracaoInvalida(ErroColeta):
     """Indica que uma configuração de robô não é permitida."""


class PedidoInvalido(ErroColeta):
    """Indica que um pedido não atende às regras do sistema."""
# Modelo de features / LPS — enunciado, Seção 2.4.
#
# TODO: implemente aqui. TIPOS_VALIDOS, ESTRATEGIAS_VALIDAS (derivados dos
# registros de Seção 2.2, não digitados à mão), REQUER/EXCLUI (4 dimensões: tipo,
# estratégia, área, urgência) e validar_configuracao levantando
# ConfiguracaoInvalida antes de qualquer robô ser instanciado.

from celular_robo.robo_base import Robo
from celular_robo.robo import RoboColetor
from celular_robo.estrategias import RotaColeta
from celular_robo.excecoes import ConfiguracaoInvalida


TIPOS_VALIDOS = set(Robo._registro)
ESTRATEGIAS_VALIDAS = set(RotaColeta._registro_rotas)

AREAS_VALIDAS = {
    "centro_padrao",
    "area_quarentena",
}

EXCLUI = {("area_quarentena", "direta")}

REQUER = {()}

#Validação de tipos > estratégia > área > e por fim se essa combinação tripla é permitida
def validar_configuracao(tipo_nome, estrategia_nome, area_nome):
    configuracao = (area_nome, estrategia_nome)
    if tipo_nome is None:
        raise ConfiguracaoInvalida("Configuração não permitida")
    if not tipo_nome in TIPOS_VALIDOS:
        raise ConfiguracaoInvalida("Configuração não permitida")
    if estrategia_nome is None:
        raise ConfiguracaoInvalida("Configuração não permitida")
    if not estrategia_nome in ESTRATEGIAS_VALIDAS:
        raise ConfiguracaoInvalida("Configuração não permitida")
    if area_nome is None:
        raise ConfiguracaoInvalida("Configuração não permitida")
    if not area_nome in AREAS_VALIDAS:
        raise ConfiguracaoInvalida("Configuração não permitida")

    if configuracao in EXCLUI:
        raise ConfiguracaoInvalida("Configuração não permitida")


def validar_pedido():
    pass

    
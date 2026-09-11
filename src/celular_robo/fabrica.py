# Factory — criar_robo_coletor, criar_robo_configurado — enunciado, Seção 2.3.
# (Ver fabrica_base.py — genérico do curso, não editar: criar_robo("RoboColetor",
# ...) já funciona, pode chamar direto ou usar como modelo.)
#
# TODO: implemente aqui. criar_robo_coletor(tipo_nome, ...) a partir do
# _registro (Seção 2.2); criar_robo_configurado combina isso com a validação do
# modelo de features (Seção 2.4).
#
# Contrato mínimo exigido por tests/test_00_fornecido.py (não altere a
# assinatura abaixo sem também atualizar aquele arquivo):
#
#   criar_robo_configurado(tipo_nome, nome, estrategia_nome=..., area_nome=...)


from celular_robo.fabrica_base import criar_robo
from celular_robo.modelo_features import validar_configuracao
from celular_robo.modelo_features import RotaColeta
from celular_robo.modelo_features import AREAS_VALIDAS
from celular_robo.observadores import EquipeDeTestes, RegistroAuditoria
from celular_robo.robo_base import Robo
from celular_robo.robo import Bandeja
from celular_robo.modos import ModoColetando


def obter_obstaculos(area_nome):
    if area_nome == "centro_padrao":
        obstaculos = set()
    elif area_nome == "area_quarentena":
        obstaculos = {(9,0),(9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,9),}
    return obstaculos

def criar_robo_coletor(tipo_nome, nome, **kwargs):
    return criar_robo(tipo_nome, nome, **kwargs)

def criar_robo_configurado(tipo_nome, nome, estrategia_nome, area_nome):
    validar_configuracao(tipo_nome,estrategia_nome, area_nome)
    classe_estrategia = RotaColeta._registro_rotas[estrategia_nome]
    estrategia = classe_estrategia()
    obstaculos = obter_obstaculos(area_nome)
    bandeja = Bandeja(None)
    modo = ModoColetando()

    robo = criar_robo_coletor(
        tipo_nome,
        nome,
        bandeja=bandeja,
        estrategia=estrategia,
        obstaculos=obstaculos,
        modo=modo,
    )

    robo.adicionar_observador(EquipeDeTestes())
    robo.adicionar_observador(RegistroAuditoria())

    return robo
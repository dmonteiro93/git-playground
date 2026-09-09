# TODO: teste da transição ModoColetando -> ModoAguardandoVerificacao
# disparada pelo Observer quando a bandeja completa — enunciado, Seção 2.7.
import pytest

from celular_robo import robo
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
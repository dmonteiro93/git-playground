"""Testes das regras de configuração e das features da aplicação."""

from celular_robo.modelo_features import (
    AREAS_VALIDAS,
    ESTRATEGIAS_VALIDAS,
    EXCLUI,
    REQUER,
    TIPOS_VALIDOS,
)


def test_tipo_robo_coletor_e_tipo_valido():
    assert "RoboColetor" in TIPOS_VALIDOS


def test_estrategias_esperadas_estao_registradas():
    assert {"direta", "dupla_conferencia"}.issubset(ESTRATEGIAS_VALIDAS)


def test_areas_esperadas_estao_registradas():
    assert {"centro_padrao", "area_quarentena"}.issubset(AREAS_VALIDAS)


def test_regras_de_features_contem_requerimentos_e_exclusoes():
    assert REQUER["urgente"] == "direta"
    assert REQUER["fragil"] == "dupla_conferencia"
    assert ("area_quarentena", "direta") in EXCLUI

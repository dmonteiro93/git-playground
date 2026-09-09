# Configuração e persistência — enunciado, Seção 2.6.
#
# TODO: implemente aqui. montar_robo_de_config(config) e
# montar_pedido_de_json(caminho) — mesmo par de funções do capstone do curso
# (montar_robo_de_config/montar_frota_de_json), adaptado: um arquivo
# configura o robô (tipo, estratégia, área), outro traz o pedido de coleta.
import json
from celular_robo.robo import ItemPedido
from celular_robo.robo import Pedido
from celular_robo.fabrica import criar_robo_configurado


def montar_pedido_de_json(caminho_pedido, caminho_catalogo):
    itens = []
    with open(caminho_pedido, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        for item in dados["itens"]:
            item_pedido = ItemPedido(
                                    item["codinome"],
                                    item["quantidade_requerida"],
                                    item["posicao"],
                                    item["fragil"],
                                    item["urgente"]
                                    )
            itens.append(item_pedido)
        pedido = Pedido(dados["lote"], itens)
    return pedido


def montar_robo_de_config(config):
    with open(config, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return criar_robo_configurado(
                                        dados["tipo"],
                                        dados["nome"],
                                        dados["estrategia"],
                                        dados["area"]
                                    )                                       

def montar_frota_de_json(caminho):
    pass

def ler_catalogo(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados


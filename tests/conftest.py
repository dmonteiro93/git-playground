# Fixtures compartilhadas entre seus test_*.py — TODO, à sua escolha.
# (A fixture usada por test_00_fornecido.py já vem definida nele mesmo —
# não precisa duplicar aqui.)
from celular_robo.persistencia import montar_pedido_de_json


def test_montar_pedido_de_json(tmp_path):
    caminho = tmp_path / "pedido.json"

    caminho.write_text(
        """
        {
            "lote": "Lote-1",
            "itens": [
                {
                    "codinome": "Projeto Aurora",
                    "quantidade_requerida": 2,
                    "posicao": [3, 4],
                    "fragil": false,
                    "urgente": true
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    pedido = montar_pedido_de_json(caminho)

    assert pedido.lote == "Lote-1"
    assert len(pedido.itens) == 1

    item = pedido.itens[0]
    assert item.codinome == "Projeto Aurora"
    assert item.quantidade_requerida == 2
    assert item.posicao == (3, 4)
    assert item.fragil is False
    assert item.urgente is True
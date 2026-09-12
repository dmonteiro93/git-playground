from celular_robo.persistencia import ler_catalogo, montar_pedido_de_json


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


def test_ler_catalogo(tmp_path):
    caminho = tmp_path / "catalogo.json"
    caminho.write_text(
        """
        {
            "Projeto Aurora": 10,
            "Projeto Vesper": 5,
            "Projeto Orion": 8
        }
        """,
        encoding="utf-8",
    )

    catalogo = ler_catalogo(caminho)

    assert catalogo == {
        "Projeto Aurora": 10,
        "Projeto Vesper": 5,
        "Projeto Orion": 8,
    }

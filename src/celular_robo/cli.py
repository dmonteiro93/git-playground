# CLI — enunciado, Seção 4.
#
# TODO: implemente aqui. Menu interativo (ou argparse, à sua escolha):
# listar pedido carregado, processar pedido, ver estado da bandeja,
# aprovar/rejeitar retirada da equipe de testes.

from celular_robo.comandos import executar_pedido
from celular_robo.excecoes import PedidoInvalido
from celular_robo.modelo_features import validar_pedido
from celular_robo.persistencia import (
    ler_configuracao,
    ler_catalogo,
    montar_pedido_de_json,
    montar_robo_de_config,
)

def obter_estrategia_nome(robo):
    """Retorna o nome da estratégia usada pelo robô."""
    for nome, classe in robo.estrategia.__class__._registro_rotas.items():
        if isinstance(robo.estrategia, classe):
            return nome

    return None


def exibir_bandeja(robo):
    """Exibe o estado atual da bandeja."""
    print("\n--- Estado da bandeja ---")

    if not robo.bandeja.itens:
        print("A bandeja está vazia.")
        return

    for codinome, item in robo.bandeja.itens.items():
        print(
            f"- {codinome}: "
            f"{item.quantidade_coletada}/"
            f"{item.quantidade_requerida}"
        )

    print(f"Total coletado: {len(robo.bandeja)}")


def executar_fluxo(caminho_config, caminho_missao, caminho_catalogo):
    """Executa o fluxo completo da missão."""
    config = ler_configuracao(caminho_config)
    robo = montar_robo_de_config(config)

    pedido = montar_pedido_de_json(caminho_missao)
    catalogo = ler_catalogo(caminho_catalogo)

    estrategia_nome = obter_estrategia_nome(robo)

    validar_pedido(
        pedido,
        catalogo,
        estrategia_nome=estrategia_nome,
    )

    robo.receber_pedido(pedido)

    print("\n=== Robô Coletor de Celulares ===")
    print(f"Robô: {robo.nome}")
    print(f"Lote: {pedido.lote}")
    print(f"Estratégia: {estrategia_nome}")

    print("\nIniciando coleta...")
    executar_pedido(robo)

    exibir_bandeja(robo)

    if robo.pedido.pedido_pronto():
        print("\nA bandeja está pronta para verificação.")

        resposta = input(
            "A equipe aprova a bandeja? (s/n): "
        ).strip().lower()

        if resposta == "s":
            robo.verificar_bandeja(aprovada=True)
            print("Bandeja aprovada.")
            print("Robô liberado para um novo pedido.")
        else:
            robo.verificar_bandeja(aprovada=False)
            print("Bandeja rejeitada.")
            print("Robô retornou ao modo de coleta.")

    return robo


def main():
    print("=== Configuração da missão ===")

    caminho_config = input(
        "Caminho do arquivo de configuração: "
    ).strip()

    caminho_missao = input(
        "Caminho do arquivo da missão: "
    ).strip()

    caminho_catalogo = input(
        "Caminho do arquivo do catálogo: "
    ).strip()

    try:
        executar_fluxo(
            caminho_config,
            caminho_missao,
            caminho_catalogo,
        )
    except PedidoInvalido as erro:
        print(f"\nPedido inválido: {erro}")
    except (KeyError, FileNotFoundError, ValueError) as erro:
        print(
            f"\nErro ao carregar os arquivos "
            f"ou configurar o sistema: {erro}"
        )


if __name__ == "__main__":
    main()
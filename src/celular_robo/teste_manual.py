from celular_robo.robo import RoboColetor, Bandeja, ItemPedido
from celular_robo.estrategias import RotaDireta, RotaComDuplaConferencia
from celular_robo.robo_base import Direcao
from celular_robo.comandos import ComandoColeta
from celular_robo.persistencia import montar_robo_de_config

# bandeja1 = Bandeja(None)

# item = ItemPedido(
#     "Projeto Aurora",
#     2,
#     (3, 2)
# )

# robo = RoboColetor(
#     "Teste",
#     bandeja1,
#     x=0,
#     y=0,
#     direcao=Direcao.LESTE
#     # obstaculos={(1,0)}
# )

# robo.estrategia = RotaComDuplaConferencia()

# print("Antes:", robo.posicao)

# comando = ComandoColeta(item)

# comando.executar(robo)

# print(robo.bandeja)
# print("Depois:", robo.posicao)
# print("Trajetória:", robo.trajetoria)
# print("Posição:", robo.posicao)
# print("Quantidade coletada:", item.quantidade)
# print("Itens na bandeja:", robo.bandeja.itens)
# print("Quantidade na bandeja:", len(robo.bandeja))

# comando.desfazer(robo)

# print("Quantidade na bandeja:", len(robo.bandeja))

robo = montar_robo_de_config("dados/config_exemplo.json")

print(robo)
print(type(robo))
print(robo.estrategia)
print(robo.obstaculos)
# State — ModoColetando, ModoAguardandoVerificacao — enunciado, Seção 2.3.
#
# Herde de `ModoOperacao` (modos_base.py — ABC com registro automático):
#
#   from celular_robo.modos_base import ModoOperacao
#
# TODO: implemente aqui. A transição ModoColetando -> ModoAguardandoVerificacao
# acontece via Observer (não é o próprio modo que decide sozinho), quando a
# bandeja completa.

from celular_robo.modos_base import ModoOperacao


class ModoColetando(ModoOperacao):

    def mover(self, robo):
        return robo.estrategia.mover(robo)

    def executar_coleta(self, robo, item):
        robo.estrategia.coletar(robo, item)
        return True


class ModoAguardandoVerificacao(ModoOperacao):

    def mover(self, robo):
        print(f"{robo.nome} está aguardando a verificação da bandeja.")
        return False

    def executar_coleta(self, robo, item):
        print(f"{robo.nome} está aguardando a verificação da bandeja.")
        return False

    def verificar_bandeja(self, robo, aprovada):
        if aprovada:
            robo.modo = ModoColetando()
            return True

        robo.notificar("pedido_rejeitado")
        robo.modo = ModoColetando()
        return False
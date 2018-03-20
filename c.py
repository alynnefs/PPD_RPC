# saved as greeting-client.py
import Pyro4
import sys
import pygame

meuId = sys.argv[1]
idInimigo = None
def print_name_server_object_list():
    """
    Use name_server function
    """
    ns = Pyro4.locateNS(host='localhost')
    print(ns.lookup('combate'))
    #print(ns.lookup('maker'))
    print(ns.list())

def teste_envia(comando):
    resposta = None
    while resposta == None:
        resposta = combate.teste('%s,%s,%s,%s' % (meuId, idInimigo, '1', 'oi'))
        print(resposta)


if __name__ == '__main__':
    combate = Pyro4.Proxy("PYRONAME:combate@localhost")
    #maker = Pyro4.Proxy("PYRONAME:maker@localhost")
    meuId = combate.meuID('%s' % meuId)
    while idInimigo == None:
        idInimigo = combate.idInimigo('%s' % meuId)
    print("inimigo %s" % idInimigo)
    #print(maker.greet('maker 1 to 2'))


    while 1:
        resposta = teste_envia('%s,%s,%s,%s' % (meuId, idInimigo, '1', 'oi'))




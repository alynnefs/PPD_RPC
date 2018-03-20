import Pyro4

jogA = None
jogB = None

@Pyro4.expose
class Combate(object):
    def meuID(self, name):
        if jogA == None: 
            global jogA
            jogA = name
        else:
            global jogB
            jogB = name
        print('Greeting from %s' % name)
        return ("%s" % name)

    def idInimigo(self,name):
        return jogB if name == jogA else jogA

    def teste(self,comando):
        #c = comando.split(',')
        return comando
        
        
if __name__ == '__main__':
    Pyro4.Daemon.serveSimple(
        {
            Combate: 'combate'

        },
        host='localhost'
    )
    print("jogA %s" % jogA)
    print("jogB %s" % jogB)

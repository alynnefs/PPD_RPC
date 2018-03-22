import Pyro4

jogA = None
jogB = None

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Combate(object):
    def __init__(self):
        self.msg1 = ''
        self.msg2 = ''
        self.msgAtual = ''

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

    def enviar_mensagem(self,id_jogador,msg):
        #self.msgAtual = msg
        if id_jogador == jogA:
            self.msg1 = msg
        else:
            self.msg2 = msg

    def receber_mensagem(self,id_jogador):
        if id_jogador == jogA:
            #if self.msg2 != 'start' or self.msg2 != self.msgAtual:
            return self.msg2
            #return
        else:
            #if self.msg1 != 'start' or self.msg1 != self.msgAtual:
            return self.msg1
            #return
        
if __name__ == '__main__':
    Pyro4.Daemon.serveSimple(
        {
            Combate: 'combate'

        },
        host='localhost'
    )
    #print("jogA %s" % jogA)
    #print("jogB %s" % jogB)

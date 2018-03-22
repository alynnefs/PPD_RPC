import Pyro4

jogA = None
jogB = None

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Combate(object):
    def __init__(self):
        self.msg1 = ''
        self.msg2 = ''
        #self.msgAtual = ''
        self.turnoA = True
        self.turnoB = False

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

    def muda_turno(self, id_jogador):
        print("muda turno")
        if id_jogador == jogA and self.turnoA == True:
            print("muda A -> falso")
            self.turnoA = False
        elif id_jogador == jogB and self.turnoB == True:
            print("muda B -> falso")
            self.turnoB = False
        elif id_jogador == jogA and self.turnoA == False:
            print("muda A -> verdadeiro")
            self.turnoA = True
        elif id_jogador == jogB and self.turnoB == False:
            print("muda B -> verdadeiro")
            self.turnoB = True
        else:
            pass
        

    def meu_turno(self, id_jogador):
        if id_jogador == jogA and self.turnoA == True:
            return True
        elif id_jogador == jogB and self.turnoB == True:
            return True
        if id_jogador == jogA and self.turnoA == False:
            return False
        elif id_jogador == jogB and self.turnoB == False:
            return False
        else:
            pass
        
if __name__ == '__main__':
    Pyro4.Daemon.serveSimple(
        {
            Combate: 'combate'

        },
        host='localhost'
    )
    #print("jogA %s" % jogA)
    #print("jogB %s" % jogB)

# -*- coding: utf-8 -*- 
import Pyro4
import sys
import pygame
from pygame.locals import *

pygame.init()

id_jogador = sys.argv[1]
id_inimigo = None
def print_name_server_object_list():
    """
    Use name_server function
    """
    ns = Pyro4.locateNS(host='localhost')
    print(ns.lookup('combate'))
    #print(ns.lookup('maker'))
    print(ns.list())

def protocolo(tipo, msg):
    return "%d," %(tipo)+msg

def tratar_mensagem(msg):
    if msg.split(",")[0] == '1': # código de mensagem
        print("Dado recebido: ", msg)
        textsurface = f_chat.render(msg.split(",")[1], True, (255, 0, 0))
        screen.blit(textsurface,(710,405))
        #pygame.display.update() # não mostra sem, quebra quando tem

        block = f_chat.render(name, True, (0, 0, 0))
        rect = block.get_rect()
        rect.center = (905,500)
        screen.blit(block, rect)
        pygame.display.flip()

'''
def teste_envia(comando):
    resposta = None
    while resposta == None:
        resposta = combate.teste('%s,%s,%s,%s' % (id_jogador, id_inimigo, '1', 'oi'))
        print(resposta)
'''
################################################################################

displayW = 1100
displayH = 800

# definição de cores
back = (154,255,208)
vermelho = (225, 0, 0)
verde = (0, 190, 0)
azul = (0, 0, 255)
lago = (0, 220, 220)
branco = (255, 255, 255)
cinza = (240, 240, 240)
preto = (0, 0, 0)

f_chat = pygame.font.Font(None, 25)
#f_chat2 = pygame.font.SysFont('arial', 25)

casas = [26,88,150,212,274,336,398,460,522,584]
jogo_inicial = [[[' ']*3 for c in range(10)] for d in range (10)]
# gera matriz quadrada de ordem 10, cada índice com 3 'argumentos'
jogo_atual = [[[' ']*3 for c in range(10)] for d in range (10)]


screen = pygame.display.set_mode((displayW,displayH),0,32)
screen.fill(cinza)

pygame.display.set_caption('Combate ID:%s' %id_jogador)

def cor_quadrado(i,j):
    if j < 4:
        return preto
    elif j > 5:
        return verde
    elif j > 3 and j < 6 and i > 1 and i < 4  or i > 5 and i < 8:
        return lago
    else:
        return cinza

def desenha_tabuleiro(dist, bordaSup, tam):
    for i in range(10):
        for j in range(10):
            pygame.draw.rect(screen, cor_quadrado(i,j), (dist+tam*i,bordaSup+tam*j,tam,tam))
            pygame.draw.rect(screen, branco, (dist+tam*i,bordaSup+tam*j,tam,tam),1)
            cor = branco if id_jogador == '1' else preto
            textsurface = f_chat.render(str(jogo_inicial[j][i][0]), True, cor) # por algum motivo está invertendo
            screen.blit(textsurface,(dist+tam*i+tam/2,bordaSup+tam*j+tam/2))

def desenha_chat(dist, bordaSup, tam):
    pygame.draw.rect(screen, cinza, (dist,bordaSup,tam*3/2,tam))
    pygame.draw.rect(screen, preto, (dist,bordaSup,tam*3/2,tam),1)

################################################################################

if __name__ == '__main__':
    combate = Pyro4.Proxy("PYRONAME:combate@localhost")

    id_jogador = combate.meuID('%s' % id_jogador)
    while id_inimigo == None:
        print("esperando inimigo")
        id_inimigo = combate.idInimigo('%s' % id_jogador)
    print("inimigo %s" % id_inimigo)

    #combate.enviar_mensagem(id_jogador, 'varios nadas')
    #print(combate.receber_mensagem(id_jogador))

    desenha_tabuleiro(25,25,62)
    name = ""
    while True:
        #combate.enviar_mensagem(id_jogador, 'oi do %s' %id_jogador)
        #print(combate.receber_mensagem(id_jogador))
        tratar_mensagem(combate.receber_mensagem(id_jogador))
        key=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif event.key == K_RETURN:
                    name = protocolo(1,name) # 1 significa 'tipo mensagem'
                    combate.enviar_mensagem(id_jogador, name)
                    name = ""
                elif event.key == K_SPACE:
                    name += " "

        pygame.display.update()
        desenha_chat(705,400,248)
        
        block = f_chat.render(name, True, (0, 0, 0))
        rect = block.get_rect()
        rect.center = (905,500)
        screen.blit(block, rect)
        #pygame.display.flip()
        


    try:
        while 1:
            continue
    except:
        print("Programa do jogador encerrado")
        client_socket.close()   




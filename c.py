# -*- coding: utf-8 -*- 
import Pyro4
import sys
import random
import pygame
from pygame.locals import *

pygame.init()

id_jogador = sys.argv[1]
id_inimigo = None

##################################### COMUNICAÇÃO #####################################

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
    elif msg.split(",")[0] == '2': # código de acao
        if msg.split(",")[1] == 'quit':
            print("O inimigo desistiu.")
        elif msg.split(",")[1] == 'reiniciar':
            print("O inimigo reiniciou a partida.")
            cria_matriz_inicial()
            desenha_tabuleiro(25,25,62)
'''
def teste_envia(comando):
    resposta = None
    while resposta == None:
        resposta = combate.teste('%s,%s,%s,%s' % (id_jogador, id_inimigo, '1', 'oi'))
        print(resposta)
'''
##################################### INTERFACE #####################################

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

pygame.display.set_caption('Combate ID: %s' %id_jogador)

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

def desenha_desistir(dist, bordaSup, tam):
    pygame.draw.rect(screen, preto, (dist,bordaSup,tam*2,tam),1)
    textsurface = f_chat.render("desistir", True, preto)
    screen.blit(textsurface,(dist+tam/2,bordaSup+tam/2-5))

def desenha_reiniciar(dist, bordaSup, tam):
    pygame.draw.rect(screen, preto, (dist,bordaSup,tam*2,tam),1)
    textsurface = f_chat.render("reiniciar", True, preto)
    screen.blit(textsurface,(dist+tam/2,bordaSup+tam/2-5))

##################################### BACK #####################################
def cria_matriz_inicial():
    pecas = [['F',1],[1,1],[2,8],[3,5],[4,4],[5,4],[6,4],[7,3],[8,2],[9,1],[10,1],['B',6]]
    pecas2 = [['F',1],[1,1],[2,8],[3,5],[4,4],[5,4],[6,4],[7,3],[8,2],[9,1],[10,1],['B',6]]
    if id_jogador == '1':
    #if combate.meu_turno(id_jogador):
        for i in range(4):
            for j in range(10):
                a = random.randint(0,len(pecas)-1)
                jogo_inicial[i][j][0] = pecas[a][0] # código da peça
                pecas[a][1] -= 1
                if pecas[a][1] == 0:
                    pecas.remove(pecas[a])
    elif id_jogador == '2':
        for i in range(6,10):
            for j in range(10):
                a = random.randint(0,len(pecas2)-1)
                jogo_inicial[i][j][0] = pecas2[a][0] # código da peça
                pecas2[a][1] -= 1
                if pecas2[a][1] == 0:
                    pecas2.remove(pecas2[a])
    for i in range(4,6):
        for j in range(2,8):
            if j == 2 or j == 3 or j == 6 or j ==7:
                jogo_inicial[i][j][0] = 'X'

    #mostraMatriz(jogo_inicial)
    valores_matriz()

def valores_matriz(): # adicionar posicao do quadrado
    global jogo_atual
    for i in range(10):
        for j in range(10):
            #jogo_inicial[i][j] = {'label':jogo_inicial[i][j],'posX':casas[i],'posY':casas[i]}
            jogo_inicial[i][j][1] = casas[i]
            jogo_inicial[i][j][2] = casas[j]
    print("inicial")
    #mostraMatriz(jogo_inicial)
    jogo_atual = jogo_inicial[:]

def descobre_quadrado(x,y):
    global jogo_atual
    a = x - ((x-25)%62) + 1
    b = y - ((y-25)%62) + 1
    print("a=%f" % a)
    print("b=%f"% b)
    if a >= 646 and a <= 832 and b >= 26 and b <= 88: # desistir
        print("desistir")
        combate.enviar_mensagem(id_jogador,protocolo(2,'quit')) # tipo acao
        pygame.quit()
        sys.exit()
    elif a >= 894 and a <= 1018 and b >= 26 and b <= 88: # reiniciar
        print("reiniciar")
        combate.enviar_mensagem(id_jogador,protocolo(2,'reiniciar')) # tipo acao
        cria_matriz_inicial()
        desenha_tabuleiro(25,25,62)
        
        jogo_atual = jogo_inicial[:]
        desenha_tabuleiro(25,25,62)
        #mostraMatriz(jogo_atual)
        #pygame.display.flip()
        
    elif a > 25 and a < 585 and b > 25 and b < 585:
        movimentacao(a,b)

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

    cria_matriz_inicial()
    desenha_tabuleiro(25,25,62)
    desenha_desistir(700,25,75)
    desenha_reiniciar(925,25,75)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                #print("X E Y ",x,y)
                descobre_quadrado(x,y)
            elif event.type == KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif event.key == K_RETURN:
                    name = protocolo(1,name) # 1 significa 'tipo mensagem'
                    combate.enviar_mensagem(id_jogador, name)
                    name = ""
                    combate.enviar_mensagem(id_inimigo, name)
                    print("TURNO? ",combate.meu_turno(id_jogador))
                    combate.muda_turno(id_jogador)
                    print("TURNO? ",combate.meu_turno(id_jogador))
                elif event.key == K_SPACE:
                    name += " "

        pygame.display.update()
        desenha_chat(705,400,248)
        block = f_chat.render(name, True, (0, 0, 0))
        rect = block.get_rect()
        rect.center = (905,500)
        screen.blit(block, rect)

    try:
        while 1:
            continue
    except:
        print("Programa do jogador encerrado")
        client_socket.close()   

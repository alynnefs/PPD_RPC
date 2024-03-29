# -*- coding: utf-8 -*- 
import Pyro4
import sys
import random
import pygame
from pygame.locals import *

pygame.init()

id_jogador = sys.argv[2]
id_inimigo = None

##################################### COMUNICAÇÃO #####################################

def print_name_server_object_list():
    """
    Use name_server function
    """
    ns = Pyro4.locateNS(host = sys.argv[1])
    print(ns.lookup('combate'))
    print(ns.list())

def protocolo(tipo, msg):
    return "%d," %(tipo)+msg

def tratar_mensagem(msg):
    if msg.split(",")[0] == '1': # código de mensagem
        print("Dado recebido: ", msg)
        textsurface = f_chat.render(msg.split(",")[1], True, (255, 0, 0))
        screen.blit(textsurface,(710,405))

        block = f_chat.render(name, True, (0, 0, 0))
        rect = block.get_rect()
        rect.center = (905,500)
        screen.blit(block, rect)
        pygame.display.flip()
    elif msg.split(",")[0] == '2': # código de acao
        if msg.split(",")[1] == 'quit':
            print("O inimigo desistiu.")
            pygame.quit()
            sys.exit()
        elif msg.split(",")[1] == 'reiniciar':
            print("O inimigo reiniciou a partida.")
            cria_matriz_inicial()
            desenha_tabuleiro(25,25,62)
            combate.enviar_mensagem(id_jogador,protocolo(2,'reiniciar')) # antes só atualizava o inimigo. Às vezes reinicia mais de uma vez
        elif msg.split(",")[1] == 'mover':
            cor = preto if id_jogador == '2' else verde
            if msg.split(",")[2] == 'baixo':
                baixo = True
                move_baixo(int(msg.split(",")[3]),int(msg.split(",")[4]),cor)
            elif msg.split(",")[2] == 'cima':
                cima = True
                move_cima(int(msg.split(",")[3]),int(msg.split(",")[4]),cor)
            elif msg.split(",")[2] == 'direita':
                direita = True
                move_direita(int(msg.split(",")[3]),int(msg.split(",")[4]),cor)
            elif msg.split(",")[2] == 'esquerda':
                esquerda = True
                move_esquerda(int(msg.split(",")[3]),int(msg.split(",")[4]),cor)

##################################### INTERFACE #####################################

displayW = 1100
displayH = 800

# definição de cores
back = (154,255,208)
verde = (0, 190, 0)
#azul = (0, 0, 255)
lago = (0, 220, 220)
branco = (255, 255, 255)
cinza = (240, 240, 240)
preto = (0, 0, 0)

'''
0 preto
48640 verde
56540 lago
15790320 cinza
'''

f_chat = pygame.font.Font(None, 25)
#f_chat2 = pygame.font.SysFont('arial', 25)

casas = [26,88,150,212,274,336,398,460,522,584]
jogo_inicial = [[[' ']*3 for c in range(10)] for d in range (10)]

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
            textsurface = f_chat.render(str(jogo_inicial[j][i][0]), True, branco) # por algum motivo está invertendo
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

def mostraMatriz(matriz):
    for i in range(len(matriz)):
        print(matriz[i])
        print('\n')

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
    valores_matriz()

def valores_matriz(): # adicionar posicao do quadrado
    global jogo_inicial
    for i in range(10):
        for j in range(10):
            #jogo_inicial[i][j] = {'label':jogo_inicial[i][j],'posX':casas[i],'posY':casas[i]}
            jogo_inicial[i][j][1] = casas[i]
            jogo_inicial[i][j][2] = casas[j]
    print("inicial")

def descobre_quadrado(x,y):
    global jogo_inicial
    a = x - ((x-25)%62) + 1
    b = y - ((y-25)%62) + 1
    print("a=%f" % a)
    print("b=%f"% b)

    pxarray = pygame.PixelArray(screen)
    #print("corzinha ",pxarray[a+10, b-30])

    if a >= 646 and a <= 832 and b >= 26 and b <= 88: # desistir
        print("desistir")
        combate.enviar_mensagem(id_jogador,protocolo(2,'quit')) # tipo acao
        pygame.quit()
        sys.exit()
    elif a >= 894 and a <= 1018 and b >= 26 and b <= 88: # reiniciar
        print("reiniciar")
        combate.enviar_mensagem(id_jogador,protocolo(2,'reiniciar')) # tipo acao
    elif a > 25 and a < 585 and b > 25 and b < 585:
        movimentacao(a,b)

peca = ''
baixo = False
cima = False
esquerda = False
direita = False
def movimentacao(a,b): # ainda nao funciona 100%. Seta as flags de movimentacao
    global jogo_inicial
    global peca
    global baixo
    global cima
    global direita
    global esquerda

    peca = jogo_inicial[casas.index(b)][casas.index(a)]# x e y estao invertidos
    print("peça ",peca)

    pxarray = pygame.PixelArray(screen)

    print("corzinha ",pxarray[a, b])
    if (id_jogador == '1' and pxarray[a, b+70] == 48640) or (id_jogador == '2' and pxarray[a, b+70] == 0) or pxarray[a, b+70] == 15790320: # cinza ou verde
        print("para baixo")
        baixo = True
       
    if (id_jogador == '1' and pxarray[a+10, b-30] == 48640) or (id_jogador == '2' and pxarray[a+10, b-30] == 0) or pxarray[a+10, b-30] == 15790320:
        print("para cima")
        cima = True

    if pxarray[a+70, b+10] == 48640 or pxarray[a+70, b+10] == 15790320:
        print("para direita")
        direita = True

    if pxarray[a-70, b+10] == 48640 or pxarray[a-70, b+10] == 15790320:
        print("para esquerda")
        esquerda = True

def pode_mover(a,b):
    print("pode mover?")
    if jogo_inicial[casas.index(b)][casas.index(a)][0] == ' ':
        print("sim")
        return True
    else:
        print("não")
        return False

def move_baixo(x,y,cor):
    global baixo
    a = x - ((x-25)%62) + 1
    b = y - ((y-25)%62) + 1
    if pode_mover(a,b+62):
        print("if baixo")
        pygame.draw.rect(screen, cinza, (a,b,62,62))
        pygame.draw.rect(screen, branco, (a,b,62,62),1)
        pygame.draw.rect(screen, cor, (a,b+62,62,62))
        pygame.draw.rect(screen, branco, (a,b+62,62,62),1)
        textsurface = f_chat.render(str(jogo_inicial[casas.index(b)][casas.index(a)][0]), True, branco) # por algum motivo está invertendo
        screen.blit(textsurface,(a+31,b+93))
        jogo_inicial[casas.index(b)][casas.index(a)],jogo_inicial[casas.index(b)+1][casas.index(a)] = jogo_inicial[casas.index(b)+1][casas.index(a)], jogo_inicial[casas.index(b)][casas.index(a)]  # por algum motivo está substituindo x e y
        baixo = False
        combate.muda_turno(id_jogador)
        combate.muda_turno(id_inimigo)

def move_cima(x,y,cor):
    print("funçao cima")
    global cima
    a = x - ((x-25)%62) + 1
    b = y - ((y-25)%62) + 1
    if pode_mover(a,b-62):
        pygame.draw.rect(screen, cinza, (a,b,62,62))
        pygame.draw.rect(screen, branco, (a,b,62,62),1)
        pygame.draw.rect(screen, cor, (a,b-62,62,62))
        pygame.draw.rect(screen, branco, (a,b-62,62,62),1)
        textsurface = f_chat.render(str(jogo_inicial[casas.index(b)][casas.index(a)][0]), True, branco) # por algum motivo está invertendo
        screen.blit(textsurface,(a+31,b-31))
        jogo_inicial[casas.index(b)][casas.index(a)],jogo_inicial[casas.index(b)-1][casas.index(a)] = jogo_inicial[casas.index(b)-1][casas.index(a)], jogo_inicial[casas.index(b)][casas.index(a)]  # por algum motivo está substituindo x e y
        cima = False
        combate.muda_turno(id_jogador)
        combate.muda_turno(id_inimigo)

def move_direita(x,y,cor): # algo errado com a atualização da matriz
    a = x - ((x-25)%62) + 1
    b = y - ((y-25)%62) + 1
    if pode_mover(a+62,b):
        pygame.draw.rect(screen, cinza, (a,b,62,62))
        pygame.draw.rect(screen, branco, (a,b,62,62),1)
        pygame.draw.rect(screen, cor, (a+62,b,62,62))
        pygame.draw.rect(screen, branco, (a+62,b,62,62),1)
        textsurface = f_chat.render(str(jogo_inicial[casas.index(b)][casas.index(a)][0]), True, branco) # por algum motivo está invertendo
        screen.blit(textsurface,(a+93,b+31))
        jogo_inicial[casas.index(b)][casas.index(a)],jogo_inicial[casas.index(b)][casas.index(a)+1] = jogo_inicial[casas.index(b)][casas.index(a)+1], jogo_inicial[casas.index(b)][casas.index(a)]  # por algum motivo está substituindo x e y
        direita = False
        combate.muda_turno(id_jogador)
        combate.muda_turno(id_inimigo)

def move_esquerda(x,y,cor):
    a = x - ((x-25)%62) + 1
    b = y - ((y-25)%62) + 1
    if pode_mover(a-62,b):
        pygame.draw.rect(screen, cinza, (a,b,62,62))
        pygame.draw.rect(screen, branco, (a,b,62,62),1)
        pygame.draw.rect(screen, cor, (a-62,b,62,62))
        pygame.draw.rect(screen, branco, (a-62,b,62,62),1)
        textsurface = f_chat.render(str(jogo_inicial[casas.index(b)][casas.index(a)][0]), True, branco) # por algum motivo está invertendo
        screen.blit(textsurface,(a-31,b+31))
        jogo_inicial[casas.index(b)][casas.index(a)],jogo_inicial[casas.index(b)][casas.index(a)-1] = jogo_inicial[casas.index(b)][casas.index(a)-1], jogo_inicial[casas.index(b)][casas.index(a)]  # por algum motivo está substituindo x e y
        esquerda = False
        combate.muda_turno(id_jogador)
        combate.muda_turno(id_inimigo)

################################################################################

if __name__ == '__main__':
    '''
    sys.argv[1] IP
    sys.argv[2] ID
    '''

    combate = Pyro4.Proxy("PYRONAME:combate@%s" % sys.argv[1])

    id_jogador = combate.meuID('%s' % id_jogador)
    while id_inimigo == None:
        print("esperando inimigo")
        id_inimigo = combate.idInimigo('%s' % id_jogador)
    print("inimigo %s" % id_inimigo)

    cria_matriz_inicial()
    desenha_tabuleiro(25,25,62)
    desenha_desistir(700,25,75)
    desenha_reiniciar(925,25,75)

    name = ""
    while True:
        combate.enviar_mensagem(id_jogador, 'start')
        tratar_mensagem(combate.receber_mensagem(id_jogador))
        key=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
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
                elif event.key == K_SPACE:
                    name += " "
            elif key[pygame.K_DOWN]:
                print("DOWN")
                print("TURNO? ",combate.meu_turno(id_jogador))
                if peca[0] != '' and peca[0] != 'B' and peca[0] != 'F' and combate.meu_turno(id_jogador) and baixo:
                    move_baixo(x,y,preto if id_jogador == '1' else verde)
                    combate.muda_turno(id_jogador)
                    combate.muda_turno(id_inimigo)
                    combate.enviar_mensagem(id_jogador,protocolo(2,'mover,baixo,%d,%d' %(x,y)))

            elif key[pygame.K_UP]:
                print("UP")
                print("TURNO? ",combate.meu_turno(id_jogador))
                if peca[0] != '' and peca[0] != 'B' and peca[0] != 'F' and combate.meu_turno(id_jogador) and cima:
                    move_cima(x,y,preto if id_jogador == '1' else verde)
                    combate.muda_turno(id_jogador)
                    combate.muda_turno(id_inimigo)
                    combate.enviar_mensagem(id_jogador,protocolo(2,'mover,cima,%d,%d' %(x,y)))

            elif key[pygame.K_LEFT]:
                print("LEFT")
                print("TURNO? ",combate.meu_turno(id_jogador))
                if peca[0] != '' and peca[0] != 'B' and peca[0] != 'F' and combate.meu_turno(id_jogador) and esquerda:
                    move_esquerda(x,y,preto if id_jogador == '1' else verde)
                    combate.muda_turno(id_jogador)
                    combate.muda_turno(id_inimigo)
                    combate.enviar_mensagem(id_jogador,protocolo(2,'mover,esquerda,%d,%d' %(x,y)))

            elif key[pygame.K_RIGHT]:
                print("RIGHT")
                print("TURNO? ",combate.meu_turno(id_jogador))
                if peca[0] != '' and peca[0] != 'B' and peca[0] != 'F' and combate.meu_turno(id_jogador) and direita:
                    move_direita(x,y,preto if id_jogador == '1' else verde)
                    combate.muda_turno(id_jogador)
                    combate.muda_turno(id_inimigo)
                    combate.enviar_mensagem(id_jogador,protocolo(2,'mover,direita,%d,%d' %(x,y)))

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

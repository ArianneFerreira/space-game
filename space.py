# coding;. iso-8859-1 -*-
import pygame 
from pygame.locals import * 
from sys import exit  
from random import *
from gameobjects.vector2 import Vector2

background_image_filename = 'universo.jpg'
inimigo = 'alien.png'
foguete = 'foguete.png'
bala_alien= 'estrela.png'

SCREEN_SIZE = (780, 600)

pygame.init() 


#definindo a tela 
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32) 
#adicionando o nome para a tela
pygame.display.set_caption("Space Game")

background = pygame.image.load(background_image_filename).convert()
nave = pygame.image.load(foguete).convert_alpha() 
alien = pygame.image.load(inimigo).convert_alpha() 
bala = pygame.image.load(bala_alien).convert_alpha()

#Variáveis
clock = pygame.time.Clock()

alien_pos_x = randint((SCREEN_SIZE[0]+alien.get_height())/2, SCREEN_SIZE[0]-alien.get_height())
alien_pos_y = randint(0, (SCREEN_SIZE[1])-alien.get_height())

direction_alien = Vector2(1,1)

posicao_fogete = Vector2(randint(nave.get_height(), 100), randint(nave.get_height(), 200))
posicao_alien = Vector2(alien_pos_x, alien_pos_y)

posicao_tiro = Vector2(alien_pos_x, alien_pos_y)

lista_tiros = []

tempo_tiro = 0
pode_atirar = True

def verifica_jogo_fechado():
    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                exit() 

def movimento_foguete(posicao_atual_foguete):

    speed_foguete = 200

    pressed_keys = pygame.key.get_pressed()
    direction_foguete = Vector2(0, 0)
    
    
    if pressed_keys[K_LEFT]:
        direction_foguete.x = -1
    elif pressed_keys[K_RIGHT]:
        direction_foguete.x = 1

    if pressed_keys[K_UP]:
        direction_foguete.y = -1
    elif pressed_keys[K_DOWN]:
        direction_foguete.y = 1
    
    direction_foguete.normalize()

    time_passed_foguete = clock.tick(30)
    segundos_foguete = time_passed_foguete/1000.0

    posicao_atual_foguete += direction_foguete * speed_foguete * segundos_foguete

    return (posicao_atual_foguete)



def movimento_alien(posicao_atual_alien, direction):
    
    speed_alien = 150
    
    direction_alien = direction


    if posicao_atual_alien.x > int(SCREEN_SIZE[0]-alien.get_height()):
        direction_alien.x = -1
    elif posicao_atual_alien.x < int((SCREEN_SIZE[0]/2)+alien.get_height()):
        direction_alien.x = 1
        #posicao_atual_alien.x = int((SCREEN_SIZE[0]/2)+alien.get_height())

    if posicao_atual_alien.y > int(SCREEN_SIZE[1]-alien.get_height()):
        direction_alien.y = -1
    elif posicao_atual_alien.y < 0:
        direction_alien.y = 1
        #posicao_atual_alien.y = 0
    
    time_passed_alien = clock.tick(30)
    segundos_alien = time_passed_alien/1000.0

    posicao_atual_alien += direction_alien * int(segundos_alien * speed_alien)
    
    return (posicao_atual_alien, direction_alien)

def lanca_tiro(posicao_atual_tiro, lista_tiros, pode_atirar):
   
    nova_posicao_tiro = Vector2(posicao_atual_tiro.x, posicao_atual_tiro.y)
    
    tiros = lista_tiros
    if pode_atirar:
        tiros.append(nova_posicao_tiro)
    
    for index, tiro in enumerate(tiros):
        if tiro.x > 0:
            screen.blit(bala, (tiro.x, tiro.y))
        else:
            tiros.pop(index)

        time_passed_tiro = clock.tick(30)
        segundos_tiro = time_passed_tiro/1000.0
        
        tiro.x -= 150 * segundos_tiro 

def temporizador_tiro(tempo_tiro, pode_atirar):
    time_tiro = clock.tick(30)
    segundos_tiro2 = time_tiro/1000.0

    tempo_tiro+= segundos_tiro2
    if tempo_tiro > 0.6:
        pode_atirar = True
        tempo_tiro = 0
    return (tempo_tiro, pode_atirar)





while True: 
    
    screen.blit(background, (0, 0))
    screen.blit(nave, (posicao_fogete.x, posicao_fogete.y))
    screen.blit(alien, (posicao_alien.x, posicao_alien.y))

    lanca_tiro(posicao_tiro, lista_tiros, pode_atirar)
    pode_atirar = False

    posicao_alien, direction_alien = movimento_alien(posicao_alien, direction_alien)
    posicao_tiro = posicao_alien
    posicao_fogete = movimento_foguete(posicao_fogete)
    
    verifica_jogo_fechado()

    tempo_tiro, pode_atirar = temporizador_tiro(tempo_tiro, pode_atirar)
    
    
    
    pygame.display.update()


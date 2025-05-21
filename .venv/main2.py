import pygame
import math
import random
from pygame import mixer

# Inicializar pygame
pygame.init()

# Crear la pantalla
screen = pygame.display.set_mode((800, 600))

# Fondo
background = pygame.image.load('background.jpg')

# Música de fondo
mixer.music.load('background.wav')
mixer.music.play(-1)

# Título e ícono
pygame.display.set_caption("Space Invaders - Modo Grupal")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Jugadores
player1Img = pygame.image.load('player.png')
player1X = 300
player1Y = 480
player1X_change = 0

player2Img = pygame.image.load('player.png')
player2X = 500
player2Y = 480
player2X_change = 0

# Enemigos
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.1)
    enemyY_change.append(40)

# Balas de ambos jugadores
bulletImg = pygame.image.load('bullet.png')
bullet1X = 0
bullet1Y = 480
bullet1X_change = 0
bullet1Y_change = 10
bullet1_state = "ready"

bullet2X = 0
bullet2Y = 480
bullet2X_change = 0
bullet2Y_change = 10
bullet2_state = "ready"

# Puntajes
score_value_player1 = 0
score_value_player2 = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Texto de Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score():
    score = font.render(f"Player 1: {score_value_player1}   Player 2: {score_value_player2}", True, (0, 255, 0))
    screen.blit(score, (10, 10))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

def player(x, y, img):
    screen.blit(img, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y, bullet_state):
    screen.blit(bulletImg, (x + 16, y + 10))
    return "fire"

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

# Bucle principal del juego
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movimiento del jugador 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player1X_change = -1
            if event.key == pygame.K_d:
                player1X_change = 1
            if event.key == pygame.K_w and bullet1_state == "ready":
                bullet1X = player1X
                bullet1_state = fire_bullet(bullet1X, bullet1Y, bullet1_state)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player1X_change = 0

        # Movimiento del jugador 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player2X_change = -1
            if event.key == pygame.K_RIGHT:
                player2X_change = 1
            if event.key == pygame.K_UP and bullet2_state == "ready":
                bullet2X = player2X
                bullet2_state = fire_bullet(bullet2X, bullet2Y, bullet2_state)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player2X_change = 0

    # Actualizar posiciones de los jugadores
    player1X += player1X_change
    player1X = max(0, min(player1X, 736))

    player2X += player2X_change
    player2X = max(0, min(player2X, 736))

    # Movimiento de enemigos
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = abs(enemyX_change[i])
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -abs(enemyX_change[i])
            enemyY[i] += enemyY_change[i]

        # Colisiones con jugador 1
        if isCollision(enemyX[i], enemyY[i], bullet1X, bullet1Y):
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bullet1Y = 480
            bullet1_state = "ready"
            score_value_player1 += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Colisiones con jugador 2
        if isCollision(enemyX[i], enemyY[i], bullet2X, bullet2Y):
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bullet2Y = 480
            bullet2_state = "ready"
            score_value_player2 += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Movimiento de balas
    if bullet1_state == "fire":
        fire_bullet(bullet1X, bullet1Y, bullet1_state)
        bullet1Y -= bullet1Y_change
        if bullet1Y <= 0:
            bullet1Y = 480
            bullet1_state = "ready"

    if bullet2_state == "fire":
        fire_bullet(bullet2X, bullet2Y, bullet2_state)
        bullet2Y -= bullet2Y_change
        if bullet2Y <= 0:
            bullet2Y = 480
            bullet2_state = "ready"

    player(player1X, player1Y, player1Img)
    player(player2X, player2Y, player2Img)
    show_score()
    pygame.display.update()

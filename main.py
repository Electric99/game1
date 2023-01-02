import pygame
import random
import math
from pygame import mixer

#Intialize the game:
pygame.init()

#screen:
screen = pygame.display.set_mode((800, 600))

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


#Title and Icon
pygame.display.set_caption("Battle Thing")
icon = pygame.image.load('arcade-game.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('tank.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#Soldier
soldierImg = []
soldierX = []
soldierY = []
soldierX_change = []
soldierY_change = []
num_of_soldiers = 15

for i in range(num_of_soldiers):
    soldierImg.append(pygame.image.load('soldier.png'))
    soldierX.append(random.randint(0, 736))
    soldierY.append(random.randint(50, 150))
    soldierX_change.append(0.1)
    soldierY_change.append(15)

#Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 28)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 56)

#Blast Radius
blast_radius = 27


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))

def game_win():
    over_text = over_font.render("VICTORY", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def soldier(x, y, i):
    screen.blit(soldierImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 20, y + 10))


def isCollision(soldierX, soldierY, bulletX, bulletY):
    distance = math.sqrt(math.pow(soldierX - bulletX, 2) + (math.pow(soldierY - bulletY, 2)))
    if distance < blast_radius:
        return True
    else:
        return False


ke_received = False
k9_received = False

#Game loop
running = True
while running:

    # RGB-red,green,blue
    screen.fill((7, 145, 7))

    # reset after super blast
    blast_radius = 27

    #Win
    if score_value>=50:
        game_win()
        soldierX=[]
        soldierY=[]
        num_of_soldiers=0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #If a keystroke is pressed check whether it's right or left or up or down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_UP:
                playerY_change = -0.2
            if event.key == pygame.K_DOWN:
                playerY_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_e:
                if k9_received:
                    blast_radius = 1000000000000
                else:
                    ke_received = True
            if event.key == pygame.K_9:
                if ke_received:
                    blast_radius = 1000000000000
                else:
                    k9_received = True

                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
            if event.key == pygame.K_e:
                ke_received = False
            if event.key == pygame.K_9:
                k9_received = False

    playerY += playerY_change
    playerX += playerX_change
#Boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # enemy movement
    for i in range(num_of_soldiers):

        #game over
        if soldierY[i] > 440:
            for j in range(num_of_soldiers):
                soldierY[j] = 2000
            game_over_text()
            break



        soldierX[i] += soldierX_change[i]
        if soldierX[i] <= 0:
            soldierX_change[i] = 0.1
            soldierY[i] += soldierY_change[i]
        elif soldierX[i] >= 736:
            soldierX_change[i] = -0.1
            soldierY[i] += soldierY_change[i]
        #Collision
        collision = isCollision(soldierX[i], soldierY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            soldierX[i] = random.randint(0, 735)
            soldierY[i] = random.randint(50, 400)
            
        soldier(soldierX[i], soldierY[i], i)

#Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

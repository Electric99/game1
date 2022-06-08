import pygame
import random
import math
#Intialize the game:
pygame.init()

#screen:
screen = pygame.display.set_mode((800, 600))

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
soldierImg = pygame.image.load('soldier.png')
soldierX = random.randint(0, 735)
soldierY = random.randint(50, 735)
soldierX_change = 0.1
soldierY_change = 15

#Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

score = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


def soldier(x, y):
    screen.blit(soldierImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 20, y + 10))


def isCollision(soldierX, soldierY, bulletX, bulletY):
    distance = math.sqrt((math.pow(soldierX-bulletX, 2)) + (math.pow(soldierY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


#Game loop
running = True
while running:

    # RGB-red,green,blue
    screen.fill((7, 145, 7))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #If a keystroke is pressed check whether it's right or left
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
                if bullet_state is "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

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

    soldierX += soldierX_change
    # Boundaries
    if soldierX <= 0:
        soldierX_change = 0.1
        soldierY += soldierY_change
    elif soldierX >= 736:
        soldierX_change = -0.1
        soldierY += soldierY_change

#Bullet Movement
    if bulletY <= 0:
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

#Collision
    collision = isCollision(soldierX, soldierY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score += 1
        print(score)
        soldierX = random.randint(0, 735)
        soldierY = random.randint(50, 735)

    player(playerX, playerY)
    soldier(soldierX, soldierY)
    pygame.display.update()

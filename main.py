# TODO-- Play Again, Highest Score...
import pygame
import random
import math
from pygame import mixer

pygame.init()
mixer.init()
screen = pygame.display.set_mode((800, 600))  # Width, Height

background = pygame.image.load("resources/SpaceBg.png")
mixer.music.load("resources/background.wav")
mixer.music.play(-1)
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("resources/logo.png")
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load("resources/Shooter.png")
playerX = 370
playerY = 480
playerXChange = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load("resources/Invader.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(2)
    enemyYChange.append(40)

# Bullet
bulletImg = pygame.image.load("resources/bullet.png")
bulletX = 0
bulletY = 480
bulletYChange = 10
bulletState = "ready"
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# GameOver
gameOverFont = pygame.font.Font("freesansbold.ttf", 64)


def showScore(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameOver():
    gOverText = gameOverFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gOverText, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # Draws the playerImg on screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # Draws the enemyImg on screen


def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    x = math.pow(enemyX - bulletX, 2)
    y = math.pow(enemyY - bulletY, 2)
    distance = math.sqrt(x + y)
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 255, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

        if event.type == pygame.KEYDOWN:  # Pressing any key
            if event.key == pygame.K_LEFT:
                playerXChange = -5
            if event.key == pygame.K_RIGHT:
                playerXChange = 5
            if event.key == pygame.K_SPACE:
                bulletSound = mixer.Sound("resources/laser.wav")
                bulletSound.play()
                if bulletState == "ready":
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # Releasing the pressed key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0

    # Boundary player
    playerX += playerXChange
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    # Boundary enemy
    for i in range(numOfEnemies):
        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyXChange[i]
        if enemyX[i] <= 0:
            enemyXChange[i] = 2
            enemyY[i] += enemyYChange[i]
        elif enemyX[i] >= 736:
            enemyXChange[i] = -2
            enemyY[i] += enemyYChange[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("resources/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bulletState = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735 - i)
            enemyY[i] = random.randint(50 - i, 150 - i)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
pygame.quit()

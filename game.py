from pygame import mixer
import pygame
import math
import random
import os
import sys

# hides the pygame message in terminal
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# initializations
pygame.init()
SCREEN_LENGTH = 800
SCREEN_WIDTH = 600
POINTS_TO_WIN = 5

# window size set up
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH))

# get backround image
background = pygame.image.load('./images/black_background.jpeg')

# sound effects
mixer.music.load("./sounds/corona_background_song.mp3")

# loop music forever
mixer.music.play(-1)

# header for game screen
pygame.display.set_caption("CORONA KILLER")

# initial player settings and coordinates
player_image = pygame.image.load('./images/player.png')
playerX = 375
playerY = 490
playerX_change = 0

# enemy settings & coordinates
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies_num = 5

# bullet settings and state
bulletImg = pygame.image.load('./images/bullet.png')
bulletX = 0
bulletY = 475
bulletX_change = 0
bulletY_change = 10

# set state to ready
bullet_state = "ready"

# points score and font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 35)

# where to display points on the screen
points_xcoordinate = 10
points_ycoordinate = 10

# ending message
win_font = pygame.font.Font('freesansbold.ttf', 64)
end_font = pygame.font.Font('freesansbold.ttf', 64)


# show points on the top left of the screen
def show_points(points_xcoordinate, points_ycoordinate):
    score = font.render("Points: " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (points_xcoordinate, points_ycoordinate))


# display game over message once you lose
def game_over_message():
    font = pygame.font.Font(None, 35)
    text = font.render(
        "LOSER! PRESS 'ENTER' TO PLAY AGAIN. 'Q' TO QUIT", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_LENGTH/2, SCREEN_WIDTH/2))
    screen.blit(text, text_rect)
    mixer.music.stop()
    # to select play again
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            os.execv(sys.executable, ['python'] + sys.argv)
        if event.key == pygame.K_q:
            pygame.quit()
            running = False
            sys.exit()


# display game winning message
def winning_message():
    font = pygame.font.Font(None, 40)
    text = font.render(
        "YOU WIN! PRESS 'ENTER' TO PLAY AGAIN. 'Q' TO QUIT", True, (0, 255, 0))
    text_rect = text.get_rect(center=(SCREEN_LENGTH/2, SCREEN_WIDTH/2))
    screen.blit(text, text_rect)
    mixer.music.stop()
    # to select play again
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            os.execv(sys.executable, ['python'] + sys.argv)
        if event.key == pygame.K_q:
            pygame.quit()
            running = False
            sys.exit()


# display player object
def player(x, y):
    screen.blit(player_image, (x, y))


# display enemy object
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# display bullet object
def shoot_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


# collision math - to determine if there is a collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    # distance formula
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) +
                         (math.pow(enemyY - bulletY, 2)))
    if distance < 26:
        return True
    else:
        return False


# RUNNER CODE
# to display onto screen virus images
for i in range(enemies_num):
    # enemy_img.append(pygame.image.load('enemy.png'))
    enemy_img.append(pygame.image.load('./images/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(45, 140))
    enemyX_change.append(4)
    enemyY_change.append(40)

# game keeps running till you WIN or LOSE
running = True
while running:

    # fill the screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # player triggered events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # deciding movements: left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # release bullet sound effect if ready
                    bulletSound = mixer.Sound("./sounds/shoot.wav")
                    bulletSound.play()
                    bulletX = playerX
                    shoot_bullet(bulletX, bulletY)
            if event.key == pygame.K_q:
                running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # changes player horizontal location
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movements
    for i in range(enemies_num):
        # decides when the game is over
        if enemyY[i] > 440:
            for j in range(enemies_num):
                enemyY[j] = 2000
            if score_value != POINTS_TO_WIN:
                game_over_message()
            break

        # horizontal virus movements
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # play sound when hit
            explosionSound = mixer.Sound("./sounds/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            # provide new random location for the virus image
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # if your current score is 5 then you win
        if score_value == POINTS_TO_WIN:
            winning_message()
            break
        else:
            # display virus image onto the screen
            enemy(enemyX[i], enemyY[i], i)

    # bullet movements depending on state
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        shoot_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if score_value == POINTS_TO_WIN:
        winning_message()

    # functions
    player(playerX, playerY)
    show_points(points_xcoordinate, points_ycoordinate)
    # update portions of screen
    pygame.display.update()

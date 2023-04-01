import os
import sys
import pygame
import random

pygame.init()

# screen
screen_width = 300
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("game (jonathan edition)")

# BGM
pygame.mixer.init()

musicFiles = ['./assets/audio/blank.mp3',
              './assets/audio/on.mp3', './assets/audio/beast.mp3']
# set the end event for the music
currentSong = 0
pygame.mixer.music.load(musicFiles[currentSong])
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

pygame.display.set_icon(pygame.image.load('./assets/imgs/jonathan.png'))

# * Variables

# Audio Variables
boom = pygame.mixer.Sound('./assets/audio/boom.mp3')

# Player Variables
player_size = 60
player_x = 0
player_y = screen_height - player_size
playerSpeed = 5

# Image Variables
playerImg = pygame.image.load('./assets/imgs/jonathan.png')
bgimg = pygame.image.load("./assets/imgs/forest2.jpg")
harmlessImg = pygame.image.load("./assets/imgs/tyler.png")
dangerImg = pygame.image.load("./assets/imgs/carlson.png")
# Shape Variables
shapes = []
shape_size = 20
shape_speed = 5
shape_timer = 0
shape_spawn_time = 600  # milliseconds between shape spawns
# Score Variables
font = pygame.font.Font(None, 36)
score = 0
scoreText = font.render(f"Score: {score}", True, (255, 255, 255))
# Other Variables
clock = pygame.time.Clock()
dead = False
# game loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not pygame.mixer.music.get_busy():
            # Stop the current music
            pygame.mixer.music.stop()

        # Load and play the next music file
            currentSong = (currentSong + 1) % len(musicFiles)
            pygame.mixer.music.load(musicFiles[currentSong])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    keys = pygame.key.get_pressed()

    screen.blit(bgimg, (0, 0))
    screen.blit(playerImg, (player_x, player_y))

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= playerSpeed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += playerSpeed

    if dead:
        score = 0
        screen.blit(scoreText, (300, 10))
        shapes.clear()
        player_x = 0
        player_y = screen_height - player_size
        pygame.time.wait(3000)
        dead = False

    # update shapes
    shape_timer += clock.get_time()
    if shape_timer >= shape_spawn_time:
        shape_timer = 0
        shape_x = random.randint(0, screen_width - shape_size)
        shape_y = 0
        # 70% chance of harmless shape, 40% chance of dangerous shape
        shape_img = harmlessImg if random.random() < 0.5 else dangerImg
        shape_rect = shape_img.get_rect(topleft=(shape_x, shape_y))
        shapes.append((shape_rect, shape_img))

    # move and draw shapes
    for shape in shapes:
        shape_rect, shape_img = shape
        shape_rect.move_ip(0, shape_speed)
        screen.blit(shape_img, shape_rect)

    # check for collisions
    for shape in shapes:
        shape_rect, shape_img = shape
        if player_x + player_size > shape_rect.left and player_x < shape_rect.right and player_y + player_size > shape_rect.top and player_y < shape_rect.bottom:
            if shape_img == dangerImg:
                dead = True
            else:
                boom.play()

                shapes.remove(shape)
                score += 1
                scoreText = font.render(
                    f"Score: {score}", True, (255, 255, 255))

    # display the score
    screen.blit(scoreText, (10, 10))

    # update the screen
    pygame.display.flip()

    # control the frame rate
    clock.tick(60)

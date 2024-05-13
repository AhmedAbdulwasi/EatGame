import pygame
import sys
import os
import random
import pygame.mixer


#initialize pygame, fonts and pygame.mixer
pygame.init()
pygame.font.init()
pygame.mixer.init()


# window, constants, fonts, images, variables and sound effects (MAKE SURE TO OPEN ASSETS FOLDER FIRST THEN THE GAME)
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eat!")
FPS = 60
VEL = 12
FOOD_VEL = 8
PLAYER_IMAGE = pygame.image.load(os.path.join("player.png"))
PLAYER = pygame.transform.scale(PLAYER_IMAGE, (150, 100))
FOOD_IMAGE = pygame.image.load(os.path.join("food.png"))
FOOD = pygame.transform.scale(FOOD_IMAGE, (30, 30))
NOTFOOD_IMAGE = pygame.image.load(os.path.join("notfood.png"))
NOTFOOD = pygame.transform.scale(NOTFOOD_IMAGE, (30, 30))
BOMB_IMAGE = pygame.image.load(os.path.join("bomba.png"))
BOMB = pygame.transform.scale(BOMB_IMAGE, (80, 80))
SCORE = 0
FONT = pygame.font.Font("font.ttf", 30)
#btw I created the sound effect so forgive me if you can hear a little background noise.
BOMB_SOUND = pygame.mixer.Sound(os.path.join("bomba.wav"))
FOOD_SOUND = pygame.mixer.Sound(os.path.join("fooded.wav"))
NOTFOOD_SOUND = pygame.mixer.Sound(os.path.join("notfooded.wav"))






# initialize game objects
player_movement = pygame.Rect(360, 590, 150, 100)
food_rect = FOOD.get_rect()
food_rect.x = random.randint(0, WIDTH - food_rect.width) # we're gonna randomly generate food at different x positions
food_rect.y = -50 # we don't need to randomly generate y positions because the food will always start off of the screen which is -50
notfood_rect = NOTFOOD.get_rect()
notfood_rect.x = random.randint(0, WIDTH - notfood_rect.width)
notfood_rect.y = -50
bomb_rect = BOMB.get_rect()
bomb_rect.x = random.randint(0, WIDTH - bomb_rect.width)
bomb_rect.y = -50
pygame.display.set_icon(FOOD)

# start screen
def start_screen():
    WIN.fill((250,250,250))
    Press_Start = FONT.render("Press SPACE twice to start", True, (0,0,0))
    made_by = FONT.render("Made by: Ahmed Bein", True, (0,0,0))
    WIN.blit(Press_Start, (WIDTH/2 - Press_Start.get_width()/2, HEIGHT/2 - Press_Start.get_height()/2))
    WIN.blit(made_by, (WIDTH/2 - made_by.get_width()/2, HEIGHT/2 - made_by.get_height()/2 + 50))
    pygame.display.update()
    startedd = False
    while not startedd:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    SCORE = 0
                    startedd = True
                    reset_game()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    #pass
    
# drawing the window
def draw_window():
    WIN.fill((173, 216, 230)) # colour is light blue
    WIN.blit(PLAYER, (player_movement.x, player_movement.y)) # where the player will spawn
    WIN.blit(FOOD, (food_rect.x, food_rect.y)) #where the food will spawn
    WIN.blit(NOTFOOD, (notfood_rect.x, notfood_rect.y)) # where the notfood will spawn
    WIN.blit(BOMB, (bomb_rect.x, bomb_rect.y)) # where the bomb will spawn

    font = pygame.font.SysFont("roboto", 30) # This is a cool font and I will use it everytime
    score_text = font.render("SCORE: " + str(SCORE), True, (255, 255, 255))
    WIN.blit(score_text, (10, 10))
    pygame.display.update()
    #pass




# objects falling and collision with the player (my favourite part of the game)
def update_objects():
    global SCORE
    food_rect.move_ip(0, FOOD_VEL) # you can change speed of the food going down here
    notfood_rect.move_ip(0, FOOD_VEL)
    bomb_rect.move_ip(0, 12) # If it is too fast, change 12 to FOOD_VEL (which is 8)
    if food_rect.bottom > HEIGHT: # if the food is at the bottom of the screend and its bigger than HEIGHT, we're gonna randomly generate it again.
        food_rect.x = random.randint(0, WIDTH - food_rect.width)
        food_rect.y = -50
    if notfood_rect.bottom > HEIGHT: # same thing with this
        notfood_rect.x = random.randint(0, WIDTH - notfood_rect.width)
        notfood_rect.y = -50
    if bomb_rect.bottom > HEIGHT: # same thing with this
        bomb_rect.x = random.randint(0, WIDTH - bomb_rect.width)
        bomb_rect.y = -50
        
    # This is where I gained valuable knowledge of collisions and the effects of them. I will use this a lot in the fure
    if player_movement.colliderect(food_rect): # I love this, everytime the point is in the same coordinates as the player (collides), the score will increment by 1 and the food will randomly generate again
        SCORE += 1
        food_rect.x = random.randint(0, WIDTH - food_rect.width)
        food_rect.y = -50
        FOOD_SOUND.play()
    if player_movement.colliderect(notfood_rect): #same thing with this, but the score will decrement by 1
        SCORE -= 1
        notfood_rect.x = random.randint(0, WIDTH - notfood_rect.width)
        notfood_rect.y = -50
        NOTFOOD_SOUND.play()
    #pass




# player movements
def game_movements(key_pressed, player_movement): # A, D, LEFT, and RIGHT are the only keys that you can use to move the player
    if (key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]) and player_movement.x - VEL > 0: # LEFT
            player_movement.x -= VEL
    if (key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]) and player_movement.x + VEL < 735: # RIGHT
            player_movement.x += VEL


# Reset after gameover
def reset_game():
    global SCORE
    global restart_game
    SCORE = 0
    restart_game = False
    player_movement.x = 360
    player_movement.y = 590
    food_rect.x = random.randint(0, WIDTH - food_rect.width)
    food_rect.y = -50
    notfood_rect.x = random.randint(0, WIDTH - notfood_rect.width)
    notfood_rect.y = -50
    bomb_rect.x = random.randint(0, WIDTH - bomb_rect.width)
    bomb_rect.y = -50
    #pass



# game over screen
def game_over():
    global SCORE
    gameover_text = FONT.render("GAME OVER", True, (255, 255, 255))
    score_text = FONT.render("SCORE: " + str(SCORE), True, (255, 255, 255))
    restart_text = FONT.render("Press SPACE to restart", True, (255, 255, 255))
    # I might add a counter of how many times you got the + sign and - sign
    WIN.fill((0, 0, 0))
    WIN.blit(gameover_text, (WIDTH/2 - gameover_text.get_width()/2, HEIGHT/2 - gameover_text.get_height()/2 - 40))
    WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2 + score_text.get_height()/2 + -10))
    WIN.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, HEIGHT/2 + restart_text.get_height()/2 + 60))
    pygame.display.update()
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    SCORE = 0
                    restart = True
                    reset_game()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    #pass


# main loop
def main():
    global SCORE
    run = True
    clock = pygame.time.Clock()
    started = False

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
        key_pressed = pygame.key.get_pressed()
        # We call all the functions we made here
        if not started:
            start_screen()
        else:
            game_movements(key_pressed, player_movement)
            draw_window()
            update_objects()
            if player_movement.colliderect(bomb_rect):
                BOMB_SOUND.play()
                game_over()
            pygame.display.update()
        if key_pressed[pygame.K_SPACE] and not started:
            SCORE = 0
            started = True
            reset_game()
        
    pygame.quit()
    sys.exit()
if __name__ == "__main__": 
    main()

"""
Created on Wed Nov  27 02:08:31 2016

@author: Paschal
"""
import random, pygame, sys                                                          #import random for placing snake head and megaman head in random location
from pygame.locals import *                                                         #import sys for sys.exit (terminating function)

pygame.init()

#paschal
start_bgm = pygame.mixer.Sound("megaman.wav")                                       #importing visual and sound aspects of the program, such as the background music and backdrop
main_bgm = pygame.mixer.music.load("Dr.mp3")                                        #all are included in the folder    
crash_sound = pygame.mixer.Sound("snakecrash.wav")
eat_sound = pygame.mixer.Sound("snakeeat.wav")
bg = pygame.image.load("background.png")

UP = 'up'                                                                           #setting the arrow keys to variables
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#shrey
FPS = 15                                                                           #used to control game speed, 20 matches the pace of the music
width_of_window = 800                                                               #sets parameters of the window for the program
height_of_window = 540
c_size = 30                                                                         #sets size of each 'cell'(ie. width of each x interval) in program

#shrey
width_of_cell = int(width_of_window / c_size)                                       #since the cells are squares/rectangles, establishes the width and height for later use
height_of_cell = int(height_of_window / c_size)

#shrey
white       = (255, 255, 255)                                                       #sets colors using R, G, B format
black       = (  0,   0,   0)
red         = (255,   0,   0)
lightgreen  = ( 0, 255,  0)
lightblue   = ( 20,  20, 175)
grey  = ( 40,  40,  40)


snakehead = 0                                                                       #sets the snakehead index aka megaman head
megaman = pygame.image.load('megaman.png')                                          #imports megaman head sprite

#paschal
def press_key_message():                                                            #creates the 'Press and Key to start!' message in the bottom right of the start and game over screen
    press_key = ulti_font.render('Press any key to start!', True, white)
    press_key_window = press_key.get_rect()                                         #.get_rect to create the window/rectangle for the text to be in
    press_key_window.topleft = (width_of_window - 380, height_of_window - 40)

    display.blit(press_key, press_key_window)                                       #.blit in order to actually display it

#paschal
def key_press_test():                                                               #as said by the name, this function checks if the user inputs a key for the start/game over screen
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    user_key_input = pygame.event.get(KEYUP)
    if len(user_key_input) == 0:                                                    #have the program do nothing if no keys are pressed
        return None
    if user_key_input[0].key == K_ESCAPE:                                           #sets the ESC button as a way to close the program
        terminate()
    return user_key_input[0].key

#paschal and shrey
def start_screen():                                                                 #establishes the start screen

    startscreen = True
    pygame.mixer.Sound.play(start_bgm)                                              #plays the start screen music imported in the beginning

    while startscreen:
        press_key_message()                                                         #while in the start screen, the key test function and the prress key to start function are called
        if key_press_test():
            pygame.mixer.Sound.stop(start_bgm)                                      #stops music when a key is pressed, can be viewed as a transition into the next song
            pygame.event.get()
            return

        pygame.display.update()                                                     #updates the program display continuously
        FPSCLOCK.tick(FPS)

        display.fill(black)                                                         #setting all the windows of text
        final_project_font = pygame.font.Font('Airacobra Extra Bold.ttf', 95)
        final_project_font2 = pygame.font.Font('Airacobra Extra Bold.ttf', 32)
        final_project_font3 = pygame.font.Font('Airacobra Extra Bold.ttf', 48)
        ek128_text = final_project_font3.render('Thank you for playing.', True, white)
        press_key1 = ulti_font.render('Press ESC to exit', True, red)
        f_text = final_project_font.render('MEGASNAKE.P', True, white)
        p_text = final_project_font2.render('Created By: Paschal Igusti', True, lightblue,48)
        ek128_window = ek128_text.get_rect()
        pk_window = press_key1.get_rect()
        f_window = f_text.get_rect()
        p_window = p_text.get_rect()
        ek128_window.center = (width_of_window / 2, height_of_window / 1.5)
        f_window.center = (width_of_window / 2, height_of_window / 2)
        p_window.center = (width_of_window / 2, 15)
        pk_window.center = (width_of_window - 640, 518)

        display.blit(ek128_text, ek128_window)                                      #.blit used once again to actually display the created messages
        display.blit(f_text, f_window)
        display.blit(p_text, p_window)
        display.blit(press_key1, pk_window)


#paschal and shrey
def game_over_screen(): #same logistics as ths atrt screen, just different sized windows, no music, and different text
    g_over_font = pygame.font.Font('Airacobra Extra Bold.ttf',225)
    g_surf = g_over_font.render('Game', True, white)
    over_text = g_over_font.render('Over', True, white)
    game_window = g_surf.get_rect()
    over_window = over_text.get_rect()
    game_window.midtop = (width_of_window / 2, 10)
    over_window.midtop = (width_of_window / 2, game_window.height + 10 + 25)

    display.blit(g_surf, game_window)
    display.blit(over_text, over_window)
    press_key_message()
    pygame.display.update()
    pygame.time.wait(500)
    key_press_test()

    while True:
        if key_press_test():
            pygame.event.get()
            return

#shrey
def scoreboard(score):
    score_text = ulti_font.render('Score: %s' % (score), True, white)       #window that displays the score/amount of megaman ehads you have eaten
    score_window = score_text.get_rect()
    score_window.topleft = (width_of_window - 790, height_of_window - 40)
    display.blit(score_text, score_window)

#paschal
def b_ground():
    display.blit(bg, (0,0)) #background is an image imported earlier in the script, originally obtained from online

#paschal
def random_location():
    return {'x': random.randint(0, width_of_cell - 1), 'z': random.randint(0, height_of_cell - 1)}      #the function that is used to place the megaman head and the snake body at random locations

#shrey
def draw_snake(snake_coordinates):  #function used to draw the snake body
    for coord in snake_coordinates:
        x = coord['x'] * c_size     #uses cell size ti appropriate the head
        z = coord['z'] * c_size
        snake_segment = pygame.Rect(x, z, c_size, c_size)   #uses .rect to draw the square like figure of the snake body cells
        pygame.draw.rect(display, grey, snake_segment)
        snake_inner_segment = pygame.Rect(x + 4, z + 4, c_size - 8, c_size - 8)
        pygame.draw.rect(display, white, snake_inner_segment)

#paschal
def megaman_head(coord): #function used to define megaman head
    x = coord['x'] * c_size     #establishes the size of the cell of the megaman head
    z = coord['z'] * c_size
    #megamanRect = pygame.Rect(x, z, c_size, c_size)
    #pygame.draw.rect(display, lightblue, megamanRect)
    megamanthick = 30
    display.blit(megaman, (x,z))                    #uses sprite obtained from online, used GIMPY to remove white background and give it a transparent background

def main():
    global FPSCLOCK, display, ulti_font

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    display = pygame.display.set_mode((width_of_window, height_of_window))
    ulti_font = pygame.font.Font('Airacobra Extra Bold.ttf', 32)
    pygame.display.set_caption('MegaSnake')

    start_screen()
    while True:
        snake()
        game_over_screen()

#paschal and shrey
def snake():

    pygame.mixer.music.play(-1) #plays main music on a loop ((-1) plays it however many times necessary while the program runs))

    s_point_x = random.randint(5, width_of_cell - 6)    #sets a random point for the snake to start
    s_point_z = random.randint(5, height_of_cell - 6)
    snake_coordinates = [{'x': s_point_x,     'z': s_point_z},
                  {'x': s_point_x - 1, 'z': s_point_z},
                  {'x': s_point_x - 2, 'z': s_point_z}]
    direction = UP                                      #sets the initial direction the snake travels, can be varied by changing direction
    megaman = random_location()                         #sets the megaman head in a random location
    while True:

        #checks to see if the snake goes out of boundaries/hits the walls of the window

        if snake_coordinates[snakehead]['x'] == -1 or snake_coordinates[snakehead]['x'] == width_of_cell or snake_coordinates[snakehead]['z'] == -1 or snake_coordinates[snakehead]['z'] == height_of_cell:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(crash_sound)
            return #initializes game over

        #checks to see if snake head coordinates overlap with any of the snake body coordinates

        for snake_bod in snake_coordinates[1:]:
            if snake_bod['x'] == snake_coordinates[snakehead]['x'] and snake_bod['z'] == snake_coordinates[snakehead]['z']:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(crash_sound)
                return #initializes game over

        #checks to see if megaman head is eaten

        if snake_coordinates[snakehead]['x'] == megaman['x'] and snake_coordinates[snakehead]['z'] == megaman['z']:
            pygame.mixer.Sound.play(eat_sound)
            megaman = random_location()     #sets a new random location for the megaman head
        else:
            del snake_coordinates[-1]       #gets rid of snake tail cell from original position; creates the 'following' mechanism
        if direction == UP:
            newsnakehead = {'x': snake_coordinates[snakehead]['x'], 'z': snake_coordinates[snakehead]['z'] - 1} #adds a cell in the direction the snake is moving when a megaman head is eaten
        elif direction == DOWN:
            newsnakehead = {'x': snake_coordinates[snakehead]['x'], 'z': snake_coordinates[snakehead]['z'] + 1}
        elif direction == LEFT:
            newsnakehead = {'x': snake_coordinates[snakehead]['x'] - 1, 'z': snake_coordinates[snakehead]['z']}
        elif direction == RIGHT:
            newsnakehead = {'x': snake_coordinates[snakehead]['x'] + 1, 'z': snake_coordinates[snakehead]['z']}
        for event in pygame.event.get(): #essentially the main loop of the program
            if event.type == QUIT:          #handles event feedback
                terminate()
            elif event.type == KEYDOWN:     #handles keys that are pressed
                if (event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        snake_coordinates.insert(0, newsnakehead)           #initializes the rest of the necessary functions
        display.fill(black)
        b_ground()
        draw_snake(snake_coordinates)
        megaman_head(megaman)
        scoreboard(len(snake_coordinates) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#paschal and shrey
def terminate():
    pygame.quit()
    sys.exit()      #only purpose of importing sys

if __name__ == '__main__':
    main()

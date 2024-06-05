import pygame
import random
from sys import exit

# WINDOW
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Fruit Matching Game')
font = pygame.font.Font('font/VCR_OSD_MONO_1.001.ttf', 40)
sub_font = pygame.font.Font('font/VCR_OSD_MONO_1.001.ttf', 25)
clock = pygame.time.Clock()
bg_music = pygame.mixer.Sound('audio/background_music.mp3')
bg_music.set_volume(0.5)
bg_music.play(loops=-1)
game_active = False
start_time = 0
rows = 4
columns = 4
correct = []
options_list = []
board_list = []
new_board = True
first_choice = None
second_choice = None
matches = 0
show_time = 1000  # Time to show the fruits (in milliseconds)
show_timer = 0
win_time = None  # Variable to store the time when the player wins

# Load fruit images
fruit_images = [
    'graphics/grapes.png',
    'graphics/apple.png',
    'graphics/banana.png',
    'graphics/blueberry.png',
    'graphics/pear.png',
    'graphics/pineapple.png',
    'graphics/raspberry.png',
    'graphics/strawberry.png'
]

# Double the fruit list to make pairs
fruit_images *= 2

# Load and scale fruit images
fruits = [pygame.image.load(fruit).convert_alpha() for fruit in fruit_images]
fruits = [pygame.transform.smoothscale(fruit, (90, 90)) for fruit in fruits]

# Function to draw the background
def background():
    background_surf = pygame.image.load('graphics/background.webp').convert_alpha()
    background_rect = background_surf.get_rect()
    background_surf = pygame.transform.smoothscale(background_surf, (600, 600))
    screen.blit(background_surf, background_rect)

def text():
    title_surf = font.render('Fruit Matching Game', False, ('#FFCE9D'), ("#EE7E57"))
    title_rect = title_surf.get_rect(center=(300, 30))
    screen.blit(title_surf, title_rect)

    instructions_surf = sub_font.render('Match all the fruit to win!', False, ('#FFCE9D'), ("#EE7E57"))
    instructions_rect = instructions_surf.get_rect(center=(300, 65))
    screen.blit(instructions_surf, instructions_rect)

    global restart_rect
    restart_surf = font.render('Restart', False, ('#FFCE9D'), ("#EE7E57"))
    restart_rect = restart_surf.get_rect(center=(100, 570))
    screen.blit(restart_surf, restart_rect)

def start_screen_text():
    title_surf = font.render('Fruit Matching Game', False, ('#FFCE9D'), ("#EE7E57"))
    title_rect = title_surf.get_rect(center=(300, 250))
    screen.blit(title_surf, title_rect)

    start_surf = sub_font.render('Click anywhere on the screen to start', False, ('#FFCE9D'), ("#EE7E57"))
    start_rect = start_surf.get_rect(center=(300, 300))
    screen.blit(start_surf, start_rect)

def board():
    global board_list
    pygame.draw.rect(screen, ("#EE7E57"), (90, 120, 420, 420), 0, 6)
    board_list = []
    for i in range(columns):
        for j in range(rows):
            piece = pygame.draw.rect(screen, ('White'), [i * 100 + 100, j * 100 + 130, 90, 90], 0, 4)
            board_list.append(piece)

def display_time():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time  # time in milliseconds
    time_surf = sub_font.render(f'Time: {current_time}', False, ('#FFCE9D'), ("#EE7E57"))
    time_rect = time_surf.get_rect(center=(300, 100))
    screen.blit(time_surf, time_rect)
    return current_time

def generate_board():
    global options_list
    options_list = list(range(rows * columns // 2)) * 2
    random.shuffle(options_list)

# Draw the board and fruits
def draw_board():
    for i, rect in enumerate(board_list):
        if i in correct or i == first_choice or i == second_choice:
            screen.blit(fruits[options_list[i]], rect.topleft)
        else:
            pygame.draw.rect(screen, ('White'), rect, 0, 4)

# Check for matches
def check_match():
    global first_choice, second_choice, show_timer, matches, correct, win_time
    if options_list[first_choice] == options_list[second_choice]:
        correct.extend([first_choice, second_choice])
        matches += 1
        first_choice = None
        second_choice = None
        if matches == len(options_list) // 2:  # Check if the player has won
            win_time = int(pygame.time.get_ticks() / 1000) - start_time
    else:
        show_timer = pygame.time.get_ticks()

# Hide unmatched fruits after a delay
def hide_unmatched():
    global first_choice, second_choice
    if pygame.time.get_ticks() - show_timer > show_time:
        first_choice = None
        second_choice = None

# Reset the game
def reset_game():
    global game_active, start_time, new_board, matches, correct, board_list, first_choice, second_choice, win_time
    game_active = True
    start_time = int(pygame.time.get_ticks() / 1000)
    new_board = True
    matches = 0
    correct = []
    board_list = []
    first_choice = None
    second_choice = None
    win_time = None

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_active:
                reset_game()
            elif matches == len(options_list) // 2:
                if play_again_rect.collidepoint(event.pos):
                    reset_game()
            elif restart_rect.collidepoint(event.pos):
                reset_game()
            else:
                for i, rect in enumerate(board_list):
                    if rect.collidepoint(event.pos) and i not in correct:
                        if first_choice is None:
                            first_choice = i
                        elif second_choice is None and i != first_choice:
                            second_choice = i
                            check_match()

    if game_active:
        if new_board:
            generate_board()
            new_board = False
        background()
        text()
        board()
        draw_board()
        elapsed_time = display_time()
        if first_choice is not None and second_choice is not None:
            hide_unmatched()

        # Check if all fruits are matched
        if matches == len(options_list) // 2:
            background()
            win_surf = font.render('You Win!', False, ('#FFCE9D'), ('#EE7E57'))
            win_rect = win_surf.get_rect(center=(300, 250))
            screen.blit(win_surf, win_rect)

            elapsed_time_surf = sub_font.render(f'Time Taken: {win_time} seconds', False, ('#FFCE9D'), ('#EE7E57'))
            elapsed_time_rect = elapsed_time_surf.get_rect(center=(300, 300))
            screen.blit(elapsed_time_surf, elapsed_time_rect)

            play_again_surf = sub_font.render('Play Again?', False, ('#FFCE9D'), ('#EE7E57'))
            play_again_rect = play_again_surf.get_rect(center=(300, 350))
            screen.blit(play_again_surf, play_again_rect)
    else:
        background()
        start_screen_text()

    pygame.display.update()
    clock.tick(60)

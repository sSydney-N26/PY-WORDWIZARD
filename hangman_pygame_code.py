import pygame, sys
import random
import math


# Setup Game Diplay
pygame.init()
WIDTH = 900
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # initialize full screen game window
pygame.display.set_caption("Welcome to the Hangman Game!")

# Initialize RGB colors used.
screen_color = (255,245,238)

# Store Hangman Stages:
stages = []
for i in range (8):
    hangman_stage = pygame.image.load("hangman_stage" + str(i) + ".png")
    stages.append(hangman_stage)

# set hangman status:
hangman_stage = 0

# Get random word from external Notepad document.
word = random.choice(open("word_list.txt").read().split()) 


# Make 26 square buttons:
# Button Variables
RADIUS = 25
GAP = 20
letters = []  # Example: [80, 550, "A", True] represents coordinates, letter
              # and boolean value representing whether the button is still
              # visible or not.
startX = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2) 
startY = 550
A = 65

def posButton():
    for i in range(26):
        x = startX + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))  
                   # add GAP to create space at the start and end on screen.
        y = startY + ((i // 13) * (GAP + RADIUS * 2))
                   # i // 13 is floor of i/13.
        letters.append([x, y, chr(A + i), True])  
        # character representation of A + i throughout for loop
posButton()
# Button Fonts:
font = pygame.font.SysFont("Arial", 40)
display_font = pygame.font.SysFont("Calibri", 60)
title_font = pygame.font.SysFont("Calibri", 75)
guessed_letters = ["D"]

# Display on Screen:
def draw():
    # Change game window color
    screen.fill(screen_color)

    # Display Title:
    title = title_font.render("HANGMAN PGAME", 1, (128,0,0))
    screen.blit(title, (180, 80))
    # Draw Word:
    word_completed = ""
    for letter in word:
        if letter in guessed_letters:
            word_completed += letter + " "
        else:
            word_completed += "_ "   # If you haven't guessed the letter.
    text = display_font.render(word_completed, 1, (0, 0, 0))   # How to display text on screen.
    screen.blit(text, (430, 350))

    # Draw Buttons
    button_colour = (105,105,105)
    for letter in letters:
        x, y, ltr, pressed = letter   # letter obtains from list.
        if pressed:
            pygame.draw.circle(screen, button_colour, (x, y), RADIUS, 4)
        # draw circle on screen using button_colour at position (x, y)
        # with dimension SIDE x SIDE (45 x 45) and line thickness = 4.
            text = font.render(ltr, 1, (0, 0, 0))
            screen.blit(text, (x - text.get_width()/2, y - text.get_height()/2))   
        # Draw text on screen at position x, y adjusted to center of buttons

    screen.blit(stages[hangman_stage], (200, 200))
    pygame.display.update()   # update to upload hangman status.
    
# Function to display message to user after game is done.
def display_message(message):
    new_screen_colour = (255, 228, 225)
    screen.fill(new_screen_colour)
    text = font.render(message, 2, (0, 0, 0))
    screen.blit(message, (160, 300))
    pygame.display.update()  # Update Game Status
    pygame.time.delay(3000)  # 3000 milliseconds or 3 seconds

def gameLoop():
    global hangman_stage

    game_speed = 60   # set game FPS
    fpsClock = pygame.time.Clock()
    guessed = True
    
    while guessed:
        fpsClock.tick(game_speed)  # game runs at speed set. 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                guessed = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, pressed = letter
                    if pressed:
                        distance = math.sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
                        if distance < RADIUS:
                            letter[3] = False   # modify boolean value stored wih each letter when pressed.
                            guessed_letters.append(ltr)  # if clicked, append letter to guessed letters list.
                            if ltr not in word:
                                hangman_stage += 1
        won = True
        for letter in word:
            if letter not in guessed_letters:
                won = False
                break
        
        if won:
            display_message("You guessed the correct word. You WON!!")
            break
        
        if hangman_stage == 7:
            display_message("You didn't guess the correct word. Try again next time. Good luck!")
        draw()
    pygame.quit()

gameLoop()




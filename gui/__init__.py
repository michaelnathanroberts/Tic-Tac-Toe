"""
The visual Tic-Tac-Toe game.
"""
# Author: Michael Roberts
# Date: 8 June 2021
# File: tictactoe\gui\main.py

from tictactoe.gui.box import Box, BoxGroup
from tictactoe.gui.button import Button, ButtonText

from tictactoe.core.enums import *
from tictactoe.core.board import Board, Combination, wins
from tictactoe.core.cpu_database_builder import build

from copy import copy
from pickle import load
from typing import Optional

import tictactoe.gui.colors as colors
import tictactoe.gui.pysound as pysound

import random
import os
import pygame



def load_resources() -> None:
    pygame.init()

    global size, screen
    global paper, font, small_font
    global pregame_music, game_music, win_music, draw_music, lose_music
    global quit, clock, board, bg, level
    global quit_button, replay_button
    global easy_button, medium_button, hard_button, impossible_button

    if __name__ != "__main__":
        os.chdir("\\".join(__file__.split("\\")[:-1]))

    size = [700, 500]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tic Tac Toe")

    paper = pygame.image.load("paper.png")
    font = pygame.font.Font("C:\\Windows\\Fonts\\georgia.ttf", 50)
    small_font = pygame.font.Font("C:\\Windows\\Fonts\\georgia.ttf", 20)
    pregame_music = pysound.Sound("anewbeginning.mp3")
    game_music = pysound.Sound("creativeminds.mp3")
    win_music = pysound.Sound("happyrock.mp3")
    draw_music = pysound.Sound("acousticbreeze.mp3")
    lose_music = pysound.Sound("memories.mp3")

    quit = False # this is a Boolean variable to control the while loop
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock() # this controls how fast the game runs

    board = Board()
    bg = BoxGroup(175, 175)

    level = Level.Impossible


    replay_button = Button(screen, ButtonText(small_font, "Play Again", 30, 15, colors.Purple, None),
                           500, 25, 150, 50, colors.Aquamarine)
    quit_button = Button(screen, ButtonText(small_font, "Quit", 50, 15, colors.Azurite, None),
                         500, 100, 150, 50, colors.HotPink)

    easy_button = Button(screen, ButtonText(small_font, "Easy", 50, 15, colors.Coral, None),
                         200, 100, 150, 50, colors.Green)
    medium_button = Button(screen, ButtonText(small_font, "Medium", 40, 15, colors.DarkCyan, None),
                         200, 200, 150, 50, colors.Yellow)
    hard_button = Button(screen, ButtonText(small_font, "Hard", 50, 15, colors.DarkKhaki, None),
                         200, 300, 150, 50, colors.Red)
    impossible_button = Button(screen, ButtonText(small_font, "Impossible", 20, 15, colors.Cyan, None),
                         200, 400, 150, 50, colors.Maroon)



def write_text(screen: pygame.Surface, font: pygame.font.Font, text: str, x: int, y: int, 
               color: colors.ColorType, background: Optional[colors.ColorType] = None):
    "Write text to a Pygame screen."
    text = font.render(text, False, color, background)
    screen.blit(text, [x, y])


def build_cpu_database() -> None:
    """
    Build the CPU database, if unbuilt.
    """
    build(False)  
    
def main_menu():
    """
    Implement the main menu
    """
    global quit
    pregame_music.play()
    done = False
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # go through every event in game (mouse etc)
            if event.type == pygame.QUIT: # if the user clicks the x on the window it will close
                done = True
                quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                global level
                if easy_button.hovering():
                    level = Level.Easy
                elif medium_button.hovering():
                    level = Level.Medium
                elif hard_button.hovering():
                    level = Level.Hard
                elif impossible_button.hovering():
                    level = Level.Impossible
                done = True
        # --- Game logic should go here
        # --- Screen-clearing code goes here
        screen.blit(paper, [0, 0])
        # --- Drawing code should go here
        write_text(screen, font, "Tic-Tac-Toe!!!", 150, 20, colors.Orange)
        easy_button.draw()
        medium_button.draw()
        hard_button.draw()
        impossible_button.draw()
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # --- Limit to 30 frames per second
        clock.tick(30) # write now the clock is running at 30 frames per second
        # if I changed it to 40 the game would run faster
        # if I change it to 20 the game would run slower      
     
    
    

def init() -> None:
    """
    Initalize game by selecting symbol and loading database.
    This function should end by calling the prepare() function.
    """
    # Note: This is a weird name for this function. It takes its name
    # from its counterpart in tictactoe.cmd.Game.init(self)
    global quit
    x_box = Box(100, 250, -2, Symbol.X)
    o_box = Box(500, 250, -1, Symbol.O)
    done = False
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # go through every event in game (mouse etc)
            if event.type == pygame.QUIT: # if the user clicks the x on the window it will close
                done = True
                quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if x_box.hovered():
                    prepare(Symbol.X)
                    done = True
                elif o_box.hovered():
                    prepare(Symbol.O)
                    done = True
        # --- Game logic should go here
        # --- Screen-clearing code goes here
        screen.blit(paper, [0, 0])
        # --- Drawing code should go here
        write_text(screen, font, "Tic-Tac-Toe!!!", 150, 100, colors.Orange)
        write_text(screen, small_font, "Select a symbol.", 100, 400, colors.Chartreuse)
        x_box.draw(screen)
        o_box.draw(screen)
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # --- Limit to 30 frames per second
        clock.tick(30) # write now the clock is running at 30 frames per second
        # if I changed it to 40 the game would run faster
        # if I change it to 20 the game would run slower 
    pregame_music.stop()
    

def prepare(user_symbol: Symbol):
    """
    Assign the provided symbol to the user, the other to the computer.
    Load the appropriate database for the computer's use.
    """
    build_cpu_database()
    
    Player.User.assign(user_symbol)
    if Player.Computer.symbol == Symbol.X:
        file = open("cpudata1.txt", "rb")
    else:
        file = open("cpudata2.txt", "rb")
    global database
    database = load(file)

def get_user_input() -> int:
    """Return the index requested by the user.
        
        The index represents the position on the board
        the user desires to go and it should be an integer,
        between 0 and 8, inclusive.
        """
    global quit
    while not quit:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                game_music.stop()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                slot = bg.hovered_slot()
                if isinstance(slot, int):
                    return slot
        # --- Game logic should go here
        # --- Screen-clearing code goes here
        screen.blit(paper, [0, 0])
        # --- Drawing code should go here
        bg.draw(screen)
        write_text(screen, font, "Tic-Tac-Toe!!!", 150, 20, colors.Orange)
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # --- Limit to 30 frames per second
        clock.tick(30) # write now the clock is running at 30 frames per second
        # if I changed it to 40 the game would run faster
        # if I change it to 20 the game would run slower
        
def write_user_input(index: int) -> bool:
        """Write the user's symbol to the provided index on the game's
        tic-tac-toe board. The index should be a number between
        0 and 8, inclusive.
        
        This function will return True if the write was sucessful,
        False otherwise.
        """
        # Write input to the board and update the BoxGroup and return True,
        # Otherwise, do nothing and return False
        if isinstance(index, int) and 0 <= index < 9:
            symbol = board[index]
            if symbol is None:
                board[index] = Player.User.symbol
                bg.update(board)
                return True
        return False
    
def user_turn():
    """
    Define one user turn. 
    
    Request an index from the user and attempt to write the user's symbol
    to the index on the tic-tac-toe board. Keep requesting an index from the 
    user until a write is sucessful. 
    """
    successful = False
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global quit
            quit = True
            return
    # --- Game logic should go here
    while not successful and not quit:
        index = get_user_input()
        successful = write_user_input(index)
    # --- Screen-clearing code goes here
    screen.blit(paper, [0, 0])
    # --- Drawing code should go here
    write_text(screen, font, "Tic-Tac-Toe!!!", 150, 20, colors.Orange)
    bg.draw(screen)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 30 frames per second
    clock.tick(30) # write now the clock is running at 30 frames per second
    # if I changed it to 40 the game would run faster
    # if I change it to 20 the game would run slower
    
def computer_turn():
    """
    Define one computer turn.
    
    Iterate over all the possible moves. Choose the best one. 
    If multiple moves are randomly best, randomly choose one of those moves.
    
    Write the computer's symbol to its chosen index.
    """
    # --- Main event loop
    for event in pygame.event.get(): # go through every event in game (mouse etc)
        if event.type == pygame.QUIT: # if the user clicks the x on the window it will close
            global quit
            quit = True
            return
        
    # --- Game logic should go here
    best_slots = []
    
    if random.randrange(3) + 1 > level.value:
        # The Inferior Algorithm
        # In general, this algorithm gathers a list of slots to randomly choose from
        # If the computer can win, only winning slots are available 
        # If the user can win next turn, only slots preventing the player's win are available
        # Otherwise, all empty slots are available
        
        winnable = False  # Boolean variable used to indicated sureness of a win.
        # Iterate over every win combination
        for combo in wins:
            # The empty slot number
            empty_slot = None
            # The accepted symbol. (None if not winnable, otherwise computer's symbol)
            symbol = None if not winnable else Player.Computer.symbol
            valid = True # Boolean variable used to allow appending of empty slot to list of slots
                         # to choose from (best_slots)
            # Iterate over the combo's slots
            for slot in combo:
                value = board[slot] # Get the symbol of the slot
                if value is None: # If there's no symbol...
                    # If there is no empty slot, assign the slot number as the empty slot
                    # Otherwise, exit this for loop and declare this combo invalid.
                    if empty_slot is not None:
                        valid = False
                        break
                    empty_slot = slot
                else: # If there is a symbol
                    # If only one symbol is accepted, break and invalidate the 
                    # combo if the value isn't the symbol. 
                    if symbol is not None: 
                        if value is not symbol:
                            valid = False
                            break
                    # Otherwise, set the accepted symbol to the value
                    symbol = value
            if valid:
                # If the computer realizes it can surely win, clear the old
                # best_slots and set winnable to True
                if not winnable and symbol is Player.Computer.symbol:
                    best_slots.clear()
                    winnable = True
                # Add the empty slot to best_slots
                best_slots.append(empty_slot)
        
                
        if not best_slots:
            # If there are no available slots, all empty slots are available
            best_slots = [i for i in range(9) if board[i] is None]
                        
                        
    else:
        # The Superior Algorithm
        # Check the database and only slots allowing the best possible outcome
        # are available for the computer's choosing
        best_outcome = Outcome.Loss
        slots = board.available_slots()
    
        for slot in slots:
            board_copy = copy(board)
            board_copy[slot] = Player.Computer.symbol
            outcome = database[repr(board_copy)]
            # Note: Win < Draw < Loss. See tictactoe\core\enums.Outcomes
            if outcome.value < best_outcome.value:
                best_outcome = outcome
                best_slots = [slot]
            elif outcome.value == best_outcome.value:
                best_slots.append(slot)
    
    # Choose a random slot from the available slots
    slot = random.choice(best_slots)

    # Write to the slot
    board[slot] = Player.Computer.symbol   
    bg.update(board)
    # --- Screen-clearing code goes here
    screen.blit(paper, [0, 0])
    # --- Drawing code should go here
    bg.draw(screen)
    write_text(screen, font, "Tic-Tac-Toe!!!", 150, 20, colors.Orange)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 30 frames per second
    clock.tick(30) # write now the clock is running at 30 frames per second
    # if I changed it to 40 the game would run faster
    # if I change it to 20 the game would run slower    
    
    
def display_result(winner: Optional[Player], combo: Optional[Combination]) -> None:
    """
    Display the result of the game to the user.
    """
    # Play the postgame music
    postgame_music.play()
    global quit
    while not quit:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                postgame_music.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Replay if the replay button is presesed;
                # Quit if the quit button is pressed
                if replay_button.hovering():
                    postgame_music.stop()
                    return
                elif quit_button.hovering():
                    quit = True
                    postgame_music.stop()
        # --- Screen-clearing code goes here
        screen.blit(paper, [0, 0])
        # --- Drawing code should go here
        bg.draw(screen)
        if winner is Player.Computer:
            color = colors.Red
            text = "Loss :("
            bg.display_win(screen, color, combo)
        elif winner is Player.User:
            color = colors.Green
            text = "Win!!!"
            bg.display_win(screen, color, combo)
        else:
            color = colors.Olive
            text = "Draw"
        write_text(screen, font, text, 200, 50, color)
        replay_button.draw()
        quit_button.draw()
        # --- Go ahead and update the screen with what we've drawn
        pygame.display.flip()
        # --- Limit to 30 frames per second
        clock.tick(30) # write now the clock is running at 30 frames per second
        # if I changed it to 40 the game would run faster
        # if I change it to 20 the game would run slower    

def play():
    """
    Play one round of Tic-Tac-Toe.
    """
    global quit
    # Run the main menu (level selecting) interface
    main_menu()
    # Return if quit request. This is prevalent throughout this file.
    if quit:
        return
    # Run the game-initalization interface
    init()
    if not quit:
        # Play the game music
        game_music.play()
        # If the computer's symbol is X, it goes first
        if Player.User.symbol == Symbol.O:
            computer_turn()
        while board.rank() is Outcome.Undetermined and not quit:
            # The user and computer alternate turns until the game is over
            if quit:
                break            
            user_turn()
            if quit or board.rank() is not Outcome.Undetermined:
                break
            computer_turn()
            if quit:
                break
        # Stop the game music
        game_music.stop()
        # Select the appropriate postgame music based off the outcome
        winner, combo = board.winner()
        global postgame_music
        if winner is Player.User:
            postgame_music = win_music
        elif winner is Player.Computer:
            postgame_music = lose_music
        else:
            postgame_music = draw_music
        # Display the result
        display_result(winner, combo)
        
def run():
    """
    Run the visual Tic-Tac-Toe interface.
    """
    while not quit:
        # Play one hand
        play()
        # Reset the board and box group
        global board
        board = Board()
        bg.update(board)
    # Stop all music (music doesn't terminate with pygame)
    for music in pregame_music, game_music, win_music, draw_music, lose_music:
        music.stop()
    
def main():
    load_resources()
    run()
    pygame.quit()
    
if __name__ == "__main__":
    main()
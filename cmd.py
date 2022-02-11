"Test the more sophisticated algorithm using the command prompt."
# Author: Michael Roberts
# Date: 8 June 2021
# File: tictactoe\cmd.py

from copy import copy
from pickle import load
from typing import Optional

import random

from tictactoe.core.board import Board, Combination
from tictactoe.core.enums import *
from tictactoe.core.cpu_database_builder import build


class Game(object):
    """
    Class for one command-line game of tic-tac-toe.
    """
    __slots__ = "board", "database"
    
    def __new__(cls):
        self = object.__new__(cls)
        self.board: Board = Board()
        self.database: dict = {}
        return self
    
    def prepare(self, user_symbol: Symbol):
        """
        Assign the provided symbol to the user, the other to the computer.
        Load the appropriate database for the computer's use.
        """
        import os
        os.chdir(os.getcwd() + "\\gui")
        self.build_cpu_database()
        
        Player.User.assign(user_symbol)
        if Player.Computer.symbol == Symbol.X:
            file = open("cpudata1.txt", "rb")
        else:
            file = open("cpudata2.txt", "rb")
        self.database = load(file)
        
    def build_cpu_database(self) -> None:
        """
        Build the CPU database, if unbuilt.
        """
        build(False)    
        
    def display_result(self, winner: Optional[Player], combo: Optional[Combination]) -> None:
        """
        Display the result of the game to the user.
        """
        if winner is Player.User:
            # This should NEVER happen 
            print("You won!")
        elif winner is Player.Computer:
            print("You lost.")
        else:
            print("The game is a draw.")
    
    def get_user_input(self) -> int: 
        """Return the index requested by the user.
        
        The index represents the position on the board
        the user desires to go and it should be an integer,
        between 0 and 8, inclusive.
        """
        invalid = True
        data = None
        while invalid:
            data = input("Enter a slot between 0 and 8: ")
            try:
                data = int(data)
                if 0 <= data <= 8:
                    invalid = False
                else:
                    print("The slot must be between 0 and 8, inclusive")
            except ValueError:
                print("The slot must be an integer")
        return data
    
    def init(self) -> None:
        """
        Initalize self. 
        This function should end by calling the prepare() function.
        """    
        print("Welcome to Tic Tac Toe!")
        print("X goes first.")
        data = None
        while data is None:
            data = input("Do you want to go (F)irst or (S)econd?: ")[0:].lower()
            if data == "f":
                self.prepare(Symbol.X)
            elif data == "s":
                self.prepare(Symbol.O)
            else: 
                data = None
        print(Board(range(9)))
    
    def output(self) -> None:
        """
        Output the board to the user.
        """
        print(self.board)
        
    def write_user_input(self, index: int) -> bool:
        """Write the user's symbol to the provided index on the game's
        tic-tac-toe board. The index should be a number between
        0 and 8, inclusive.
        
        This function will return True if the write was sucessful,
        False otherwise.
        """
        if isinstance(index, int) and 0 <= index < 9:
            symbol = self.board[index]
            if symbol is None:
                self.board[index] = Player.User.symbol
                return True
        return False
    
    def user_turn(self) -> None:
        """
        Define one user turn. 
        
        Request an index from the user and attempt to write the user's symbol
        to the index on the tic-tac-toe board. Keep requesting an index from the 
        user until a write is sucessful. 
        """
        successful = False
        while not successful:
            index = self.get_user_input()
            successful = self.write_user_input(index)
            
    
    def computer_turn(self):
        """
        Define one computer turn.
        
        Iterate over all the possible moves. Choose the best one. 
        If multiple moves are randomly best, randomly choose one of those moves.
        
        Write the computer's symbol to its chosen index.
        """
        # Get the slot
        best_outcome = Outcome.Loss
        best_slots = []
        slots = self.board.available_slots()
        
        for slot in slots:
            board_copy = copy(self.board)
            board_copy[slot] = Player.Computer.symbol
            outcome = self.database[repr(board_copy)]
            # Note: Win < Draw < Loss. See enums.Outcomes
            if outcome.value < best_outcome.value:
                best_outcome = outcome
                best_slots = [slot]
            elif outcome.value == best_outcome.value:
                best_slots.append(slot)
                
        slot = random.choice(best_slots)
        
        # Write to the slot
        self.board[slot] = Player.Computer.symbol
        
    def play(self) -> tuple[Optional[Player], Optional[Combination]]:
        """
        Play the game. 
        
        Alternate between the user's and computer's turn, outputting the board
        to the user before and after their turn. After the user's and computer's turn,
        check if there is a winner. If there is, return the winner and the winning combination. 
        In case of a draw, return (None, None).
        """
        if Player.User.symbol is Symbol.X:
            self.output()
            self.user_turn()
            self.output()
            
        ongoing = True
        
        while ongoing:
            self.computer_turn()
            self.output()
            
            winner, combo = self.board.winner()
            if winner is not None:
                return (winner, combo)
            
            if self.board.is_draw():
                return (None, None)
            

            self.user_turn()
            self.output()
            
            winner, combo = self.board.winner()
            if winner is not None:
                return (winner, combo)
            
            if self.board.is_draw():
                return (None, None)
        
    def run(self):
        """
        Run the game comprehensively. Initalize it, play it
        and display the results.
        """
        self.init()
        winner, combo = self.play()
        self.display_result(winner, combo)
        

game = Game()

if __name__ == "__main__":
    game.run()
        
        
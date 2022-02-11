"Define the Board class and the winning combinations."
# File: tictactoe\core\board.py

from collections.abc import Iterable
from copyreg import __newobj__
from typing import Optional

from tictactoe.core.enums import *

# Helpers

horizontal_wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
vertical_wins = ((0, 3, 6), (1, 4, 7), (2, 5, 8))
diagonal_wins = ((0, 4, 8), (2, 4, 6))
wins = (*horizontal_wins, *vertical_wins, *diagonal_wins)

# Annotation for a combination
Combination = tuple[int, int, int]

## Helper functions
def _elem_str(obj: Optional[Symbol]) -> str:
    # Return the string representation for a board element
    if isinstance(obj, int):
        return str(obj)
    return str(obj) if isinstance(obj, Symbol) else "-"

def _board_symbol(char: str) -> Optional[Symbol]:
    # Return the symbol represented by a character
    if char == "X":
        return Symbol.X
    elif char == "O":
        return Symbol.O
    elif char == "-":
        return None
    raise ValueError("Character must be in 'XO-'")

class Board(list):
    """
    The tic-tac-toe board. 
    """
    
    __slots__ = ()
    
    def __new__(cls, iterable: Iterable[Symbol] = ()):
        # Get a new object from list.__new__(cls, ())
        self = list.__new__(cls, ())
        # Extends self with the iterable provided
        self.extend(iterable[:9])
        # Pad the unassigned slots with the None value
        if len(self) < 9:
            self.extend([None] * (9 - len(self)))
        # Return self. Whew!
        return self
    
    def __init__(self, iterable: Iterable[Symbol] = ()):
        pass
    
    def __reduce_ex__(self, protocol: int):
        return (__newobj__, (type(self), tuple(self)), None, None, None)
    
    @classmethod
    def from_string(cls, strobj: str):
        self = cls()
        index = 0
        for char in strobj:
            if char in "XO-":
                if index >= 9:
                    raise ValueError("String represents nonexistant board")
                self[index] = _board_symbol(char)
                index += 1
        return self
    
    def winner(self) -> tuple[Optional[Player], Optional[Combination]]:
        """
        Return the player who won and the win combination, if that information is available.
        Otherwise, return (None, None)
        """
        # Iterate over all the win combinations
        for combo in wins:
            # The desired symbol
            desired_symbol = None
            # Iterate over every index in the combo
            for index in combo:
                # Find the symbol contained in the index
                symbol = self[index]
                # If the symbol is None, the slot is empty.
                # Thus, there is no win from this combo.
                if symbol is None:
                    break
                # The symbol is not the desired symbol.
                # Thus, there is no win from this combo.
                if desired_symbol is not None:
                    if symbol is not desired_symbol:
                        break
                else:
                    # Set our desired symbol to the symbol
                    desired_symbol = symbol
            else:
                # We have found three identical symbols in a horizontal combo
                # Return the symbol's player and the combo
                return (symbol.player, tuple(combo))
            
        return (None, None)
    
    def is_draw(self) -> bool:
        "Return if there is a draw."
        # If there is an empty slot, return False. 
        # There is no draw.
        if None in self:
            return False
        # Return if self.winner() doesn't determine a winner
        winner, _ = self.winner()
        return not winner
    
    def rank(self) -> Outcome:
        """
        Return the outcome of the board, 
        from the computer's prespective.
        """
        winner, _ = self.winner()
        if winner is Player.Computer:
            return Outcome.Win
        elif winner is Player.User:
            return Outcome.Loss
        elif None in self:
            return Outcome.Undetermined
        return Outcome.Draw
    
    def __repr__(self):
        return "".join([_elem_str(obj) for obj in self])
    
    def __str__(self):
        s = ""
        for i in range(0, 9, 3):
            s = s + " ".join([_elem_str(obj) for obj in self[i:i+3]]) + "\n"
        return s
    
    def available_slots(self) -> list[int]:
        "Return the slots available"
        listobj = []
        for index in range(9):
            symbol = self[index]
            if symbol is None:
                listobj.append(index)
        return listobj
    
    def turn(self) -> Player:
        "Return the player whose turn it is"
        x, o = self.count(Symbol.X), self.count(Symbol.O)
        if x == o:
            return Symbol.X.player
        if (x - 1) == o:
            return Symbol.O.player
        raise ValueError("Invalid board!")    
        
        
                    
        
    
    
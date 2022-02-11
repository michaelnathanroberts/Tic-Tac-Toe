"Enumerations related to the Tic-Tac-Toe game."
# File: tictactoe\core\enums.py

from __future__ import annotations
from enum import Enum

class Symbol(Enum):
    """
    The symbols of Tic-Tac-Toe (X and O)
    """
    X, O = range(2)
    
    __slots__ = 'player', 
    
    def opposite(self) -> Symbol:
        "Return the other symbol."
        return Symbol.O if self is Symbol.X else Symbol.X
    
    def __str__(self):
        return self.name

class Player(Enum):
    """
    The players of the game.
    There are 2 players in Tic-Tac-Toe:
        1) the user (the human player of the game)
        2) the computer (the automated opponent)
    """
    __slots__ = 'symbol', 
    
    User, Computer = range(2)
    
    def assign(self, symbol: Symbol) -> None:
        """
        Assign a symbol to both players.
        Assign the provided symbol to the provided player while
        assigning the other symbol to the other player.
        """
        self.symbol = symbol
        symbol.player = self
        other = self.opposite()
        other.symbol = self.symbol.opposite()
        self.symbol.opposite().player = other
    
    def opposite(self):
        "Return the other player."
        return Player.User if self is Player.Computer else Player.Computer
    
class Outcome(Enum):
    """
    The possible outcomes of a Tic-Tac-Toe game.
    Used by the computer in its recursive algorithm.
    """
    Win, Draw, Loss, Undetermined = range(4)
    
class Level(Enum):
    """
    The levels (or difficulties) of the Tic-Tac-Toe game.
    """
    Easy, Medium, Hard, Impossible = range(4)
    
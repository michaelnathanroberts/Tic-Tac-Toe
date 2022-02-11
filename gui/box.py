"""
Define the Box and BoxGroup classes.
This is the GUI to the tic-tac-toe Board objects.
"""
# File: tictactoe\gui\box.py

import pygame
from typing import Optional
from math import radians

import tictactoe.gui.colors as colors
from tictactoe.gui.colors import ColorType
from tictactoe.core.enums import Symbol
from tictactoe.core.board import Board, Combination
import tictactoe.core.board as board

class Box(object):
    """
    Define a box for visual tic-tac-toe. 
    """
    __slots__ = '_x', '_y', '_index', 'symbol'
    
    length = 100 # Width and height of the square 
    partition = 10 # Length of the partition; outline between boxes
    symbol_size = 10 # Size of symbols being drawn
    buffer = 10 # Length of the buffer between the partition's end and the symbol's beginning
    
    @property
    def x(self):
        "The x of the top-left corner"
        return self._x
    
    @property
    def y(self):
        "The y of the top-left corner"
        return self._y
    
    @property
    def index(self):
        "The number of the slot, from 0 to 8"
        return self._index
    
    def __new__(cls, x: int, y: int, index: int, symbol: Optional[Symbol] = None):
        self = object.__new__(cls)
        self._x = x
        self._y = y
        self._index = index
        self.symbol = symbol
        return self
    
    def __init__(self, x: int, y: int, index: int, symbol: Optional[Symbol] = None):
        pass
    
    def centre(self) -> tuple[int, int]:
        """Return the centre of this box"""
        return ((self.x + self.length // 2), (self.y + self.length // 2))   
    
    def hovered(self) -> bool:
        """
        Returns True if the slot's territory is hovered over by the mouse,
        False otherwise.
        """
        x, y = pygame.mouse.get_pos()
        if x > self.x + self.partition and x < self.x + self.length - self.partition:
            if y > self.y + self.partition and y < self.y + self.length - self.partition:
                return True
        return False
    
    def draw(self, screen: pygame.Surface, color: ColorType = colors.Grey) -> None:
        """
        Draw the box, to the pygame window.
        """
        pygame.draw.rect(screen, color, [self.x, self.y, self.length, self.length], self.partition)
        
        if self.symbol is Symbol.X:
            pygame.draw.line(screen, color, 
                             [self.x + self.partition + self.buffer, 
                              self.y + self.partition + self.buffer],
                             [self.x + self.length - self.partition - self.buffer, 
                              self.y + self.length - self.partition - self.buffer], 
                             self.symbol_size)
            pygame.draw.line(screen, color, 
                             [self.x + self.length - self.partition - self.buffer, 
                              self.y + self.partition + self.buffer],
                             [self.x + self.partition + self.buffer, 
                              self.y + self.length - self.partition - self.buffer], 
                             self.symbol_size)
        if self.symbol is Symbol.O:
            half_length = (self.length - (self.partition / 2)) / 2
            pygame.draw.circle(screen, color, [self.x + half_length, self.y + half_length], half_length - self.buffer, 
                               self.symbol_size)
            
            
class BoxGroup(object):
    """
    A group of 9 Box instances arranged 3x3, fit for a tic-tac-toe
    game.
    
    This is the GUI for the Board class.
    """
    
    __slots__ = "x", "y", "boxes"
    
    def __init__(self, x: int, y: int, board: Optional[Board] = None):
        self.x = x
        self.y = y
        self.boxes = []
        
        if board is None:
            board = Board()
            
        for i in range(3):
            for j in range(3):
                self.boxes.append(Box(x + (Box.length * j), y + (Box.length * i), len(self.boxes), board[len(self.boxes)]))
                                  
    
    def draw(self, screen: pygame.Surface, color: ColorType = colors.Grey) -> None:
        """
        Output the boxes to the screen provided.
        """
        for box in self.boxes:
            box.draw(screen, color)
            
    def display_win(self, screen: pygame.Surface, color: Optional[ColorType], combo: Combination) -> None:
        """
        Display the winning combination.
        """
        start = self.boxes[combo[0]]
        end = self.boxes[combo[2]]
        pygame.draw.line(screen, color, start.centre(), end.centre(), 10)
            
    def update(self, board: Board):
        """
        Update the box group using a Board instance.
        """
        self.__init__(self.x, self.y, board)
        
    def hovered_slot(self) -> Optional[int]:
        """
        Return the slot hovered, or None if no slot.
        """
        for box in self.boxes:
            if box.hovered():
                return box.index
        return None
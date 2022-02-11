"""
Define button and button-related classes
"""
# File: tictactoe\gui\button.py

import tictactoe.gui.colors as colors
from tictactoe.gui.box import Box

from dataclasses import dataclass
from typing import Optional
import pygame

@dataclass
class ButtonText(object):
    """
    Text for a button.
    """
    __slots__ = 'font', 'text', 'x', 'y', 'color', 'background_color'
    
    font: pygame.font.Font # The button's font
    text: str # The string of characters to be displayed
    x: int # Relative to the button
    y: int # Relative to the button
    color: colors.ColorType # The text color
    background_color: Optional[colors.ColorType] # The background color, or None
    
@dataclass
class ButtonOutline(object):
    """
    Outline for a button.
    """
    __slots__ = 'length', 'color'
    
    length: int # The length of the outline (or -1 if no outline)
    color: colors.ColorType
    
# -1: Nothing will be drawn.
# Black: null color - rgb(0, 0, 0)
ButtonOutline.__init__.__defaults__ = (-1, colors.Black)
ButtonOutline.null_instance = ButtonOutline() 


    
    
@dataclass
class Button(object):
    """A clickable button"""
    __slots__ = 'screen', 'text', 'x', 'y', 'width', 'height', 'color', 'outline'
    
    screen: pygame.Surface
    text: ButtonText
    x: int
    y: int
    width: int
    height: int
    color: colors.ColorType
    outline: ButtonOutline
    
    
    def draw(self):
        """
        Draw the button to the screen.
        """
        text = self.text.font.render(self.text.text, False, self.text.color, self.text.background_color)
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.width, self.height])
        pygame.draw.rect(self.screen, self.outline.color, [self.x, self.y, self.width, self.height], self.outline.length)
        self.screen.blit(text, [self.x + self.text.x, self.y + self.text.y])
        
    def hovering(self) -> bool:
        """Return if the mouse is hovering over the button."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.x <= mouse_x <= (self.x + self.width) and self.y <= mouse_y <= (self.y + self.height)
        
        
        
Button.__init__.__defaults__ = (ButtonOutline.null_instance,)
"""
A portable sound utility. 

Pygame sound, Windows sound and Darwin (Mac) sound supported.
An unfunctional sound instance is provided when the options above fail.

Credit to PyPI's playsound package.
"""
# File: tictactoe\gui\pysound.py

from abc import ABC, abstractmethod


class AbstractSound(ABC):
    "ABC for sound classes, including pygame.mixer.Sound"
    __slots__ = ()
    @abstractmethod
    def __init__(self, file):
        "Initialize self.  See help(type(self)) for accurate signature."
    @abstractmethod
    def play(self): 
        "Play the sound, from the beginning."
    @abstractmethod
    def stop(self):
        "Stop the sound being played."

try:
    import pygame
    PygameSound = pygame.mixer.Sound
    AbstractSound.register(PygameSound)
except ImportError:
    PygameSound = AbstractSound
    
WindowsSound = DarwinSound = AbstractSound


# Get the OS
import platform
system = platform.system()

if system == "Windows":
    from ctypes import c_buffer, windll
    from random import random
    from time   import sleep
    from sys    import getfilesystemencoding

    class WindowsSound(AbstractSound):
        """
        Pygame sound for Windows OS
        """
        __slots__ = "alias", "duration", "file"
        
        @staticmethod
        def winCommand(*command):
            buf = c_buffer(255)
            command = ' '.join(command).encode(getfilesystemencoding())
            errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
            if errorCode:
                errorBuffer = c_buffer(255)
                windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
                exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                    '\n        ' + command.decode() +
                                    '\n    ' + errorBuffer.value.decode())
                raise OSError(exceptionMessage)
            return buf.value     
        
        def __init__(self, file):
            self.file = file
            self.alias = 'playsound_' + str(random())
            WindowsSound.winCommand('open "' + self.file + '" alias', self.alias)
            WindowsSound.winCommand('set', self.alias, 'time format milliseconds')
            self.duration = WindowsSound.winCommand('status', self.alias, 'length')
            
        def play(self):
            WindowsSound.winCommand('play', self.alias, 'from 0 to', self.duration.decode())
            
        def stop(self):
            WindowsSound.winCommand('stop', self.alias)
    
elif platform.system() == "Darwin":
    from AppKit     import NSSound
    from Foundation import NSURL
    from time       import sleep
    
    class DarwinSound(AbstractSound):
        """
        Pygame sound for Darwin OS (Apple Mac)
        """
        __slots__ = "file", "sound"
        def __init__(self, file):
            if '://' not in file:
                if not file.startswith('/'):
                    from os import getcwd
                    file = getcwd() + '/' + sound
                file = 'file://' + sound
            url   = NSURL.URLWithString_(file)
            nssound = NSSound.alloc().initWithContentsOfURL_byReference_(url, True)
            if not nssound:
                raise IOError('Unable to load sound named: ' + file)
            
            self.file = file
            self.sound = nssound
            
        def play(self):
            self.sound.play()
            
        def stop(self):
            self.sound.stop()

class PseudoSound(AbstractSound):
    """
    Concrete class for unfunctional sound
    """
    __slots__ = ()
    def __init__(self, file): pass
    def play(self): pass
    def stop(self): pass    

def Sound(file):
    "Create and return a new sound object"
    try:
        # Try pygame's utility first
        return PygameSound(file)
    except Exception:
        try:
            # Try Windows sound
            return WindowsSound(file)
        except Exception:
            try:
                # Try Darwin sound
                return DarwinSound(file)
            except Exception:
                # Return an non-functional sound object
                return PseudoSound(file)
        

__all__ = ["AbstractSound", "WindowsSound", "DarwinSound", "PseudoSound", "PygameSound", "Sound"]
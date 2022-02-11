"Generate the CPU database for the more sophisticated algorithm."
# File: tictactoe\core\cpu_database_builder.py

from tictactoe.core.board import Board
from tictactoe.core.enums import *

from copy import copy
from pickle import dump

registry = {}

def _register(board: Board, outcome: Outcome) -> None:
    # Set repr(board) to outcome in registry
    registry[repr(board)] = outcome


def recursive_rank(board: Board) -> Outcome:
    # Get the "obvious" rank
    rank = board.rank()
    # If this board has been rated previously, don't do it again.
    # Rather use the registry.
    if repr(board) in registry:
        return registry[repr(board)]
    # If the obvious rank is determined, return it.
    # This is the base case.
    if rank is not Outcome.Undetermined:
        _register(board, rank)
        return rank
    # Get the player whose turn it is
    player = board.turn()
    # Get the avaliable slots
    slots = board.available_slots()
    # List of outcomes
    outcomes = []
    # Iterate over the avaliable slots
    for slot in slots:
        # Copy the board
        board_copy = copy(board)
        # Add the symbol of the player to the current slot
        board_copy[slot] = player.symbol
        # Determine its outcome by recursively calling this function 
        #assert board_copy.count(None) < board.count(None)
        outcomes.append(recursive_rank(board_copy))
    # Assume both players play perfectly
    # Therefore, they will choose the best option for themselves
    # Reminder: the outcomes are from the computer's prespective
    if player == Player.Computer:
        if Outcome.Win in outcomes:
            outcome = Outcome.Win
        elif Outcome.Draw in outcomes:
            outcome = Outcome.Draw
        else:
            outcome = Outcome.Loss
        return outcome
    else:
        # Only boards which the computer can act upon are registered
        # After the player's move it is the computer turn
        if Outcome.Loss in outcomes:
            outcome = Outcome.Loss
        elif Outcome.Draw in outcomes:
            outcome = Outcome.Draw
        else:
            outcome = Outcome.Win
        _register(board, outcome)
        return outcome
    
def build_first():
    Player.Computer.assign(Symbol.X)
    board = Board()
    recursive_rank(board)
    dump(registry, firstfile, 4)
    
def build_second():
    registry.clear()
    
    board = Board()
    Player.Computer.assign(Symbol.O)
    recursive_rank(board)
    dump(registry, secondfile, 4)
    
def build(rebuild=False):
    if not rebuild:
        # Don't reload if loaded alredy
        try: 
            open("cpudata1.txt", "rb")
            open("cpudata2.txt", "rb")
            return
        except IOError:
            pass
    global firstfile, secondfile
    firstfile = open("cpudata1.txt", "wb")
    secondfile = open("cpudata2.txt", "wb")    
    build_first()
    build_second()
    
if __name__ == "__main__":
    build(True)
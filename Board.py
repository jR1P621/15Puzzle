# KivaGale Hall & Jon Rippe 
# Created for CSCE A405 - Artificial Intelligence Fall 2021

# Board Class -
# Represents a board of 15-Puzzle (4x4 by default)
# "Solved" order is 1 to 15 with a following space:
#  1  2  3  4
#  5  6  7  8
#  9 10 11 12
# 13 14 15  _
# "Solved" order is consistent with the above pattern regardless of board size.
# Board will initialize by default in the "solved" state.

import math
import random


class Board:
    def __init__(self, cols=4, rows=4, nums=None, verbose=False) -> None:
        self.rows = rows
        self.cols = cols
        self.size = rows*cols
        if nums is None:
            nums = [*range(1, self.size)]+[0]
        self.resetBoard(nums, verbose=verbose)

    # Sets board order according to nums list param
    # (Ex. "solved" order = [1, 2, 3, 4, 5, 6, ... , 14, 15, 0])
    def resetBoard(self, nums, verbose=False):
        if set(nums) != set([*range(0, self.size)]):
            print('Wrong numbers!')
            nums = [*range(1, self.size)]+[0]
        self.spaces = {}
        for i in range(1, self.size+1):
            self.spaces[i] = nums[i-1]
            if nums[i-1] == 0:
                self.empty = i
        if verbose:
            self.print()

    # returns a dict of available moves with key = space and
    # value = number in that space
    def getMoves(self):
        moves = {}
        if self.empty > self.cols:
            i = self.empty - self.cols
            moves[i] = self.spaces[i]
        if self.empty <= self.size - self.cols:
            i = self.empty + self.cols
            moves[i] = self.spaces[i]
        if (self.empty - 1) % self.cols > 0:
            i = self.empty - 1
            moves[i] = self.spaces[i]
        if self.empty % self.cols > 0:
            i = self.empty + 1
            moves[i] = self.spaces[i]
        return moves

    # Makes a valid move and updates board
    # Returns new board if inplace=False
    def makeMove(self, num, inplace=False, verbose=False):
        if inplace:
            thisBoard = self
        else:
            thisBoard = self.clone(verbose=False)

        moves = thisBoard.getMoves()
        if num in moves.values():
            numSpace = self._getSpace(num)
            thisBoard.spaces[thisBoard.empty], thisBoard.spaces[numSpace] = \
                thisBoard.spaces[numSpace], thisBoard.spaces[thisBoard.empty]
            thisBoard.empty = numSpace
        else:
            print('Invalid Move.')
        if verbose:
            thisBoard.print()
        if not inplace:
            return thisBoard

    # Makes n random moves (avoids moving the same tile consecutively)
    # Returns a list of tiles moved
    def shuffle(self, n=None, verbose=False):
        if n is None:
            n = self.size * 10
        prevSpace = None
        history = []
        for i in range(0, n):
            moves = self.getMoves()
            if prevSpace is not None:
                moves.pop(prevSpace)
            prevSpace = self.empty
            keys = list(moves)
            move = random.randint(0, len(keys) - 1)
            self.makeMove(moves[keys[move]], inplace=True, verbose=verbose)
            history.append(moves[keys[move]])
        return history

    # Prints the current board
    def print(self):
        maxDigits = math.trunc(math.log10(self.size-1))+1
        for i in range(1, self.size+1):
            if i == self.empty:
                print('_', end='')
                currDigits = 1
            else:
                print(self.spaces[i], end='')
                currDigits = math.trunc(math.log10(self.spaces[i]))+1
            for d in range(currDigits, maxDigits+1):
                print(' ', end='')
            if i % self.cols == 0:
                print()
        # print(self.getMoves())

    # Returns a clone of the current Board object
    def clone(self, verbose=False):
        return Board(self.cols, self.rows, list(
            self.spaces.values()), verbose=verbose)

    # Returns a list of ints corresponding to the current tile order
    def getState(self):
        return list(self.spaces.values())

    # Return the board's parity (0=even 1=odd) based on "solved" board
    def getParity(self):
        wrong = 0
        validSpaces = [*range(1, self.size+1)]
        for i in validSpaces:
            for j in validSpaces[i:]:
                if self.spaces[j] > 0 and self.spaces[i] > self.spaces[j]:
                    wrong += 1
        # Adjust based on empty space distance from bottom row
        if self.cols % 2 == 0:
            wrong += ((self.empty - 1) // self.cols) + self.rows + 1

        return wrong % 2

    # Returns the number of total misplaced tiles based on goal
    # Uses "solved" board as default
    def getMisplacedCount(self, goal=None):
        if goal is None:
            goal = Board(cols=self.cols, rows=self.rows, verbose=False)
        if self.rows != goal.rows or self.cols != goal.cols:
            print('Incompatible Boards')
            return -1
        misplaced = 0
        for n, m in zip(self.spaces.values(), goal.spaces.values()):
            if n > 0 and n != m:
                misplaced += 1
        return misplaced

    # Returns the number of tiles a given num is from its desired space
    def getDistance(self, num, space=None):
        currentSpace = self._getSpace(num)
        currentRow = (currentSpace - 1) // self.cols
        currentCol = (currentSpace - 1) % self.cols
        if space is None:
            space = num
        desiredRow = (space - 1) // self.cols
        desiredCol = (space - 1) % self.cols
        return abs(currentRow - desiredRow) + abs(currentCol - desiredCol)

    # Returns the total "distance" between two boards
    # Uses "solved" board as default
    def getBoardDistance(self, otherBoard=None):
        if otherBoard is None:
            otherBoard = Board(cols=self.cols, rows=self.rows, verbose=False)
        if self.rows != otherBoard.rows or self.cols != otherBoard.cols:
            print('Incompatible Boards')
            return -1
        distance = 0
        for n in self.spaces.values():
            if n > 0:
                distance += self.getDistance(n,
                                             space=otherBoard._getSpace(n))
        return distance

    # Returns the tile index containing num
    def _getSpace(self, num):
        for key, value in self.spaces.items():
            if value == num:
                return key

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Board) or \
                self.cols != o.cols or self.rows != o.rows:
            return False
        return self.spaces.items() == o.spaces.items()

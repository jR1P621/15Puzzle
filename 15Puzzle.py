# KivaGale Hall & Jon Rippe
# Created for CSCE A405 - Artificial Intelligence Fall 2021

# Textual UI to demonstrate Tree Search algorithms on a 15-Puzzle board


# Imports
from Board import Board
from Node import Node
from SearchFunctions import treeSearch
from hashlib import md5


# Global variables
boardRows = 4
boardCols = 4
start = Board(cols=boardCols, rows=boardRows, verbose=False)
goal = Board(cols=boardCols, rows=boardRows, verbose=False)
userInput = ''
menuFunctions = {}
nodeExpandFunctions = {}
searchFunctions = {}
maxNodes = 1000000
trimmer = True
global costFunction


# Print Functions ----------------------------------------------


# Prints current start and goal status
def printStatus():
    print('Current Board State:')
    start.print()
    print()
    print('Goal Board State:')
    goal.print()
    print()
    print('Misplaced Tiles:', str(start.getMisplacedCount(goal)))
    print('Distance to Goal:', str(start.getBoardDistance(goal)))
    print('Board/Goal Parity:', str(start.getParity()),
          '/', str(goal.getParity()))


# Prints the main menu
def printMainMenu():
    print('---Main Menu---\n',
          '1) Reset Board\n',
          '2) Reset Goal\n',
          '3) Set Board\n',
          '4) Set Goal\n',
          '5) Shift Tile on Board\n',
          '6) Shift Tile on Goal\n',
          '7) Shuffle Board\n',
          '8) Perform Search\n',
          '9) Change Board Size\n',
          '0) Exit',
          sep='')


# Prints the search menu
def printSearchMenu():
    global maxNodes
    global userInput
    global trimmer
    if start.getParity() != goal.getParity():
        print('Unequal parity.  No solution possible.')
        input("Press Enter to return to Main Menu...")
        userInput = '0'
    while(userInput != '0'):
        print('Select Search Method:\n',
              '1) Breadth-First\n',
              '2) Greedy Best-First\n',
              '3) A*\n',
              #   '8) Toggle Redundant Node Trimmer (',
              #   'ON' if trimmer else 'OFF', ')\n',
              '9) Set Max Node Count (', 'disabled' if maxNodes < 0 else str(
                  maxNodes), ')\n',
              '0) Return to Main Menu',
              sep='')
        userInput = input('Enter Menu Option: ')
        if userInput == '9':
            try:
                maxNodes = int(input('Enter new max: '))
            except ValueError:
                print('Invalid Input')
        # elif userInput == '8':
        #     trimmer = ~trimmer
        elif userInput != '0':
            performSearch(userInput)
    userInput = ''


# Prompt Functions -------------------------------------------


# Resets start board (0) or goal board (1) to "solved" state
def resetBoard(param):
    print('Resetting...')
    if param == 0:
        global start
        start = Board(cols=boardCols, rows=boardRows, verbose=False)
    else:
        global goal
        goal = Board(cols=boardCols, rows=boardRows, verbose=False)


# Sets start board (0) or goal board (1) based on user specified input
def setBoard(param):
    inputString = input(
        'Enter numbers in desired order ' +
        '(left to right / top to bottom)\n' +
        'separated by spaces.  Use \'0\' for the empty space.\n' +
        '(Ex. default 4x4 = \"1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0\"):\n')
    strList = inputString.split(' ')
    try:
        numList = [int(s) for s in strList]
    except ValueError:
        print('Invalid List')
    else:
        print('Setting...')
        if param == 0:
            global start
            start = Board(cols=boardCols, rows=boardRows,
                          nums=numList, verbose=False)
        else:
            global goal
            goal = Board(cols=boardCols, rows=boardRows,
                         nums=numList, verbose=False)


# Performs a use specified move on the specified board
def makeMove(board):
    try:
        board.makeMove(int(input('Number to Move: ')),
                       inplace=True, verbose=False)
    except ValueError:
        print('Invalid Input')


# Changes board size based on user input
def changeSize():
    try:
        newCols = int(input('Enter new column count (2+): '))
        newRows = int(input('Enter new row count (2+): '))
    except ValueError:
        print('Invalid Input')
        return
    if newCols < 2 or newRows < 2:
        print('Must be at least 2x2')
    else:
        global boardCols
        global boardRows
        global start
        global goal
        boardCols = newCols
        boardRows = newRows
        start = Board(cols=boardCols, rows=boardRows, verbose=False)
        goal = Board(cols=boardCols, rows=boardRows, verbose=False)


# Makes a user specified number of random moves
def shuffleBoard():
    try:
        count = abs(int(input('How many random moves?: ')))
    except ValueError:
        print('Invalid Input')
    else:
        start.shuffle(count, verbose=False)


# Search Functions --------------------------------------------------


# Sets cost functions and performs a tree search:
def performSearch(s):
    global costFunction
    try:
        costFunction = int(s) - 1
        if costFunction > 2 or costFunction < 0:
            raise ValueError
        if start.getParity() != goal.getParity():
            print('Unequal parity.  No solution possible.')
            raise ValueError
    except ValueError:
        print('Invalid Search')
    else:
        solution = treeSearch(start=Node(start, None, None, 0, 0),
                              goal=goal,
                              expandFunction=nodeExpand,
                              hashFunction=nodeHash,
                              maxNodes=maxNodes,
                              trimmer=trimmer,
                              verbose=True)
        print('\n---Results---')
        [print(key, ':', value) for key, value in solution.items()]
    input('Press Enter to Continue...')


# Custom expand function to work with TreeSearch
# Sets child node cost according to costFunction:
# 1= Breadth-first (cost = depth)
# 2= Greedy Best (cost = distance)
# 3= A* (cost = depth + distance)
def nodeExpand(node: Node):
    global costFunction
    thisBoard: Board = node.state
    moves = thisBoard.getMoves()
    newNodes = []
    for key, value in moves.items():
        newBoard = thisBoard.makeMove(value, verbose=False)
        costFunctions = [node.depth + 1,
                         newBoard.getBoardDistance(goal),
                         newBoard.getBoardDistance(goal) + node.depth + 1]
        newNodes.append(Node(newBoard,
                             node,
                             value,
                             costFunctions[costFunction],
                             node.depth + 1))
    return newNodes


def nodeHash(node: Node):
    thisBoard: Board = node.state
    return md5(bytes(str(thisBoard.getState()), 'utf-8')).hexdigest()


# Main Menu ---------------------------------------------------


menuFunctions['1'] = lambda: resetBoard(0)
menuFunctions['2'] = lambda: resetBoard(1)
menuFunctions['3'] = lambda: setBoard(0)
menuFunctions['4'] = lambda: setBoard(1)
menuFunctions['5'] = lambda: makeMove(start)
menuFunctions['6'] = lambda: makeMove(goal)
menuFunctions['7'] = lambda: shuffleBoard()
menuFunctions['8'] = lambda: printSearchMenu()
menuFunctions['9'] = lambda: changeSize()
menuFunctions['0'] = lambda: print('Goodbye')
promptOptions = ['1', '2', '3', '4', '5', '6', '7', '9']

while(userInput != '0'):
    print()
    print('---------------------')
    printStatus()
    print()
    printMainMenu()
    userInput = input('Enter Menu Option: ')
    print()

    if userInput not in menuFunctions.keys():
        print('Invalid Input')
    else:
        menuFunctions[userInput]()
    if userInput in promptOptions:
        input('Press Enter to Continue...')

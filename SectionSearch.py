from Node import Node
from Board import Board
from queue import PriorityQueue
from typing import List
from hashlib import md5
from SearchFunctions import _getSolutionPath


def sectionSearch(start: Board, goal: Board, maxNodes: int,
                  verbose=False):

    wCol = 1
    wRow = 1
    wWidth = 2
    wHeight = 2
    currentNode = Node(start, None, None, 0, 0)
    spaces2d = [[*range(i, i+start.cols)]
                for i in range(1, start.size, start.cols)]
    spacesLocked = set()
    maxNodes = abs(maxNodes)
    root = currentNode
    root.parent = None
    solution = {}
    solution['expandedNodes'] = 0
    solution['totalNodes'] = 1
    solution['depth'] = 0
    solution['path'] = 'No solution found within node limit (' + str(
        maxNodes) + ')'
    trimmerHistory = set()

    nodeQueue = PriorityQueue()
    nodeQueue.put(root)
    if verbose:
        verboseCount = 1

    def getWorkingSpaces():
        workingRows = spaces2d[wRow-1:wRow+wHeight-1]
        s = [c for r in workingRows for c in r[wCol-1:wCol+wWidth-1]]
        if 16 in s:
            s.remove(16)
        return set(s)

    def nodeExpand(node: Node):
        thisBoard: Board = node.state
        moves = thisBoard.getMoves()
        newNodes = []
        for key, value in moves.items():
            if key not in spacesLocked:
                newBoard = thisBoard.makeMove(value, verbose=False)
                distance = node.depth + 1
                for i in wSpaces:
                    distance += newBoard.getDistance(i, i)
                    # if newBoard._getSpace(i) not in wSpaces:
                    #     distance += newBoard.getDistance(i, newBoard.empty)
                newNodes.append(Node(newBoard,
                                     node,
                                     value,
                                     distance,
                                     node.depth + 1))
        return newNodes

    while wRow + wHeight <= start.rows + 1:
        while wCol + wWidth <= start.cols + 1:
            wSpaces = getWorkingSpaces()
            for s in wSpaces:
                if s in spacesLocked:
                    spacesLocked.remove(s)
            print(spacesLocked)
            print(wSpaces)

            # Begin Processing

            # Search
            while(maxNodes >= solution['totalNodes']):
                currentNode: Node = nodeQueue.get()

                # Found solution
                currentBoard: Board = currentNode.state
                if all(key == currentBoard.spaces[key] for key in wSpaces):
                    # solution['path'].append(_getSolutionPath(currentNode))
                    break

                # Expand next node and add children to queue
                newNodes: List[Node] = nodeExpand(currentNode)

                if newNodes:
                    solution['expandedNodes'] += 1
                for node in newNodes:
                    trimmerHash = md5(
                        bytes(str(node.state.getState()), 'utf-8')).hexdigest()
                    if trimmerHash not in trimmerHistory:
                        trimmerHistory.add(trimmerHash)
                        solution['totalNodes'] += 1
                        nodeQueue.put(node)

                # Update counts
                if solution['depth'] < currentNode.depth + 1:
                    solution['depth'] = currentNode.depth + 1
                if verbose and solution['totalNodes'] >= 10000 * verboseCount:
                    print('Node Count: ' + str(solution['totalNodes']))
                    verboseCount += 1

                # print('Node Count: ' + str(solution['totalNodes']))

            if verbose:
                currentNode.state.print()
            nodeQueue = PriorityQueue()
            nodeQueue.put(currentNode)
            trimmerHistory.clear()
            spacesLocked.update(wSpaces)
            wCol += 2
            if wCol == start.cols:
                wCol -= 1
        wCol = 1
        wRow += 2
        if wRow == start.rows:
            wRow -= 1

    # Found solution
        if currentNode.state == goal:
            solution['path'] = _getSolutionPath(currentNode)
            break

    return solution

# KivaGale Hall & Jon Rippe
# Created for CSCE A405 - Artificial Intelligence Fall 2021
# Primary Tree Search function

from Node import Node
from queue import PriorityQueue
from typing import List

# Helper Functions


# Follows a given node up to the root node
# Returns a list of actions to get from root to goal
def _getSolutionPath(goalNode):
    solution = []
    currentNode: Node = goalNode
    while (currentNode.parent is not None):
        solution.append(currentNode.action)
        currentNode = currentNode.parent
    solution.reverse()
    return solution


# Recursively checks if a branch is dead
# Returns a list of nodes in the dead branch
def _trimDeadEnd(node: Node):
    if node.children:
        return []
    else:
        node.parent.children.remove(node)
        return [node] + _trimDeadEnd(node.parent)


# Main Search Function


# Performs a Tree Search using a Priority Queue
# Queue evaluates nodes based on cost (lowest to highest)
# start is a Node
# goal is a state (must be same type as start.state)
# expandFunction is a function that takes a Node and
#   returns a list of child Nodes.
# hashFunction is a function that takes a Node and returns a
#   hash representing its state as a string.
# Implemented Tree Search algorithm is dependent on the costs
#   assigned to nodes through the expandNode function.
# trimmer enables a node history that prevents identical nodes
# Returns Dictionary containing solution, node counts, and depth
def treeSearch(start: Node,
               goal,
               expandFunction,
               hashFunction,
               maxNodes: int = -1,
               trimmer=True,
               verbose=False):

    # Initialization
    verboseCount = 1
    root = start
    root.parent = None
    root.cost = 0
    solution = {}
    solution['expandedNodes'] = 0
    solution['totalNodes'] = 1
    solution['maxSearchSpaceNodes'] = 1
    solution['treeDepth'] = 0
    solution['pathLength'] = 0
    solution['path'] = 'No solution found'
    searchSpaceCount = 1
    trimmerHistory = {}
    searchSpaceNodes = [root]

    nodeQueue = PriorityQueue()
    nodeQueue.put(root)
    trimmerHistory[hashFunction(root)] = root.cost

    # Search
    while ((maxNodes < 0 or maxNodes >= solution['totalNodes'])
           and nodeQueue.qsize() > 0):

        currentNode: Node = nodeQueue.get()

        # Found solution
        if currentNode.state == goal:
            solution['path'] = _getSolutionPath(currentNode)
            solution['pathLength'] = currentNode.depth
            break

        # Expand next node and add children to queue
        newNodes: List[Node] = expandFunction(currentNode)
        if newNodes:
            solution['expandedNodes'] += 1
            for node in newNodes:
                nodeHash = hashFunction(node)
                if (not trimmer) or \
                        (nodeHash not in trimmerHistory.keys() or
                         trimmerHistory[nodeHash] > node.cost):
                    trimmerHistory[nodeHash] = node.cost
                    solution['totalNodes'] += 1
                    searchSpaceCount += 1
                    nodeQueue.put(node)
                    searchSpaceNodes.append(node)
                    currentNode.children.append(node)
        # Trim dead branches / remove from search space
        trimmedNodes = _trimDeadEnd(currentNode)
        searchSpaceCount -= len(trimmedNodes)
        for node in trimmedNodes:
            searchSpaceNodes.remove(node)
            del node

        # Update counts
        solution['treeDepth'] = max(solution['treeDepth'],
                                    currentNode.depth + 1)
        solution['maxSearchSpaceNodes'] = max(solution['maxSearchSpaceNodes'],
                                              searchSpaceCount)

        if verbose and solution['totalNodes'] >= 10000 * verboseCount:
            print(solution['treeDepth'], ' : ', searchSpaceCount, ' : ',
                  solution['totalNodes'])
            verboseCount += 1

    return solution

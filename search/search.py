# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    initial_state = (problem.getStartState(), '', 0)
    frontier.push(initial_state)
    explored = []
    actions = []

    parent_map = { initial_state[0] : None }

    while not frontier.isEmpty():
        node = frontier.pop()
        explored.append(node[0])

        if problem.isGoalState(node[0]):
            cusror = node[0]
            while cusror is not initial_state[0]:
                actions.append(parent_map.get(cusror)[1])
                cusror = parent_map.get(cusror)[0]

            actions.reverse()
            return actions

        for action in problem.getSuccessors(node[0]):
            child = action[0]  # Gets state

            if not child in frontier.list and not child in explored:
                frontier.push(action)
                parent_map[child] = (node[0], action[1])
                
    return actions
    
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    initial_state = (problem.getStartState(), '', 0)
    frontier.push(initial_state[0])
    explored = []
    actions = []

    parent_map = { initial_state[0] : None }

    while not frontier.isEmpty():
        node = frontier.pop()
        explored.append(node)

        if problem.isGoalState(node):      
            cusror = node
            while cusror is not initial_state[0]:
                actions.append(parent_map.get(cusror)[1])
                cusror = parent_map.get(cusror)[0]

            actions.reverse()
            return actions

        for action in problem.getSuccessors(node):
            child = action[0]  # Gets state

            if not child in frontier.list and not child in explored:
                frontier.push(child)
                parent_map[child] = (node, action[1])

    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    initial_state = (problem.getStartState(), '', 0)
    frontier.push(initial_state[0], 0)
    explored = []
    actions = []

    parent_map = { initial_state[0] : None }
    cost_map = { initial_state[0] : 0 }

    while not frontier.isEmpty():
        node = frontier.pop()
        explored.append(node)

        if problem.isGoalState(node):
            cursor = node
            while cursor is not initial_state[0]:
                    actions.append(parent_map.get(cursor)[1])
                    cursor = parent_map.get(cursor)[0]

            actions.reverse()
            return actions

        for action in problem.getSuccessors(node):
            child = action[0]

            if not child in explored and not child in frontier.heap:
                parent_map[child] = (node, action[1])

                actions_to_child = [action[1]]
                cursor = node
                while cursor is not initial_state[0]:
                    actions_to_child.append(parent_map.get(cursor)[1])
                    cursor = parent_map.get(cursor)[0]

                actions_to_child.reverse()
                cost = problem.getCostOfActions(actions_to_child)
                cost_map[child] = cost
                frontier.push(child, cost)
                explored.append(child)
                
            
            else:
                for item in frontier.heap:
                    if child == item[2]:
                        actions_to_child = [action[1]]
                        cursor = node

                        while cursor is not initial_state[0]:
                            actions_to_child.append(parent_map.get(cursor)[1])
                            cursor = parent_map.get(cursor)[0]

                        actions_to_child.reverse()
                        cost = problem.getCostOfActions(actions_to_child)

                        if cost < cost_map.get(child):
                            for item in frontier.heap:
                                if child == item[2]:
                                    frontier.heap.remove(item)
                            frontier.push(child, cost)
                            parent_map[child] = (node, action[1])
                            cost_map[child] = cost

    return actions



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    initial_state = (problem.getStartState(), '', 0)
    frontier.push(initial_state[0], 0)
    explored = []
    actions = []

    parent_map = { initial_state[0] : None }
    cost_map = { initial_state[0] : 0 }

    while not frontier.isEmpty():
        node = frontier.pop()
        explored.append(node)

        if problem.isGoalState(node):
            cursor = node
            while cursor is not initial_state[0]:
                    actions.append(parent_map.get(cursor)[1])
                    cursor = parent_map.get(cursor)[0]

            actions.reverse()
            return actions

        for action in problem.getSuccessors(node):
            child = action[0]

            if not child in explored and not child in frontier.heap:
                parent_map[child] = (node, action[1])

                actions_to_child = [action[1]]
                cursor = node
                while cursor is not initial_state[0]:
                    actions_to_child.append(parent_map.get(cursor)[1])
                    cursor = parent_map.get(cursor)[0]

                actions_to_child.reverse()
                cost = problem.getCostOfActions(actions_to_child) + heuristic(child, problem)
                cost_map[child] = cost
                frontier.push(child, cost)
                explored.append(child)
                
            
            else:
                for item in frontier.heap:
                    if child == item[2]:
                        actions_to_child = [action[1]]
                        cursor = node

                        while cursor is not initial_state[0]:
                            actions_to_child.append(parent_map.get(cursor)[1])
                            cursor = parent_map.get(cursor)[0]

                        actions_to_child.reverse()
                        cost = problem.getCostOfActions(actions_to_child) + heuristic(child, problem)

                        if cost < cost_map.get(child):
                            for item in frontier.heap:
                                if child == item[2]:
                                    frontier.heap.remove(item)
                            frontier.push(child, cost)
                            parent_map[child] = (node, action[1])
                            cost_map[child] = cost

    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

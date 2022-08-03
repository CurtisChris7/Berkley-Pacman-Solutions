# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostPositions = successorGameState.getGhostPositions()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        foodList = newFood.asList()
        if len(foodList) == 0:
            return float('inf')

        minFoodDistance = float('inf')
        for pos in foodList:
            posDistance = manhattanDistance(newPos, pos)

            for state in newGhostPositions:
                posDistance -= manhattanDistance(newPos, state)

            if posDistance < minFoodDistance:
                minFoodDistance = posDistance

        return (10 * successorGameState.getScore()) - minFoodDistance

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """

    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """ 
    def minimax(self, gameState, depth, agentIndex):
        if (agentIndex == gameState.getNumAgents()):
            depth += 1
            agentIndex = agentIndex % gameState.getNumAgents()

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        if agentIndex == 0:  # Max agent
            v = float('-inf')

        else:
            v = float('inf')

        for action in gameState.getLegalActions(agentIndex):
            state = gameState.generateSuccessor(agentIndex, action)
            
            if state.isWin() or state.isLose():
                if agentIndex == 0:
                    v = max(v, self.evaluationFunction(state))
                else:
                    v = min(v, self.evaluationFunction(state))
            else:
                if agentIndex == 0:
                    v = max(v, self.minimax(state, depth, agentIndex + 1))
                else:
                    v = min(v, self.minimax(state, depth, agentIndex + 1))
        return v

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        action_map = {}
        best_action_value = float('-inf')
        best_action = None

        for action in gameState.getLegalActions(0):
            action_map[action] = self.minimax(gameState.generateSuccessor(0, action), 0, 1)

        for action in action_map:
            if best_action_value < action_map[action]:
                best_action_value = action_map[action]
                best_action = action

        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def minValue (self, gameState, agentIndex, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth: #No Legal actions.
            return self.evaluationFunction(gameState)

        v = float('inf')
        for action in gameState.getLegalActions(agentIndex):
            if (agentIndex < gameState.getNumAgents() - 1):
                v = min(v, self.minValue(gameState.generateSuccessor(agentIndex,action), agentIndex + 1, depth, alpha, beta))
            else:  
                v = min(v, self.maxValue(gameState.generateSuccessor(agentIndex, action), depth + 1, alpha, beta))

            if (v < alpha):
                return v
            beta = min(beta, v)

        return v

    def maxValue (self, gameState, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        v = float('-inf')
        for action in gameState.getLegalActions(0):
            v = max(v, self.minValue(gameState.generateSuccessor(0, action), 1, depth, alpha, beta))

            if (v > beta):
                return v
            alpha = max(alpha, v)

        return v

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        alpha = float('-inf')
        beta = float('inf')
        action_value = float('-inf')
        max_action = None

        for action in gameState.getLegalActions(0):
            action_value = self.minValue(gameState.generateSuccessor(0, action), 1, 0, alpha, beta)
            if (alpha < action_value):
                alpha = action_value
                max_action = action

        return max_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expValue (self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth: #No Legal actions.
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentIndex)
        avg = 1 / len(actions)
        for action in actions:
            if (agentIndex < gameState.getNumAgents() - 1):
                avg += self.expValue(gameState.generateSuccessor(agentIndex,action), agentIndex + 1, depth)
            else:  
                avg += self.maxValue(gameState.generateSuccessor(agentIndex, action), depth + 1)

        return avg

    def maxValue (self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        v = float('-inf')
        for action in gameState.getLegalActions(0):
            v = max(v, self.expValue(gameState.generateSuccessor(0, action), 1, depth))

        return v

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        action_map = {}
        best_action_value = float('-inf')
        best_action = None

        for action in gameState.getLegalActions(0):
            action_map[action] = self.expValue(gameState.generateSuccessor(0, action), 1, 0)

        for action in action_map:
            if best_action_value < action_map[action]  and action != "Stop":
                best_action_value = action_map[action]
                best_action = action

        return best_action

def getMinFoodDistance(currentGameState):
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    foodList = newFood.asList()
    
    if len(foodList) == 0:
        return 0

    minFoodDistance = float('inf')
    for pos in foodList:
        posDistance = manhattanDistance(newPos, pos)

        if posDistance < minFoodDistance:
            minFoodDistance = posDistance

    return minFoodDistance

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Pursues the closest food pellet
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    capsules = currentGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]

    foodList = newFood.asList()
    if len(foodList) == 0:
        return float('inf')

    minCapsuleDistance= float('inf')
    for capsule in capsules:
        dist = manhattanDistance(newPos, capsule)
        if dist < minCapsuleDistance:
            minCapsuleDistance = dist

    newGhostPositions = currentGameState.getGhostPositions()

    minGhostDistance = float('inf')
    i = 0
    for ghostState in newGhostPositions:
        ghostDistance = manhattanDistance(newPos, ghostState)
        i += 1
        if ghostDistance < minGhostDistance:
            minGhostDistance = ghostDistance

    minFoodDistance = float('inf')
    for pos in foodList:
        posDistance = manhattanDistance(newPos, pos)

        if posDistance < minFoodDistance:
            minFoodDistance = posDistance

    minScaredTime = float('inf')
    for time in newScaredTimes:
        if time < minScaredTime:
            minScaredTime = time

    return (2 * currentGameState.getScore()) - (1.3 * minFoodDistance) - (1 * minCapsuleDistance) - (0.2 * minGhostDistance) + (0.2 * minScaredTime)
    

# Abbreviation
better = betterEvaluationFunction

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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        gPoses = [ghost.getPosition() for ghost in newGhostStates]
        gDis = [manhattanDistance(newPos, gPos) for gPos in gPoses]
        #print(gDis, newScaredTimes)
        fDis = [manhattanDistance(newPos, fPos) for fPos in newFood.asList()]
        cDis = [manhattanDistance(newPos, cPos) for cPos in successorGameState.getCapsules()]
        if min(gDis) > 5 or min(newScaredTimes) > 10:
            fScore, diffScore = 0, 0
            if fDis:
                fScore = 100 - min(fDis) + int(newFood[newPos[0]][newPos[1]]) * 10
            diffScore = (successorGameState.getScore() - currentGameState.getScore())*10
            return fScore + diffScore
        else:
            cScore = 0
            if cDis:
                #print(successorGameState.getCapsules(), newPos)
                cScore = int(newPos in successorGameState.getCapsules()) * 99999999999
            return min(gDis)*10 + cScore

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
    def minimax(self, state, depth):
        maximum = -float("inf")
        result = None
        for action in state.getLegalActions(0):
            temp = self.minValue(state.generateSuccessor(0, action), 1, 0, depth)
            if temp > maximum:
                maximum = temp
                result = action
        return result

    def minValue(self, state, index, curDepth, depth):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        v = float("inf")
        for a in state.getLegalActions(index):
            if index < state.getNumAgents()-1:
                v = min(v, self.minValue(state.generateSuccessor(index, a), index+1, curDepth, depth))
            else:
                v = min(v, self.maxValue(state.generateSuccessor(index, a), 0, curDepth + 1, depth))

        return v

    def maxValue(self, state, index, curDepth, depth):
        if state.isWin() or state.isLose() or curDepth == depth:
            return self.evaluationFunction(state)
        v = -float("inf")
        for a in state.getLegalActions(index):
            v = max(v, self.minValue(state.generateSuccessor(0, a), 1, curDepth, depth))

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
        
        return self.minimax(gameState, self.depth)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def ABS(self, state, depth):
        re = [None]
        v = self.maxValue(state, 0, 0, depth, -float("inf"), float("inf"), re)
        return re[0]

    def minValue(self, state, index, curDepth, depth, alpha, beta):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        v = float("inf")
        for a in state.getLegalActions(index):
            if index < state.getNumAgents()-1:
                v = min(v, self.minValue(state.generateSuccessor(index, a), index+1, curDepth, depth, alpha, beta))
            else:
                v = min(v, self.maxValue(state.generateSuccessor(index, a), 0, curDepth + 1, depth, alpha, beta))
            if v < alpha: return v
            beta = min(beta, v)
        return v

    def maxValue(self, state, index, curDepth, depth, alpha, beta, re = [None]):
        if state.isWin() or state.isLose() or curDepth == depth:
            return self.evaluationFunction(state)
        v = -float("inf")
        for a in state.getLegalActions(index):
            temp = self.minValue(state.generateSuccessor(0, a), 1, curDepth, depth, alpha, beta)
            if temp > v:
                v = temp
                re[0] = a
            if v > beta: return v
            alpha = max(alpha, v)
        return v

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.ABS(gameState, self.depth)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectSearch(self, state, depth):
        maximum = -float("inf")
        result = None
        for action in state.getLegalActions(0):
            temp = self.expectValue(state.generateSuccessor(0, action), 1, 0, depth)
            if temp > maximum:
                maximum = temp
                result = action
        return result

    def expectValue(self, state, index, curDepth, depth):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        v = []
        for a in state.getLegalActions(index):
            if index < state.getNumAgents()-1:
                v.append(self.expectValue(state.generateSuccessor(index, a), index+1, curDepth, depth))
            else:
                v.append(self.maxValue(state.generateSuccessor(index, a), 0, curDepth + 1, depth))

        return sum(v)/len(v)

    def maxValue(self, state, index, curDepth, depth):
        if state.isWin() or state.isLose() or curDepth == depth:
            return self.evaluationFunction(state)
        v = -float("inf")
        for a in state.getLegalActions(index):
            v = max(v, self.expectValue(state.generateSuccessor(0, a), 1, curDepth, depth))

        return v
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectSearch(gameState, self.depth)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    pacPos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    foodPoses = food.asList()
    gPoses = [ghost.getPosition() for ghost in ghostStates]
    gDis = [manhattanDistance(pacPos, gPos) for gPos in gPoses]
    fDis = [manhattanDistance(pacPos, fPos) for fPos in foodPoses]
    cDis = [manhattanDistance(pacPos, cPos) for cPos in currentGameState.getCapsules()]
    #do not get into ghost's house!
    if pacPos in [(10,3), (10,4), (10, 5)]:
        return -9999999999
    
    if min(gDis) > 3 or min(scaredTimes) > 5:
        fScore = 0
        if fDis:
            fScore = 100 - min(fDis) + int(food[pacPos[0]][pacPos[1]]) * 100
        return fScore + currentGameState.getScore()-len(cDis)*10
    else:
        cScore = 0
        if cDis:
            #print(successorGameState.getCapsules(), newPos)
            cScore = int(pacPos in currentGameState.getCapsules()) * 99999999999
        return min(gDis)*10 + cScore
# Abbreviation
better = betterEvaluationFunction

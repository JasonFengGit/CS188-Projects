# myAgents.py
# ---------------
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

from game import Agent
from searchProblems import PositionSearchProblem

import util
import time
import search
from util import *

FOOD = None
"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'):
    global FOOD
    FOOD = None
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """
        "*** YOUR CODE HERE ***"
        '''
        if self.actionIndex == 0:
            self.actions = self.strategy(state)
        else:
            self.actionIndex += 1
        return self.actions[self.actionIndex]
        '''
        
        if not self.path:
            self.path = self.search(state)
        if not self.path:
            return "Stop"
        return self.path.pop()
    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
        
        "*** YOUR CODE HERE"
        self.actionIndex = 0
        self.path = []
        self.going = True
        #raise NotImplementedError()
    def search(self, gameState):
        """Search the node of least total cost first."""
        "*** YOUR CODE HERE ***"
        #34,58,22,25,28,31,34,37,40,43,47,59,61,58,52
        if not self.going:
            return []

        global FOOD

        
        startPosition = gameState.getPacmanPosition(self.index)
        if not FOOD:
            FOOD = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)
        getSucc = problem.getSuccessors
        
        #wid, height = gameState.getWidth(), gameState.getHeight()
        #disLimit = (wid**2 + height**2)/2

        visited = set()
        pq = PriorityQueue()
        pq.push((startPosition, [], 0), 0)
        
        while not pq.isEmpty():
            cur, path, w = pq.pop()
            if FOOD[cur[0]][cur[1]]:
                FOOD[cur[0]][cur[1]] = False
                '''
                print(NUMGOING)
                if NUMGOING > 1 and abs(startPosition[0]-cur[0])**2 + abs(startPosition[1]-cur[1])**2 > disLimit:
                    break
                '''
                return path

            if cur not in visited:
                visited.add(cur)

                for each in getSucc(cur):
                    if each[0] not in visited:
                        pq.push((each[0], [each[1]] + path, w + each[2]), w + each[2])
            
        self.going = False
        return []
    
"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)


        "*** YOUR CODE HERE ***"
        from util import Queue
        getSucc = problem.getSuccessors
        visited = set()
        queue = Queue()
        queue.push((startPosition, []))
        while not queue.isEmpty():
            cur, path = queue.pop()
            if food[cur[0]][cur[1]]:
                return path

            if cur not in visited:
                visited.add(cur)

                for each in getSucc(cur):
                    if each[0] not in visited:
                        queue.push((each[0], path + [each[1]]))
            

        return []

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        #print(sum(sum(each) for each in self.food))
        for each in self.food:
            for isFood in each:
                if isFood:
                    return False
        return True
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


'''
def seperateSearch(self, gameState):
        global zones
        #print(self.index)
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)
        numAgents = gameState.getNumAgents()
        #print(numAgents)
        width = gameState.getWidth()
        height = gameState.getHeight()
        num4 = numAgents//4*4
        if numAgents == 1:
            num4 = 1
        s_w = width/num4/2
        s_h = height/num4/2

        if zones:
            if numAgents == 1:
                return []
            elif numAgents == 4:
                zones = [(s_w,s_h), (s_w + width/2, s_h), (s_w, s_h + height/2), (s_w + width/2, s_h + height/2)]
            elif numAgents == 5:
                zones = [(s_w,s_h), (s_w + width/2, s_h), (s_w, s_h + height/2), (s_w + width/2, s_h + height/2), (width/2, height/2)]
            elif numAgents == 8:
                zones = [(s_w,s_h), (s_w + width/4, s_h), (s_w, s_h + height/4), (s_w + width/4, s_h + height/4),
                        (width/2 + s_w, s_h), (width/2 + s_w, s_h + height/2), (width/2 + s_w + width/4, s_h), (width/2 + s_w + width/4, s_h + height/2)]
        
        self.zone = zones[self.index-1]
        
        def h(state):
            if numAgents == 1:
                return 0
            
            x, y = state
            z_x, z_y = self.zone
            if z_x-s_w < x < z_x+s_w and z_y-s_h < y < z_y+s_h:
                return 0
            else:
                return abs(x-z_x) + abs(y-z_y)
        
        
        getSucc = problem.getSuccessors
        visited = set()
        s = PriorityQueue()
        s.push((startPosition, [], 0), 0)
        while not s.isEmpty():
            cur, path, w = s.pop()
            if food[cur[0]][cur[1]]:
                return path

            if cur not in visited:
                visited.add(cur)

                for each in getSucc(cur):
                    if each[0] not in visited:
                        s.push((each[0], path + [each[1]], w + each[2]), w + each[2] + h(each[0]))
            

        return []
'''

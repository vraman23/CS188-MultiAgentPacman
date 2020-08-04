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
from game import Directions
from game import Actions
from searchProblems import PositionSearchProblem

import util
import time
import search
import random

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""

targets = []
randomTarget = []
paths = {}

def createAgents(num_pacmen, agent='MyAgent'):
    global randomTarget
    global paths
    list = []
    for i in range(num_pacmen):
        randomTarget.append(False)
        paths[i] = []
        list.append(eval(agent)(index = i))
    # return list

    return [ClosestDotAgent(index = 0)]
    # return [eval(agent)(index = 0), SurviveAgent(index = 1), ClosestDotAgent(index = 2), SurviveAgent(index = 3)]


class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def findPath(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition(self.index)
        # food = gameState.getFood().asList()
        # walls = gameState.getWalls()
        global paths
        global randomTarget
        # print(randomTarget)
        "*** YOUR CODE HERE ***"
        path = search.astar(MyFSP(gameState, self.index))
        # if randomTarget[self.index]:
        #     path = search.astar(RandomFSP(gameState, self.index))
        #     randomTarget[self.index] = False
        return path

    def getAction(self, state):
        global paths
        global targets
        if len(paths[self.index]) == 0:
            # print("Agent", self.index, "ate dot at", state.getPacmanPosition(self.index))
            paths[self.index] = self.findPath(state)
            pos = state.getPacmanPosition(self.index)
            if pos in targets:
                targets.remove(pos)
        return paths[self.index].pop(0)

    def initialize(self):
        pass

class MyFSP(PositionSearchProblem):
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
        # self.random = random.choice(self.food.asList())
        self.index = agentIndex

        # self.targets = targets
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
        global targets
        global randomTarget

        dots = self.food.asList()
        if state in dots:
            if state in targets:
                randomTarget[self.index] = True
            else:
                targets.append(state)
            return True
        return False

"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""
class RandomFSP(PositionSearchProblem):
    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()
        self.goal = random.choice(self.food.asList())
        self.index = agentIndex
        # self.targets = targets
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
        global randomTarget
        x,y = state
        return state == self.goal


class ClosestDotAgent(Agent):

    # def foodHeuristic(state, problem):
    #     position, foodGrid = state
    #     dots = foodGrid.asList()
    #
    #     gs = problem.startingGameState
    #     if len(dots) > 0:
    #         xCOM = sum([dot.position.x for dot in dots])/len(dots)
    #         yCOM = sum([dot.position.y for dot in dots])/len(dots)
    #         xy1 = position
    #         xy2 = (xCOM, yCOM)
    #         return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5
    #     else:
    #         return 0

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        global randomTarget
        # startPosition = gameState.getPacmanPosition(self.index)
        # food = gameState.getFood().asList()
        # walls = gameState.getWalls()
        problem = MultiFSP(gameState, self.index)
        random = RandomFSP(gameState, self.index)
        # print(randomTarget)
        "*** YOUR CODE HERE ***"
        path = search.astar(problem)
        if randomTarget[self.index]:
            # print("random")
            path = search.astar(random)
            # randomTarget[self.index] = False
        return path

    def findPathToRandomDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition(self.index)
        # food = gameState.getFood().asList()
        # walls = gameState.getWalls()
        # goal = random.choice(food)
        # print(goal)
        problem = RandomFSP(gameState, self.index)

        "*** YOUR CODE HERE ***"
        return search.astar(problem)

    def getAction(self, state):
        global randomTarget
        # print(randomTarget)
        if len(self.path) == 0:
            # print("Ate dot at", state.getPacmanPosition(self.index))
            self.path = self.findPathToClosestDot(state)
        path = self.path
        # print(path)
        # print(self.path)
        action = path.pop(0)
        self.path = path
        return action

    # def getAction(self, state):
    #     if len(self.paths) == 0:
    #         num = state.getNumAgents()
    #         for index in range(num):
    #             self.paths[index] = []
    #
    #     if len(self.paths[self.index]) == 0:
    #         self.paths[self.index] = self.findPathToClosestDot(state)
    #     path = self.paths[self.index]
    #     action = path.pop(0)
    #     self.paths[self.index] = path
    #     return action

    def initialize(self):
        self.path = []
        # print("Initialized")







class MultiFSP(PositionSearchProblem):
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
        # self.random = random.choice(self.food.asList())
        self.index = agentIndex

        # self.targets = targets
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
        global targets
        global randomTarget
        # print(targets)
        # print(randomTarget)
        # global randomGoal
        dots = self.food.asList()
        "*** YOUR CODE HERE ***"
        # if randomTarget[self.index]:
        #     if state == self.random:
        #         randomTarget[self.index] = False
        #         return True
        # else:
        if state in dots:
            if state not in targets:
                targets.append(state)
                return True
            else:
                randomTarget[self.index] = True
        return False


# class AnyFoodSearchProblem(PositionSearchProblem):
#     """
#     A search problem for finding a path to any food.
#
#     This search problem is just like the PositionSearchProblem, but has a
#     different goal test, which you need to fill in below.  The state space and
#     successor function do not need to be changed.
#
#     The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
#     inherits the methods of the PositionSearchProblem.
#
#     You can use this search problem to help you fill in the findPathToClosestDot
#     method.
#     """
#
#     def __init__(self, gameState, agentIndex):
#         "Stores information from the gameState.  You don't need to change this."
#         # Store the food for later reference
#         self.food = gameState.getFood()
#         self.index = agentIndex
#         # Store info for the PositionSearchProblem (no need to change this)
#         self.walls = gameState.getWalls()
#         self.startState = gameState.getPacmanPosition(agentIndex)
#         self.costFn = lambda x: 1
#         self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE
#
#     def isGoalState(self, state):
#         """
#         The state is Pacman's position. Fill this in with a goal test that will
#         complete the problem definition.
#         """
#         x,y = state
#
#         "*** YOUR CODE HERE ***"
#         if state in self.food.asList():
#             # print(state)
#             return true
#         else:
#             return false

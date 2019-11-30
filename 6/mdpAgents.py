# mapAgents.py
# parsons/11-nov-2017
#
# Version 1.0
#
# A simple map-building to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
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

# The agent here is an extension of the above code written by Simon
# Parsons, based on the code in pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util
import sys

class MDPAgent(Agent):

    def registerInitialState(self, state):
        self.walls = api.walls(state)
        self.nonWalls = []
        (x, y) = self.calcLayoutBounds(state)
        for i in range(x):
            for j in range(y):
                if (i, j) not in self.walls:
                    self.nonWalls.append((i, j))
        self.gamma = 0.5
        self.iterationLimit = 20
        self.actions = ["North", "East", "South", "West"]
        self.updateMap(state)

    def calcLayoutBounds(self, state):
        corners = api.corners(state)
        height = self.getLayoutHeight(corners)
        width  = self.getLayoutWidth(corners)
        return (width, height)

    # This code has been taken from mapAgents.py
    # Which was provided as a solution to practical
    # 05 of the AI module
    def getLayoutHeight(self, corners):
        height = -1
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height + 1

    # This code has been taken from mapAgents.py
    # Which was provided as a solution to practical
    # 05 of the AI module
    def getLayoutWidth(self, corners):
        width = -1
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width + 1

    def updateRewards(self, food, capsules, ghosts):
        self.rewards = {}
        for i in self.nonWalls:
            if i in food:
                self.rewards[i] = 10
            elif i in capsules:
                self.rewards[i] = 20
            # elif i in ghosts:
            #     self.rewards[i] = -100
            else:
                self.rewards[i] = -1
        
        for i in self.nonWalls:
            if i in ghosts:
                self.rewards[i] = -100
                (x, y) = i
                (n, e, s, w) = self.getSurroundingLocations(x, y)
                if n in self.rewards:
                    self.rewards[n] = -50
                if e in self.rewards:
                    self.rewards[e] = -50
                if s in self.rewards:
                    self.rewards[s] = -50
                if w in self.rewards:
                    self.rewards[w] = -50

    def resetValues(self):
        self.values = dict.fromkeys(self.nonWalls, 0)

    def resetPolicy(self):
        self.policy = dict.fromkeys(self.nonWalls, 'North')

    def getSurroundingLocations(self, x, y):
        n = (x, y + 1)
        e = (x + 1, y)
        s = (x, y - 1)
        w = (x - 1, y)
        return (n, e, s, w)

    def expectedUtility(self, x, y, action):
        current = (x,y)
        (nLoc, eLoc, sLoc, wLoc) = self.getSurroundingLocations(x, y)

        # If move results to a wall, stay in original position
        currentValue = self.values[current]
        nValue = self.values[nLoc] if nLoc not in self.walls else currentValue
        eValue = self.values[eLoc] if eLoc not in self.walls else currentValue
        sValue = self.values[sLoc] if sLoc not in self.walls else currentValue
        wValue = self.values[wLoc] if wLoc not in self.walls else currentValue

        if action == 'North':
            return 0.8 * nValue + 0.1 * eValue + 0.1 * wValue
        elif action == 'East':
            return 0.8 * eValue + 0.1 * nValue + 0.1 * sValue
        elif action == 'South':
            return 0.8 * sValue + 0.1 * eValue + 0.1 * wValue
        else:
            return 0.8 * wValue + 0.1 * nValue + 0.1 * sValue

    def argmax(self, utils):
        i = utils.index(max(utils))
        return self.actions[i]

    def policyIteration(self):
        while True:
            self.policyEval()
            same = True
            for k in self.values:
                expectedUtilities = []
                for action in self.actions:
                    expectedUtilities.append(self.expectedUtility(k[0], k[1], action))
                a = self.argmax(expectedUtilities)
                if a != self.policy[k]:
                    self.policy[k] = a
                    same = False
            if same: return

    def policyEval(self):
        for i in range(self.iterationLimit):
            for k in self.values:
                self.values[k] = self.rewards[k] + self.gamma * self.expectedUtility(k[0], k[1], self.policy[k])

    def updateMap(self, state):
        self.updateRewards(api.food(state), api.capsules(state), api.ghosts(state))
        self.resetValues()
        self.resetPolicy()

    def getAction(self, state):
        self.updateMap(state)
        self.policyIteration()
        pacman = api.whereAmI(state)
        legal = api.legalActions(state)
        move = self.policy[pacman]
        return api.makeMove(move, legal)
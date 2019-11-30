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
        # Dictionary of locations that aren't walls
        self.nonWalls = self.getNonWalls(state)
        # Constants for policy iteration
        self.GAMMA = 0.5
        self.ITERATION_LIMIT = 20
        self.ACTIONS = ["North", "East", "South", "West"]
        # Constants for rewards
        self.FOOD = 10
        self.CAPSULE = 20
        self.GHOST = -100
        self.GHOST_ZONE = -50
        self.EMPTY = -1
        # Initialises reward, values (utilities) and policies dictionaries
        self.updateMap(state)

    # Returns dictionary of non wall locations
    def getNonWalls(self, state):
        nonWalls = []
        (x, y) = self.calcLayoutBounds(state)
        for i in range(x):
            for j in range(y):
                if (i, j) not in self.walls:
                    nonWalls.append((i, j))
        return nonWalls

    # Returns width and height of game grid
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

    # Updates the reward dictionary
    def updateRewards(self, food, capsules, ghosts):
        self.rewards = {}
        # For all locations that are not walls
        for i in self.nonWalls:
            # If location contains food
            if i in food:
                self.rewards[i] = self.FOOD
            # If location contains a capsule
            elif i in capsules:
                self.rewards[i] = self.CAPSULE
            # If location contains a capsule
            elif i in ghosts:
                self.rewards[i] = self.GHOST
            # If location is an empty space
            else:
                self.rewards[i] = self.EMPTY

        # Add a negative reward zone around every ghost
        # The zone 1 manhattan distance away from the ghost
        # This is done after the ghosts, food, capsules and empty space
        # To prevent the zone being overwritten
        for i in self.nonWalls:
            if i in ghosts:
                (x, y) = i
                (n, e, s, w) = self.getSurroundingLocations(x, y)
                if n in self.rewards:
                    self.rewards[n] = self.GHOST_ZONE
                if e in self.rewards:
                    self.rewards[e] = self.GHOST_ZONE
                if s in self.rewards:
                    self.rewards[s] = self.GHOST_ZONE
                if w in self.rewards:
                    self.rewards[w] = self.GHOST_ZONE

    # Reset utility dictionary to all zeros
    def resetValues(self):
        self.values = dict.fromkeys(self.nonWalls, 0)

    # Reset policies dictionary. North for example
    def resetPolicy(self):
        self.policy = dict.fromkeys(self.nonWalls, 'North')

    # Returns N, E, S, W positions from given position
    def getSurroundingLocations(self, x, y):
        n = (x, y + 1)
        e = (x + 1, y)
        s = (x, y - 1)
        w = (x - 1, y)
        return (n, e, s, w)

    # Calculates expected utility of a given action at a given position
    def expectedUtility(self, x, y, action):
        current = (x,y)
        (nLoc, eLoc, sLoc, wLoc) = self.getSurroundingLocations(x, y)

        # If move results to a wall, stay in original position
        # Retrieve utilities for N, E, S, W locations
        currentValue = self.values[current]
        nValue = self.values[nLoc] if nLoc not in self.walls else currentValue
        eValue = self.values[eLoc] if eLoc not in self.walls else currentValue
        sValue = self.values[sLoc] if sLoc not in self.walls else currentValue
        wValue = self.values[wLoc] if wLoc not in self.walls else currentValue

        # Apply the transition function to determine expected utility
        if action == 'North':
            return 0.8 * nValue + 0.1 * eValue + 0.1 * wValue
        elif action == 'East':
            return 0.8 * eValue + 0.1 * nValue + 0.1 * sValue
        elif action == 'South':
            return 0.8 * sValue + 0.1 * eValue + 0.1 * wValue
        else:
            return 0.8 * wValue + 0.1 * nValue + 0.1 * sValue

    # Returns action that maximises utility
    # Given list of utlities [N, E, S, W]
    def argmax(self, utils):
        i = utils.index(max(utils))
        return self.ACTIONS[i]

    # Updates policy dictionary with optimum evaluated policy
    def policyIteration(self):
        while True:
            # Evaluate current policy
            self.policyEval()
            same = True
            # For every value in utlity dictionary
            for k in self.values:
                # Determine the action, a,  that maximises utlity
                expectedUtilities = []
                for action in self.ACTIONS:
                    expectedUtilities.append(self.expectedUtility(k[0], k[1], action))
                a = self.argmax(expectedUtilities)
                # If a has changed from previous policy
                if a != self.policy[k]:
                    # Update the policy
                    self.policy[k] = a
                    same = False
            # Stop iterating, policy has converged
            if same: return

    # Evaluate a given policy
    # Used by policy iteration
    def policyEval(self):
        # Implementation of policy evaluation formula from lecture slides
        for i in range(self.ITERATION_LIMIT):
            for k in self.values:
                self.values[k] = self.rewards[k] + self.GAMMA * self.expectedUtility(k[0], k[1], self.policy[k])

    # Before each move, update state of rewards
    # To reflect the state of the game
    # And reset the utilities and policies dictionary
    # To prepare for policy iteration
    def updateMap(self, state):
        self.updateRewards(api.food(state), api.capsules(state), api.ghosts(state))
        self.resetValues()
        self.resetPolicy()

    # Makes the best move according to the optimum evaluated policy
    # Determined by policy iteration
    def getAction(self, state):
        self.updateMap(state)
        self.policyIteration()
        pacman = api.whereAmI(state)
        legal = api.legalActions(state)
        move = self.policy[pacman]
        return api.makeMove(move, legal)
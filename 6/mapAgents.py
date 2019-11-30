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

#
# A class that creates a grid that can be used as a map
#
# The map itself is implemented as a nested list, and the interface
# allows it to be accessed by specifying x, y locations.
#
class Grid:
         
    # Constructor
    #
    # Note that it creates variables:
    #
    # grid:   an array that has one position for each element in the grid.
    # width:  the width of the grid
    # height: the height of the grid
    #
    # Grid elements are not restricted, so you can place whatever you
    # like at each location. You just have to be careful how you
    # handle the elements when you use them.
    def __init__(self, width, height):
        self.width = width
        self.height = height
        subgrid = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                row.append(0)
            subgrid.append(row)

        self.grid = subgrid

    # Print the grid out.
    def display(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[i][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print

    # The display function prints the grid out upside down. This
    # prints the grid out so that it matches the view we see when we
    # look at Pacman.
    def prettyDisplay(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[self.height - (i + 1)][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print
        
    # Set and get the values of specific elements in the grid.
    # Here x and y are indices.
    def setValue(self, x, y, value):
        self.grid[y][x] = value

    def getValue(self, x, y):
        return self.grid[y][x]

    # Return width and height to support functions that manipulate the
    # values stored in the grid.
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

class MDPAgent(Agent):

    def __init__(self):
        print "Running init!"

    def registerInitialState(self, state):
        # print "Running registerInitialState!"
        self.map = self.makeMap(state)
        self.walls = api.walls(state)
        # print self.walls
        self.nonWalls = []
        for i in range(self.map.getWidth()):
            for j in range(self.map.getHeight()):
                if (i, j) not in self.walls:
                    self.nonWalls.append((i, j))
        # print self.nonWalls
        self.values = dict.fromkeys(self.nonWalls, 0)
        # print self.values
        self.policy = dict.fromkeys(self.nonWalls, 'North')
        # print self.policy
        self.rewards = {}
        food = api.food(state)
        capsules = api.capsules(state)
        ghosts = api.ghosts(state)
        self.updateRewards(food, capsules, ghosts)
        # print self.rewards
        self.gamma = 0.5
        self.iterationLimit = 20
        self.actions = ["North", "East", "South", "West"]
        self.ghostZone = {}


    # This is what gets run when the game ends.
    def final(self, state):
        print "Looks like I just died!"

    def makeMap(self, state):
        corners = api.corners(state)
        height = self.getLayoutHeight(corners)
        width  = self.getLayoutWidth(corners)
        return Grid(width, height)

    def getLayoutHeight(self, corners):
        height = -1
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height + 1

    def getLayoutWidth(self, corners):
        width = -1
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width + 1

    def updateRewards(self, food, capsules, ghosts):
        for i in self.nonWalls:
            if i in food:
                self.rewards[i] = 10
            elif i in capsules:
                self.rewards[i] = 20
            # elif i in ghosts:
            #     self.rewards[i] = -100
            #     (x, y) = i
            #     northLoc = (x, y + 1)
            #     eastLoc = (x + 1, y)
            #     southLoc = (x, y - 1)
            #     westLoc = (x - 1, y)
            #     if northLoc in self.rewards:
            #         self.rewards[northLoc] = -50
            #     if eastLoc in self.rewards:
            #         self.rewards[eastLoc] = -50
            #     if southLoc in self.rewards:
            #         self.rewards[southLoc] = -50
            #     if westLoc in self.rewards:
            #         self.rewards[westLoc] = -50
            else:
                self.rewards[i] = -1
        
        for i in self.nonWalls:
            if i in ghosts:
                self.rewards[i] = -100
                (x, y) = i
                northLoc = (x, y + 1)
                eastLoc = (x + 1, y)
                southLoc = (x, y - 1)
                westLoc = (x - 1, y)
                if northLoc in self.rewards:
                    self.rewards[northLoc] = -50
                if eastLoc in self.rewards:
                    self.rewards[eastLoc] = -50
                if southLoc in self.rewards:
                    self.rewards[southLoc] = -50
                if westLoc in self.rewards:
                    self.rewards[westLoc] = -50

    def resetValues(self):
        for i in self.values:
            self.values[i] = 0

    def resetPolicy(self):
        for i in self.policy:
            self.policy[i] = "North"

    def expectedUtility(self, x, y, action):
        currentLoc = (x,y);     currentValue = self.values[currentLoc]
        # If move results to a wall, stay in original position
        northLoc = (x, y + 1);  northValue = self.values[northLoc] if northLoc not in self.walls else currentValue
        eastLoc = (x + 1, y);   eastValue = self.values[eastLoc] if eastLoc not in self.walls else currentValue
        southLoc = (x, y - 1);  southValue = self.values[southLoc] if southLoc not in self.walls else currentValue
        westLoc = (x - 1, y);   westValue = self.values[westLoc] if westLoc not in self.walls else currentValue

        if action == 'North':
            return 0.8*northValue + 0.1*eastValue + 0.1*westValue
        elif action == 'East':
            return 0.8*eastValue + 0.1*northValue + 0.1*southValue
        elif action == 'South':
            return 0.8*southValue + 0.1*eastValue + 0.1*westValue
        else:
            return 0.8*westValue + 0.1*northValue + 0.1*southValue

    def argmax(self, utils):
        i = utils.index(max(utils))
        return self.actions[i]

    def policyIteration(self):
        while True:
            self.policyEvaluation()
            unchanged = True
            for k in self.values:
                expectedUtilities = []
                for action in self.actions:
                    expectedUtilities.append(self.expectedUtility(k[0], k[1], action))
                a = self.argmax(expectedUtilities)
                if a != self.policy[k]:
                    self.policy[k] = a
                    unchanged = False
            if unchanged:
                return

    def policyEvaluation(self):
        for i in range(self.iterationLimit):
            for k in self.values:
                self.values[k] = self.rewards[k] + self.gamma * self.expectedUtility(k[0], k[1], self.policy[k])

    def updateMap(self, state):
        self.updateRewards(api.food(state), api.capsules(state), api.ghosts(state))
        self.resetValues()
        self.resetPolicy()
        self.policyIteration()

    def getAction(self, state):
        self.updateMap(state)
        pacman = api.whereAmI(state)
        legal = api.legalActions(state)
        move = self.policy[pacman]
        # print self.values
        # print move
        return api.makeMove(move, legal)
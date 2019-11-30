# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
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

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

# GoWestAgent
#
# You should write a GoWestAgent, which always tries to have
# Pacman go west on the grid when it is possible. What happens
# when WEST is not a legal move is up to you.
class GoWestAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
            # Always go West if it is an option
        if Directions.WEST in legal:
            return api.makeMove(Directions.WEST, legal)
        # Otherwise pick any other legal action
        return api.makeMove(random.choice(legal), legal)

# HungryAgent 
#
# which uses information about the location of the food to try to
# move towards the nearest food
class HungryAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Get current location of pacman
        pacman = api.whereAmI(state)
        # Get list of food locations
        food = api.food(state)
        # Compute manhattan distance to each food location
        foodDistances = []
        for i in range(len(food)):
            foodDistances.append(util.manhattanDistance(pacman,food[i]))
        # print foodDistances
        minDistance = min(foodDistances)
        # print "Min Distance: ", minDistance
        minDistanceIndex = foodDistances.index(minDistance)
        # print "Min Food index: ", minDistanceIndex
        nearestFood = food[minDistanceIndex]
        # print "Pacman: ", pacman
        # print "Nearest Food: ", nearestFood
        diffX = pacman[0] - nearestFood[0]
        diffY = pacman[1] - nearestFood[1]
        # print "legal", legal
        # print diffX, diffY
        moveX = Directions.STOP
        moveY = Directions.STOP
        # Determine whether to move east or west
        if diffX >= 0:
            # print "Go left"
            moveX = Directions.WEST
        elif diffX < 0:
            # print "Go right"
            moveX = Directions.EAST
        # Determine whether to move north or south
        if diffY >= 0:
            # print "Go down"
            moveY = Directions.SOUTH
        elif diffY < 0:
            # print "Go up"
            moveY = Directions.NORTH
        # Determine whether to move in X or Y
        # print "diffX: ", diffX, " diffY", diffY
        if abs(diffX) >= abs(diffY) and moveX in legal:
            # print moveX
            return api.makeMove(moveX, legal)
        elif abs(diffY) >= 0 and moveY in legal:
            # print moveY
            return api.makeMove(moveY, legal)
        elif abs(diffX) >= 0 and moveX in legal:
            return api.makeMove(moveX, legal)
        else:
            # print "Random"
            return api.makeMove(random.choice(legal), legal)

# SurvivalAgent 
#
# which uses the location of Pacman and the ghosts (and any
# other information that may be helpful) to stay alive as long as possible.
class SurvivalAgent(Agent):

    def getAction(self, state):
        print "-------------"
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Get current location of pacman
        pacman = api.whereAmI(state)
        # Get list of ghost locations
        ghosts = api.ghosts(state)
        # Compute manhattan distance to each ghost location
        ghostsDistances = []
        for i in range(len(ghosts)):
            ghostsDistances.append(util.manhattanDistance(pacman,ghosts[i]))
        minDistance = min(ghostsDistances)
        # print "Min Distance: ", minDistance
        minDistanceIndex = ghostsDistances.index(minDistance)
        # print "Min Ghosts index: ", minDistanceIndex
        nearestGhost = ghosts[minDistanceIndex]
        # print "Pacman: ", pacman
        # print "Nearest Ghost: ", nearestGhost
        diffX = pacman[0] - nearestGhost[0]
        diffY = pacman[1] - nearestGhost[1]
        # print "legal", legal
        # print diffX, diffY
        moveX = Directions.STOP
        moveY = Directions.STOP
        # Determine whether to move east or west
        if diffX >= 0:
            # print "Go right"
            moveX = Directions.EAST
        elif diffX < 0:
            # print "Go left"
            moveX = Directions.WEST
        # Determine whether to move north or south
        if diffY >= 0:
            # print "Go up"
            moveY = Directions.NORTH
        elif diffY < 0:
            # print "Go down"
            moveY = Directions.SOUTH
        # Determine whether to move in X or Y
        # print "diffX: ", diffX, " diffY", diffY
        if abs(diffX) >= abs(diffY) and moveX in legal:
            # print moveX
            return api.makeMove(moveX, legal)
        elif abs(diffY) >= 0 and moveY in legal:
            # print moveY
            return api.makeMove(moveY, legal)
        elif abs(diffX) >= 0 and moveX in legal:
            # print moveX
            return api.makeMove(moveX, legal)
        else:
            print "Best Random"
            # print legal
            # For each legal, calculate where it would take you
            legals = {}
            for i in range(len(legal)):
                if legal[i] == Directions.NORTH:
                    legals[legal[i]] = (pacman[0], pacman[1] + 1)
                if legal[i] == Directions.EAST:
                    legals[legal[i]] = (pacman[0] + 1, pacman[1])
                if legal[i] == Directions.SOUTH:
                    legals[legal[i]] = (pacman[0], pacman[1] - 1)
                if legal[i] == Directions.WEST:
                    legals[legal[i]] = (pacman[0] - 1, pacman[1])
            print legals
            # For each legal move location, calculate how far from the ghost it is
            for k in legals:
                legals[k] = util.manhattanDistance(legals[k], nearestGhost)
            print legals
            # Pick the move that has largest distance
            bestLegalDistance = 0
            bestLegal = Directions.STOP
            for k in legals:
                if legals[k] >= bestLegalDistance:
                    bestLegal = k
                    bestLegalDistance = legals[k]
            print "bestLegal", bestLegal
            return api.makeMove(bestLegal, legal)
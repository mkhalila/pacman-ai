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
            print util.manhattanDistance(pacman, theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)

        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)

        # Where are the corners?
        print "corners locations: "
        print api.corners(state)

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
            foodDistances.append(util.manhattanDistance(pacman, food[i]))
        print foodDistances
        minDistance = min(foodDistances)
        print "Min Distance: ", minDistance
        minDistanceIndex = foodDistances.index(minDistance)
        print "Min Food index: ", minDistanceIndex
        nearestFood = food[minDistanceIndex]
        print "Pacman: ", pacman
        print "Nearest Food: ", nearestFood
        diffX = pacman[0] - nearestFood[0]
        diffY = pacman[1] - nearestFood[1]
        print "legal", legal
        print diffX, diffY
        moveX = Directions.STOP
        moveY = Directions.STOP
        # Determine whether to move east or west
        if diffX >= 0:
            print "Go left"
            moveX = Directions.WEST
        elif diffX < 0:
            print "Go right"
            moveX = Directions.EAST
        # Determine whether to move north or south
        if diffY >= 0:
            print "Go down"
            moveY = Directions.SOUTH
        elif diffY < 0:
            print "Go up"
            moveY = Directions.NORTH
        # Determine whether to move in X or Y
        print "diffX: ", diffX, " diffY", diffY
        if abs(diffX) >= abs(diffY) and moveX in legal:
            return api.makeMove(moveX, legal)
        elif abs(diffY) >= 0 and moveY in legal:
            return api.makeMove(moveY, legal)
        else:
            return api.makeMove(random.choice(legal), legal)

# SurvivalAgent
#
# which uses the location of Pacman and the ghosts (and any
# other information that may be helpful) to stay alive as long as possible.


class SurvivalAgent(Agent):

    def getAction(self, state):
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
            ghostsDistances.append(util.manhattanDistance(pacman, ghosts[i]))
        minDistance = min(ghostsDistances)
        print "Min Distance: ", minDistance
        minDistanceIndex = ghostsDistances.index(minDistance)
        print "Min Ghosts index: ", minDistanceIndex
        nearestGhost = ghosts[minDistanceIndex]
        print "Pacman: ", pacman
        print "Nearest Ghost: ", nearestGhost
        diffX = pacman[0] - nearestGhost[0]
        diffY = pacman[1] - nearestGhost[1]
        print "legal", legal
        print diffX, diffY
        moveX = Directions.STOP
        moveY = Directions.STOP
        # Determine whether to move east or west
        if diffX >= 0:
            print "Go right"
            moveX = Directions.EAST
        elif diffX < 0:
            print "Go left"
            moveX = Directions.WEST
        # Determine whether to move north or south
        if diffY >= 0:
            print "Go up"
            moveY = Directions.NORTH
        elif diffY < 0:
            print "Go down"
            moveY = Directions.SOUTH
        # Determine whether to move in X or Y
        print "diffX: ", diffX, " diffY", diffY
        if abs(diffX) >= abs(diffY) and moveX in legal:
            return api.makeMove(moveX, legal)
        elif abs(diffY) >= 0 and moveY in legal:
            return api.makeMove(moveY, legal)
        elif abs(diffX) >= 0 and moveX in legal:
            return api.makeMove(moveX, legal)
        else:
            return api.makeMove(random.choice(legal), legal)

class CornerSeekingAgent(Agent):

    # Constructor
    #
    # Create variables to remember target positions
    def __init__(self):
         self.BL = False
         self.TL = False
         self.BR = False
         self.TR = False

    def final(self, state):
         self.BL = False
         self.TL = False
         self.BR = False
         self.TR = False
        
    def getAction(self, state):

        # Get extreme x and y values for the grid
        corners = api.corners(state)
        print corners
        # Setup variable to hold the values
        minX = 100
        minY = 100
        maxX = 0
        maxY = 0
        
        # Sweep through corner coordinates looking for max and min
        # values.
        for i in range(len(corners)):
            cornerX = corners[i][0]
            cornerY = corners[i][1]
            
            if cornerX < minX:
                minX = cornerX
            if cornerY < minY:
                minY = cornerY
            if cornerX > maxX:
                maxX = cornerX
            if cornerY > maxY:
                maxY = cornerY

        bl = (minX, minY)
        tl = (minX, maxY)
        br = (maxX, minY)
        tr = (maxX, maxY)
        print "a: ", bl, tl, br, tr

        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        print legal
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Where is Pacman now?
        pacman = api.whereAmI(state)
        print "p", pacman

        # Find nearest unvisited corner
        nearestCorner = corners[0]
        nearestCornerDistance = util.manhattanDistance(pacman, corners[0])
        for i in range(1, len(corners)):
            cornerDistance = util.manhattanDistance(pacman, corners[i])
            if cornerDistance < nearestCornerDistance:
                nearestCornerDistance = cornerDistance
                nearestCorner = corners[i]

        print nearestCorner
        #
        # If we haven't got to the lower left corner, try to do that
        #
        
        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == minY + 1:
                print "Got to BL!"
                self.BL = True

        # If not, move towards it, first to the West, then to the South.
        if self.BL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
        #
        # Now we've got the lower left corner
        #

        # Move towards the top left corner
        
        # Check we aren't there:
        if pacman[0] == minX + 1:
           if pacman[1] == maxY - 1:
                print "Got to TL!"
                self.TL = True

        # If not, move West then North.
        if self.TL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Now, the top right corner
        
        # Check we aren't there:
        if pacman[0] == maxX - 1:
           if pacman[1] == maxY - 1:
                print "Got to TR!"
                self.TR = True

        # Move east where possible, then North
        if self.TR == False:
            if pacman[0] < maxX - 1:
                if Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Fromto right it is a straight shot South to get to the bottom right.
        
        if pacman[0] == maxX - 1:
           if pacman[1] == minY + 1:
                print "Got to BR!"
                self.BR = True
                return api.makeMove(Directions.STOP, legal)
           else:
               print "Nearly there"
               return api.makeMove(Directions.SOUTH, legal)

        print "Not doing anything!"
        return api.makeMove(Directions.STOP, legal)


class HungryCornerSeekingAgent(Agent):

    # Constructor
    #
    # Create variables to remember target positions
    def __init__(self):
        self.last = Directions.STOP
        self.BL = False
        self.TL = False
        self.BR = False
        self.TR = False

    def final(self, state):
        self.last = Directions.STOP
        self.BL = False
        self.TL = False
        self.BR = False
        self.TR = False

    def getAction(self, state):
        # Get extreme x and y values for the grid
        corners = api.corners(state)
        # print corners
        food = api.food(state)
        pacman = api.whereAmI(state)
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        print legal
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        print pacman
        print food

        # Setup variable to hold the values
        minX = 100
        minY = 100
        maxX = 0
        maxY = 0

        # Sweep through corner coordinates looking for max and min
        # values.
        for i in range(len(corners)):
            cornerX = corners[i][0]
            cornerY = corners[i][1]

            if cornerX < minX:
                minX = cornerX
            if cornerY < minY:
                minY = cornerY
            if cornerX > maxX:
                maxX = cornerX
            if cornerY > maxY:
                maxY = cornerY

        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == minY + 1:
                print "Got to BL!"
                self.BL = True

        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == maxY - 1:
                print "Got to TL!"
                self.TL = True

        # Check we aren't there:
        if pacman[0] == maxX - 1:
            if pacman[1] == maxY - 1:
                print "Got to TR!"
                self.TR = True


        if pacman[0] == maxX - 1:
            if pacman[1] == minY + 1:
                print "Got to BR!"
                self.BR = True
        
        # If there is food nearby, be a hungry agent
        if len(food) > 0:
            print "Being hungry"
            foodDistances = []
            for i in range(len(food)):
                foodDistances.append(util.manhattanDistance(pacman, food[i]))
            minDistance = min(foodDistances)
            minDistanceIndex = foodDistances.index(minDistance)
            nearestFood = food[minDistanceIndex]
            diffX = pacman[0] - nearestFood[0]
            diffY = pacman[1] - nearestFood[1]
            moveX = Directions.STOP
            moveY = Directions.STOP
            if diffX >= 0:
                moveX = Directions.WEST
            elif diffX < 0:
                moveX = Directions.EAST
            if diffY >= 0:
                moveY = Directions.SOUTH
            elif diffY < 0:
                moveY = Directions.NORTH
            if abs(diffX) >= abs(diffY) and moveX in legal:
                return api.makeMove(moveX, legal)
            elif abs(diffY) >= 0 and moveY in legal:
                return api.makeMove(moveY, legal)
            elif abs(diffX) >= 0 and moveX in legal:
                return api.makeMove(moveX, legal)
            else:
                return api.makeMove(random.choice(legal), legal)
        # Otherwise be a corner seeking agent
        else:
            print "Corner seeking"
            #
            # If we haven't got to the lower left corner, try to do that
            #

            # If not, move towards it, first to the West, then to the South.
            if self.BL == False:
                if pacman[0] > minX + 1:
                    if Directions.WEST in legal:
                        return api.makeMove(Directions.WEST, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)
                else:
                    if Directions.SOUTH in legal:
                        return api.makeMove(Directions.SOUTH, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)
            #
            # Now we've got the lower left corner
            #

            # Move towards the top left corner

            # If not, move West then North.
            if self.TL == False:
                if pacman[0] > minX + 1:
                    if Directions.WEST in legal:
                        return api.makeMove(Directions.WEST, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)
                else:
                    if Directions.NORTH in legal:
                        return api.makeMove(Directions.NORTH, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)

            # Now, the top right corner

            # Move east where possible, then North
            if self.TR == False:
                if pacman[0] < maxX - 1:
                    if Directions.EAST in legal:
                        return api.makeMove(Directions.EAST, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)
                else:
                    if Directions.NORTH in legal:
                        return api.makeMove(Directions.NORTH, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)

            # Now, the bottom right corner
            # Move east where possible, then South
            if self.BR == False:
                if pacman[0] < maxX - 1:
                    if Directions.EAST in legal:
                        return api.makeMove(Directions.EAST, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)
                else:
                    if Directions.SOUTH in legal:
                        return api.makeMove(Directions.SOUTH, legal)
                    else:
                        pick = random.choice(legal)
                        return api.makeMove(pick, legal)

            # Fromto right it is a straight shot South to get to the bottom right.

            # if pacman[0] == maxX - 1:
            #     if pacman[1] == minY + 1:
            #         print "Got to BR!"
            #         self.BR = True
            #         return api.makeMove(Directions.STOP, legal)
            #     else:
            #         print "Nearly there"
            #         return api.makeMove(Directions.SOUTH, legal)

            print "Being Randomish"
            if self.last in legal:
                return api.makeMove(self.last, legal)
            else:
                pick = random.choice(legal)
                # Since we changed action, record what we did
                self.last = pick
                return api.makeMove(pick, legal)

class HungryCornerSeekingSurvivalAgent(Agent):

    # Constructor
    #
    # Create variables to remember target positions
    def __init__(self):
        self.last = Directions.STOP
        self.BL = False
        self.TL = False
        self.BR = False
        self.TR = False

    def final(self, state):
        self.last = Directions.STOP
        self.BL = False
        self.TL = False
        self.BR = False
        self.TR = False

    def getAction(self, state):
        print "--------------------"
        # Get extreme x and y values for the grid
        corners = api.corners(state)
        # print corners
        food = api.food(state)
        pacman = api.whereAmI(state)
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        # print legal
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # print pacman
        # print food

        # Setup variable to hold the values
        minX = 100
        minY = 100
        maxX = 0
        maxY = 0

        # Sweep through corner coordinates looking for max and min
        # values.
        for i in range(len(corners)):
            cornerX = corners[i][0]
            cornerY = corners[i][1]

            if cornerX < minX:
                minX = cornerX
            if cornerY < minY:
                minY = cornerY
            if cornerX > maxX:
                maxX = cornerX
            if cornerY > maxY:
                maxY = cornerY

        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == minY + 1:
                # print "Got to BL!"
                self.BL = True

        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == maxY - 1:
                # print "Got to TL!"
                self.TL = True

        # Check we aren't there:
        if pacman[0] == maxX - 1:
            if pacman[1] == maxY - 1:
                # print "Got to TR!"
                self.TR = True


        if pacman[0] == maxX - 1:
            if pacman[1] == minY + 1:
                # print "Got to BR!"
                self.BR = True

        ghosts = api.ghosts(state)

        # If can hear a ghost, become worried
        print ghosts
        if len(ghosts) > 0:
            print "Being Survival"
            ghostsDistances = []
            for i in range(len(ghosts)):
                ghostsDistances.append(util.manhattanDistance(pacman, ghosts[i]))
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
                return api.makeMove(moveX, legal)
            elif abs(diffY) >= 0 and moveY in legal:
                return api.makeMove(moveY, legal)
            elif abs(diffX) >= 0 and moveX in legal:
                return api.makeMove(moveX, legal)
            else:
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
        # Else be HungryCornerSeekingAgent
        else:
            # print "Being HungryCornerSeekingAgent"
            # If there is food nearby, be a hungry agent
            if len(food) > 0:
                print "Being hungry"
                foodDistances = []
                for i in range(len(food)):
                    foodDistances.append(util.manhattanDistance(pacman, food[i]))
                minDistance = min(foodDistances)
                minDistanceIndex = foodDistances.index(minDistance)
                nearestFood = food[minDistanceIndex]
                diffX = pacman[0] - nearestFood[0]
                diffY = pacman[1] - nearestFood[1]
                moveX = Directions.STOP
                moveY = Directions.STOP
                if diffX >= 0:
                    moveX = Directions.WEST
                elif diffX < 0:
                    moveX = Directions.EAST
                if diffY >= 0:
                    moveY = Directions.SOUTH
                elif diffY < 0:
                    moveY = Directions.NORTH
                if abs(diffX) >= abs(diffY) and moveX in legal:
                    return api.makeMove(moveX, legal)
                elif abs(diffY) >= 0 and moveY in legal:
                    return api.makeMove(moveY, legal)
                elif abs(diffX) >= 0 and moveX in legal:
                    return api.makeMove(moveX, legal)
                else:
                    return api.makeMove(random.choice(legal), legal)
            # Otherwise be a corner seeking agent
            else:
                print "Corner seeking"
                #
                # If we haven't got to the lower left corner, try to do that
                #

                # If not, move towards it, first to the West, then to the South.
                if self.BL == False:
                    if pacman[0] > minX + 1:
                        if Directions.WEST in legal:
                            return api.makeMove(Directions.WEST, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                    else:
                        if Directions.SOUTH in legal:
                            return api.makeMove(Directions.SOUTH, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                #
                # Now we've got the lower left corner
                #

                # Move towards the top left corner

                # If not, move West then North.
                if self.TL == False:
                    if pacman[0] > minX + 1:
                        if Directions.WEST in legal:
                            return api.makeMove(Directions.WEST, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                    else:
                        if Directions.NORTH in legal:
                            return api.makeMove(Directions.NORTH, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)

                # Now, the top right corner

                # Move east where possible, then North
                if self.TR == False:
                    if pacman[0] < maxX - 1:
                        if Directions.EAST in legal:
                            return api.makeMove(Directions.EAST, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                    else:
                        if Directions.NORTH in legal:
                            return api.makeMove(Directions.NORTH, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)

                # Now, the bottom right corner
                # Move east where possible, then South
                if self.BR == False:
                    if pacman[0] < maxX - 1:
                        if Directions.EAST in legal:
                            return api.makeMove(Directions.EAST, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                    else:
                        if Directions.SOUTH in legal:
                            return api.makeMove(Directions.SOUTH, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)

                # Fromto right it is a straight shot South to get to the bottom right.

                # if pacman[0] == maxX - 1:
                #     if pacman[1] == minY + 1:
                #         print "Got to BR!"
                #         self.BR = True
                #         return api.makeMove(Directions.STOP, legal)
                #     else:
                #         print "Nearly there"
                #         return api.makeMove(Directions.SOUTH, legal)

                print "Being Randomish"
                if self.last in legal:
                    return api.makeMove(self.last, legal)
                else:
                    pick = random.choice(legal)
                    # Since we changed action, record what we did
                    self.last = pick
                    return api.makeMove(pick, legal)

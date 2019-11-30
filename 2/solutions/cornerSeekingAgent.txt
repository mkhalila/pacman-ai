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

        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        print legal
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Where is Pacman now?
        pacman = api.whereAmI(state)
        print pacman
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

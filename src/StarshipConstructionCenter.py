'''
Created on Aug 20, 2013

@author: tstephen
'''


class StarshipConstructionCenter():
    '''
    This is the basic Starship Construction Center class
    '''


    def __init__( self, sscClass, name = "" ):
        '''
        Initialize the Starship Construction Center
        '''
        self.shipQueue = []
        self.totalHullSizes = 0
        self.isLoaded = False
        self.workload = []
        self.destroyed = False
        if ( '' == name ):
            name = "Type %s Construction Center" % sscClass
        self.name = name

        if ( 1 == sscClass ):
            self.maxHullSize = 20
            self.maxMilitaryHullSize = 20
            self.maxTotalHullSizes = 140
            self.hullProbabilty = 1.0
            self.onlySystemShips = False
        elif ( 2 == sscClass ):
            self.maxHullSize = 14
            self.maxMilitaryHullSize = 6
            self.maxTotalHullSizes = 50
            self.hullProbabilty = 0.75
            self.onlySystemShips = False
        elif ( 3 == sscClass ):
            self.maxHullSize = 20
            self.maxMilitaryHullSize = 0
            self.maxTotalHullSizes = 20
            self.hullProbabilty = 0.35
            self.onlySystemShips = True
        elif ( 4 == sscClass ):
            self.maxHullSize = 5
            self.maxMilitaryHullSize = 3
            self.maxTotalHullSizes = 20
            self.hullProbabilty = 1.0
            self.onlySystemShips = True
        elif ( 5 == sscClass ):  # this is a generic SCC you must set the max number of hull points
            self.maxHullSize = 20
            self.maxMilitaryHullSize = 20
            self.maxTotalHullSizes = 0
            self.hullProbabilty = 1.0
            self.onlySystemShips = False
        else:
            raise Exception( "Only class 1-5 starship construction centers are defined." )
        self.nextShipSize = self.maxTotalHullSizes
        self.timeToHullSize = {}


    def getMaxHullSize( self ): return self.maxHullSize
    def getMaxMilitaryHullSize( self ): return self.maxMilitaryHullSize
    def getMaxTotalHullSizes( self ): return self.maxTotalHullSizes
    def getHullProbability( self ): return self.hullProbabilty
    def getOnlySystemShips( self ): return self.onlySystemShips
    def getCurrentHullSizeTotal( self ): return self.totalHullSizes
    def getNextShipSize( self ): return self.nextShipSize
    def getName( self ): return self.name

    def update( self , day ):
        '''
        Updates the status of the ships in the SCC and the SCC state
        
        Returns a list of ships that have finished their construction/repairs
        '''
        finishedList = []
        if ( len( self.workload ) ):
#            print self.name, len( self.workload ), len( self.shipQueue ), self.totalHullSizes
            self.workload.pop( 0 ) # that was yesterday's loading
            if ( not len( self.workload ) ):
                self.workload.append( 0 )
            self.nextShipSize = self.maxTotalHullSizes - self.workload[0]
            self.totalHullSizes = self.workload[0]
        for ship in list( self.shipQueue ):
            complete = ship.update( day )
            # if complete
            if ( complete ):
                self.shipQueue.remove( ship )
                finishedList.append( ship )
            # calculate time to HS for HS range allowed
            date = 0
            hullSize = 1
            for hullCount in self.workload:
                while ( self.maxTotalHullSizes - hullCount >= hullSize and hullSize <= 20 ):
                    self.timeToHullSize[hullSize] = date
                    hullSize += 1
                date += 1
        return finishedList

    def getAvailableSpace( self ):
        return self.maxTotalHullSizes - self.totalHullSizes

    def addToQueue( self, ship ):
        if ( ship.getHullSize() > self.nextShipSize ):  # can't add a ship we don't have space for
            raise ValueError( "Ship size is too large for available space" )
        self.isLoaded = True
        self.shipQueue.append( ship )  #add it to the queue
        self.totalHullSizes += ship.getHullSize()
        self.nextShipSize -= ship.getHullSize()
        if ( not ship.isNew() ):  #if it is in for repairs calcuate the repair time
            ship.startMaintenance( ship.getYearsBetweenMaintenance() )
        daysInSCC = ship.getDaysRemaining()  #number of days the ship will be in the shop
        count = 0
        if ( daysInSCC <= len( self.workload ) ):  # our workflow list extends beyond that time
            while ( count < daysInSCC ):  # add in the hull size to the workload for each of those days
                self.workload[count] = self.workload[count] + ship.getHullSize()
                count += 1
        else:  # our workload list isn't long enough for the days to add
            for i, hullCount in enumerate( self.workload ):  #add the hull size on to every day in the list
                self.workload[i] = hullCount + ship.getHullSize()
                count += 1
            while ( count < daysInSCC ):  # then extend the list by the remaining days
                self.workload.append( ship.getHullSize() )
                count += 1
    def loaded( self ): return self.isLoaded
    def clearLoaded( self ): self.isLoaded = False
    def queueSize( self ): return len( self.shipQueue )
    def shipsInQueue( self ): return self.shipQueue

    def clearQueue( self ):
        self.shipQueue = []
        self.totalHullSizes = 0
        self.shipsInQueue = 0

    def markDestroyed( self ):
        self.destroyed = True

    def isDestroyed( self ): return self.destroyed


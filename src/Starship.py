'''
Created on Aug 20, 2013

@author: tstephen
'''
import random

class Starship():
    '''
    Basic starship class
    '''
    random.seed()


    def __init__( self, size, shipType, years ):
        '''
        Create a ship for the starship construction queue
        
        hullSize - the hull size of the ship
        type - 'civilian' or 'military'
        newShip - boolean flag for whether this is a new ship construction or existing ship in for maintenance
        days - number of days of maintenance for exiting ship
        '''
        if ( 'civilian' == shipType or 'military' == shipType ):
            self.shipType = shipType
        else:
            raise ValueError( "Incorrect ship type" )
        if ( size in range( 1, 21 ) ):
            self.hullSize = size
        else:
            raise ValueError( "Hull size not in 1-20 range" )

        self.daysLeft = self.hullSize * 30
        self.yearsBetweenMaintenance = years
        self.dateCreated = 0
        self.timeToNextMaintenance = 0
        self.newShip = True
        self.passedCount = 0  # number of days the ship has been skipped over in the lists

    def getType( self ): return self.shipType
    def getHullSize( self ): return self.hullSize
    def getDaysRemaining( self ): return self.daysLeft
    def setCreationDate( self, day ):
        self.dateCreated = day
        self.daysLeft = 0
        self.setRepairsCompleted( day )
    def getTimeToNextMaintenance( self ): return self.timeToNextMaintenance
    def setRepairsCompleted( self, day ):
        self.timeToNextMaintenance = day + 400 * self.yearsBetweenMaintenance
    def startMaintenance( self, years ):
        self.daysLeft = self.hullSize
        while ( years > 0 ):
            self.daysLeft += random.randint( 1, 10 )
            years -= 1
    def isNew( self ): return self.newShip
    def update( self, day ):
        '''
        This method updates the status of the ship decrementing the time in dock (daysLeft)
        or time until next maintenance as appropriate.
        
        Returns True if the ship is in dock and repairs/construction is completed or if it is
        out of dock and it is time for maintenance.
        
        Returns False if the state shouldn't change
        '''
        #First handle ships in a SCC
        if ( self.daysLeft ):
            self.daysLeft -= 1
            if ( 0 == self.daysLeft ): # we're done
                if ( False == self.newShip ):  # in for repairs
                    self.setRepairsCompleted( day )  #Start the count down to the next maintenance
                else:  # new ship construction completed
                    self.setCreationDate( day )
                    self.newShip = False
                return True  # we're done, get us out of the SCC
            else:
                return False  # still more work to be done

        # Next handle the ships that are not under construction/repair
        if ( day >= self.timeToNextMaintenance ):  #We've passed the maintenance date
            return True  # Things are falling apart and we need repairs
        else:
            return False  # Smooth sailing
        return False  #should never hit this one but just in case
    def incrementPassedCount( self ): self.passedCount += 1
    def getPassedCount( self ): return self.passedCount
    def getYearsBetweenMaintenance( self ): return self.yearsBetweenMaintenance

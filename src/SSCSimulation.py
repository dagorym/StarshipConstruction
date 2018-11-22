#!/usr/bin/python
'''
Created on Aug 20, 2013

@author: tstephen
'''

import random
import math
import sys

from StarshipConstructionCenter import StarshipConstructionCenter
from Starship import Starship


def createSSCList():
    '''
    Created on Aug 22, 2013
    
    @author Tom Stephens
    
    Generate the list of starship construction centers
    '''
    centers = []
    sccList = {
               "Hentz" : 4,
               "Yast" : 4,
               "Rupert's Hole" : 4,
               "Triad" : 4,
               "Laco" : 4,
               "Inner Reach" : 4,
               "OuterReach" : 4,
               "Groth" : 4,
               "Terledrom" : 4,
               "Hargut" : 4,
               "Ken'zah Kit" : 4,
               "Zik-kit" : 4,
               "Kdikit" : 4,
               "GranQuivera" : 4,
               "Morgain's World" : 4,
               "Histran" : 4,
               "Hakosoar" : 4,
               "Minotaru" : 4,
               "Lossend" : 4,
               "Pale" : 4,
               "New Pale" : 4,
               "Clarion" : 4,
               "Hentz SSC" : 2,
               "Rupert's Hole SSC" : 3,
               "Triad SSC" : 1,
               "Outer Reach SSC" : 3,
               "Terledrom SSC" : 2,
               "Gran Quivera SSC" : 1,
               "Minotaur SSC" : 2,
               "Pale SSC" : 3,
               "Clarion SSC" : 3,
#            "Test SSC" : 4,
               }
    for key in sccList:
        centers.append( StarshipConstructionCenter( sccList[key], key ) )
    return centers

def getHullSize( mean = None ):
    '''
    Created on Aug 22, 2013
    
    @author Tom Stephens
    
    Generate random hull size from a distribution.
    
    @param mean: The median of the distribution to use.  If 'None' then the hull size is just
    random from 1 to 20
    '''
    if( None == mean ):
        #ave = random.randint( 1, 20 )
        #ave = int( ( random.randint( 1, 20 ) + 20 - math.sqrt( random.randint( 1, 400 ) ) ) / 2 )
        if ( len( sys.argv ) > 2 ):
            ave = int( sys.argv[2] )
        else:
#             ave = random.randint( 1, 20 )
            
#            ave = random.randint( 1, 11 ) + random.randint( 1, 12 ) - 3
#            if ( ave < 1 ): ave = 3

            roll = random.randint( 1, 55 ) #165 )
            if ( roll < 12 ):
                ave = 1
            elif ( roll < 23 ):
                ave = 2
            elif ( roll < 34 ):
                ave = 3
            elif ( roll < 45 ):
                ave = 4
            elif ( roll < 56 ):
                ave = 5
            elif ( roll < 67 ):
                ave = 6
            elif ( roll < 78 ):
                ave = 7
            elif ( roll < 89 ):
                ave = 8
            elif ( roll < 100 ):
                ave = 9
            elif ( roll < 111 ):
                ave = 10
            elif ( roll < 121 ):
                ave = 11
            elif ( roll < 130 ):
                ave = 12
            elif ( roll < 138 ):
                ave = 13
            elif ( roll < 145 ):
                ave = 14
            elif ( roll < 151 ):
                ave = 15
            elif ( roll < 156 ):
                ave = 16
            elif ( roll < 160 ):
                ave = 17
            elif ( roll < 163 ):
                ave = 18
            elif ( roll < 165 ):
                ave = 19
            else:
                ave = 20
            if(random.randint(1,3) == 1):
                ave = random.randint(1,3)

        return ave

def generateNewShipList( ships ):
    '''
    Created on Aug 22, 2013
    
    @author Tom Stephens
    
    Generate a list of 100 ships waiting to be constructed
    '''
    if ( len( sys.argv ) > 1 ):
        years = int( sys.argv[1] )
    else:
        years = 1 #number of years between maintenance
    for x in range( 100 ):
        hullSize = getHullSize()
        ships.append( Starship( hullSize, 'civilian', years ) )
        generateNewShipList.totalShipsGenerated += 1
        generateNewShipList.totalHullsGenerated += hullSize
    return ships
generateNewShipList.totalShipsGenerated = 0
generateNewShipList.totalHullsGenerated = 0

if __name__ == '__main__':
    print "#Running Star Ship Construction Simulation."
    sccs = createSSCList()
    ships = []
    newShips = []
    repairShips = []
    shipDist = {}
    day = 1
    daysToSimulate = 40000


    while ( day <= daysToSimulate ):
        if ( len( newShips ) == 0 ):
            generateNewShipList( newShips )
        for ship in list( ships ):
            needsRepair = ship.update( day )
            if ( needsRepair ):
                ships.remove( ship )
                repairShips.append( ship )
        for scc in sccs:
            # update SSC status and get list of any finished ships
            finshedShips = scc.update( day )
            # add any new ships to completed ships list
            for ship in finshedShips:
                ships.append( ship );
        #loop over each scc
        for scc in sccs:
            #get available hull space
            ahs = scc.getAvailableSpace()
            #add first maintenance ship that will fit
            for ship in list( repairShips ):
                if ( ahs and ship.getHullSize() <= ahs and ship.getHullSize() <= scc.getMaxHullSize()):
                    scc.addToQueue( ship )
                    repairShips.remove( ship )
                    ahs -= ship.getHullSize()
                    #break
        #loop over each unloaded ssc
        firstShipPos = 0;
        for scc in sccs:
#            if ( scc.loaded() ): continue  #skip the ones that have had ships added already
            # make sure we always have at least 100 ships in the queue
            if ( 300 > len( newShips ) ):
                generateNewShipList( newShips )
            #get available hull space
            ahs = scc.getAvailableSpace()
            #add first new ship that will fit
            newCount = 0
            for ship in list( newShips ):
                #@todo Need to address prioritizing passed over ships
                if ( ship.getHullSize() <= ahs and ship.getHullSize() <= scc.getMaxHullSize()):
                    scc.addToQueue( ship )
                    shipPos = newShips.index( ship );
                    if ( shipPos > firstShipPos ): firstShipPos = shipPos #record position of last ship added
                    newShips.remove( ship )
                    ahs -= ship.getHullSize()
                    newCount += 1
                    if ( newCount > 10 ):
                        break
        #increment passed over counter for all ships by passed from queue
        for i, ship in enumerate( newShips ):
            ship.incrementPassedCount()
            if (ship.getPassedCount() > 400):
                newShips.remove( ship )
            if ( i > firstShipPos ): break
#         for ship in newShips:
#             if (ship.getPassedCount() > 400):
#                 newShips.remove( ship )

        #clear loaded flag on SSC
        for scc in sccs:
            scc.clearLoaded()

        # generate yearly statistics
        totalShips = len( ships ) + len( repairShips )
        for scc in sccs:
            totalShips += scc.queueSize()
        if ( not day % 100 ):
            print day, totalShips, len( ships ), len( repairShips )
        day += 1
    # generate final statistics
    totalHullSize = 0;
    for x in range(20):
        shipDist[x+1] = 0
    for ship in ships:
        totalHullSize += ship.getHullSize()
        shipDist[ship.getHullSize()] += 1
    for ship in repairShips:
        totalHullSize += ship.getHullSize()
        shipDist[ship.getHullSize()] += 1
    for scc in sccs:
        for ship in scc.shipsInQueue():
            totalHullSize += ship.getHullSize()
            shipDist[ship.getHullSize()] += 1
    print "#Total ships = %d" % totalShips
    print "#Average Hull Size =", ( float( totalHullSize ) / totalShips )
    print "Hull Size Distribution"
    for x in range(20):
        print "  ", x+1, ":  ", shipDist[x+1]
    totalNewHullSize = 0
    newShipCount = 0
    for ship in newShips:
        if ( ship.getPassedCount() > 0 ):
#            print ship.getHullSize(), ship.getPassedCount()
            totalNewHullSize += ship.getHullSize()
            newShipCount += 1
    print "#Number of ships passed over = %d" % newShipCount
    if ( newShipCount ):
        print "#Average new ship hull size =", ( float( totalNewHullSize ) / newShipCount )
    print "#Total ships generated = %d" % generateNewShipList.totalShipsGenerated
    print "#Average hull size generated =", ( float( generateNewShipList.totalHullsGenerated ) / generateNewShipList.totalShipsGenerated )

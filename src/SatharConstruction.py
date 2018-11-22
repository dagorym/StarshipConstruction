#!/usr/bin/python
'''
Created on Nov 22, 2018

@author: Tom Stephens
'''

import random
import math
import sys

from StarshipConstructionCenter import StarshipConstructionCenter
from Starship import Starship


def createSSCList():
    '''
    Created on Nov 22, 2018
    
    @author Tom Stephens
    
    Generate the list of starship construction centers
    '''
    centers = []
    i=0
    #list is name, max hull sizes  All will be type 5
    sccList = {
               "SCC01" : 46,
               "SCC02" : 46,
               "SCC03" : 47,
               "SCC04" : 50,
               "SCC05" : 50,
               "SCC06" : 200,
               "SCC07" : 75,
               "SCC08" : 75,
               "SCC09" : 75,
               "SCC10" : 60,
               }
    for key in sccList:
        centers.append( StarshipConstructionCenter( 5, key ) )
        centers[i].maxTotalHullSizes = sccList[key]
        i += 1
    return centers



if __name__ == '__main__':
    print ("#Running Sathar Starship Construction Simulation.")
    sccs = createSSCList()
    ships = []
    newShips = []
    repairShips = []
    shipDist = {}
    day = 1
    daysToSimulate = 40000

    for scc in sccs:
        print (scc.getName(), scc.getMaxTotalHullSizes())



#    while ( day <= daysToSimulate ):
#        if ( len( newShips ) == 0 ):
#            generateNewShipList( newShips )
#        for ship in list( ships ):
#            needsRepair = ship.update( day )
#            if ( needsRepair ):
#                ships.remove( ship )
#                repairShips.append( ship )
#        for scc in sccs:
#            # update SSC status and get list of any finished ships
#            finshedShips = scc.update( day )
#            # add any new ships to completed ships list
#            for ship in finshedShips:
#                ships.append( ship );
#        #loop over each scc
#        for scc in sccs:
#            #get available hull space
#            ahs = scc.getAvailableSpace()
#            #add first maintenance ship that will fit
#            for ship in list( repairShips ):
#                if ( ahs and ship.getHullSize() <= ahs and ship.getHullSize() <= scc.getMaxHullSize()):
#                    scc.addToQueue( ship )
#                    repairShips.remove( ship )
#                    ahs -= ship.getHullSize()
#                    #break
#        #loop over each unloaded ssc
#        firstShipPos = 0;
#        for scc in sccs:
##            if ( scc.loaded() ): continue  #skip the ones that have had ships added already
#            # make sure we always have at least 100 ships in the queue
#            if ( 300 > len( newShips ) ):
#                generateNewShipList( newShips )
#            #get available hull space
#            ahs = scc.getAvailableSpace()
#            #add first new ship that will fit
#            newCount = 0
#            for ship in list( newShips ):
#                #@todo Need to address prioritizing passed over ships
#                if ( ship.getHullSize() <= ahs and ship.getHullSize() <= scc.getMaxHullSize()):
#                    scc.addToQueue( ship )
#                    shipPos = newShips.index( ship );
#                    if ( shipPos > firstShipPos ): firstShipPos = shipPos #record position of last ship added
#                    newShips.remove( ship )
#                    ahs -= ship.getHullSize()
#                    newCount += 1
#                    if ( newCount > 10 ):
#                        break
#        #increment passed over counter for all ships by passed from queue
#        for i, ship in enumerate( newShips ):
#            ship.incrementPassedCount()
#            if (ship.getPassedCount() > 400):
#                newShips.remove( ship )
#            if ( i > firstShipPos ): break
##         for ship in newShips:
##             if (ship.getPassedCount() > 400):
##                 newShips.remove( ship )

#        #clear loaded flag on SSC
#        for scc in sccs:
#            scc.clearLoaded()

#        # generate yearly statistics
#        totalShips = len( ships ) + len( repairShips )
#        for scc in sccs:
#            totalShips += scc.queueSize()
#        if ( not day % 100 ):
#            print day, totalShips, len( ships ), len( repairShips )
#        day += 1
#    # generate final statistics
#    totalHullSize = 0;
#    for x in range(20):
#        shipDist[x+1] = 0
#    for ship in ships:
#        totalHullSize += ship.getHullSize()
#        shipDist[ship.getHullSize()] += 1
#    for ship in repairShips:
#        totalHullSize += ship.getHullSize()
#        shipDist[ship.getHullSize()] += 1
#    for scc in sccs:
#        for ship in scc.shipsInQueue():
#            totalHullSize += ship.getHullSize()
#            shipDist[ship.getHullSize()] += 1
#    print "#Total ships = %d" % totalShips
#    print "#Average Hull Size =", ( float( totalHullSize ) / totalShips )
#    print "Hull Size Distribution"
#    for x in range(20):
#        print "  ", x+1, ":  ", shipDist[x+1]
#    totalNewHullSize = 0
#    newShipCount = 0
#    for ship in newShips:
#        if ( ship.getPassedCount() > 0 ):
##            print ship.getHullSize(), ship.getPassedCount()
#            totalNewHullSize += ship.getHullSize()
#            newShipCount += 1
#    print "#Number of ships passed over = %d" % newShipCount
#    if ( newShipCount ):
#        print "#Average new ship hull size =", ( float( totalNewHullSize ) / newShipCount )
#    print "#Total ships generated = %d" % generateNewShipList.totalShipsGenerated
#    print "#Average hull size generated =", ( float( generateNewShipList.totalHullsGenerated ) / generateNewShipList.totalShipsGenerated )


#!/usr/bin/python
'''
Created on Nov 22, 2018

@author: Tom Stephens
'''
# For this simulation we will be controlling the types of ships
# created in each of the individual SCCs as well as the start date
# for ship manufacture at each SCC.  We'll also be outputting the
# total number of each type of ship at regular intervals


import random
import math
import sys

from StarshipConstructionCenter import StarshipConstructionCenter
from Starship import Starship
from enum import Enum

class ShipType(Enum):
    F = 1
    C = 4
    FF = 5
    DD = 6
    LC = 14
    AC = 16
    HC = 18

SCCData = {
          "SCC01" : { "HP":46, "start":868, "types":[ShipType.LC,ShipType.DD] },
          "SCC02" : { "HP":46, "start":221, "types":[ShipType.AC,ShipType.DD,ShipType.F], "buildFighters": True },
          "SCC03" : { "HP":47, "start":155, "types":[ShipType.HC,ShipType.DD,ShipType.FF] },
          "SCC04" : { "HP":50, "start":196, "types":[ShipType.AC,ShipType.LC,ShipType.DD,ShipType.F], "buildFighters": True  },
          "SCC05" : { "HP":50, "start":142, "types":[ShipType.LC,ShipType.DD,ShipType.C] },
          "SCC06" : { "HP":200, "start":5000, "types":[ShipType.HC,ShipType.LC,ShipType.AC,ShipType.DD,ShipType.FF,ShipType.C,ShipType.F] },
          "SCC07" : { "HP":75, "start":5000, "types":[ShipType.HC,ShipType.LC,ShipType.AC,ShipType.DD,ShipType.FF,ShipType.C,ShipType.F] },
          "SCC08" : { "HP":75, "start":5000, "types":[ShipType.HC,ShipType.LC,ShipType.AC,ShipType.DD,ShipType.FF,ShipType.C,ShipType.F] },
          "SCC09" : { "HP":75, "start":5000, "types":[ShipType.HC,ShipType.LC,ShipType.AC,ShipType.DD,ShipType.FF,ShipType.C,ShipType.F] },
          "SCC10" : { "HP":60, "start":5000, "types":[ShipType.HC,ShipType.LC,ShipType.AC,ShipType.DD,ShipType.FF,ShipType.F] }
          }

shipCount = {
    ShipType.F: 0,
    ShipType.C: 0,
    ShipType.FF: 0,
    ShipType.DD: 0,
    ShipType.LC: 0,
    ShipType.AC: 0,
    ShipType.HC: 0,
    }

def createSSCList():
    '''
    Created on Nov 22, 2018
    
    @author Tom Stephens
    
    Generate the list of starship construction centers
    '''
    centers = []
    i=0
    for key in SCCData:
        centers.append( StarshipConstructionCenter( 5, key ) )
        centers[i].maxTotalHullSizes = SCCData[key]["HP"]
        centers[i].nextShipSize = SCCData[key]["HP"]
        i += 1
    return centers

def checkBuildFighters(scc,type):
    if (SCCData[scc]["buildFighters"] == True):
        SCCData[scc]["buildFighters"] = False
        return ShipType.F.value
    else:
        SCCData[scc]["buildFighters"] = True
        return type.value


def nextShip(scc,space):
    '''Returns the hull size of the next ship to start based on the SSC's
    production schedule '''
    size = 0
    if ("SSC02" == scc or "SSC04" == scc):
        for ship in SCCData[scc]["types"]:
            if (space >= ship.value):
                if (ShipType.DD):
                    return checkBuildFighters(scc,ShipType.DD)
                return ship.value
    else:
        for ship in SCCData[scc]["types"]:
            if (space >= ship.value):
                return ship.value
    return size


if __name__ == '__main__':
    print ("#Running Sathar Starship Construction Simulation.")
    sccs = createSSCList()


    day = 0
    daysToSimulate = 800

    #for scc in sccs:
    #    print (scc.getName(), scc.getMaxTotalHullSizes())

    ships = []
    while (day < daysToSimulate):
        year = 59 + day//400
        date = 1 + day%400
#        print(year,".",date)
        for scc in sccs:
            if (day >= SCCData[scc.getName()]["start"]): #only update the SCC if past its "start date"
                # first get all the ships that were completed (if any)
                finishedShips = scc.update(day)
                if (len(finishedShips) > 0):
                    for ship in finishedShips:
                        for type in ShipType:
                            if (type.value == ship.getHullSize()):
                                #print(year,".",date,"-",scc.getName(),"produced a",type.name)
                                ships.append(ship)
                                shipCount[type] += 1
                # next add in a new ship if there is room
                ahs = scc.getAvailableSpace()
                while (ahs > 0):
                    size = nextShip(scc.getName(),ahs)
                    if (size > 0):
                        #create new ship of the returned size and add it the scc's queue
                        newShip = Starship( size, 'military', 100 )
                        scc.addToQueue(newShip)
                        ahs -= size
                    else:
                        break
        if ((day+1)%40 == 0):
            string = "FY"+str(year)+"."+str(date).zfill(3)+":"
            for type in ShipType:
                string += "  "+type.name+": "+str(shipCount[type]).zfill(2)
            print (string)

        day += 1





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


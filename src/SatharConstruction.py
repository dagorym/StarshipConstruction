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


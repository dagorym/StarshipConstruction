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

doPrint = True

class ShipType(Enum):
    F = 1
    C = 4
    FF = 5
    DD = 6
    LC = 14
    AC = 16
    HC = 18

SCCData = {
          "SCC01" : { "HP":47, "start":868, "types":[ShipType.LC,ShipType.DD], "nextFighters":-1, "FighterAlternate":None },
          "SCC02" : { "HP":46, "start":221, "types":[ShipType.AC,ShipType.DD,ShipType.F], "nextFighters":430, "FighterAlternate":ShipType.DD },
          "SCC03" : { "HP":59, "start":155, "types":[ShipType.HC,ShipType.DD,ShipType.FF], "nextFighters":-1, "FighterAlternate":None },
          "SCC04" : { "HP":49, "start":196, "types":[ShipType.AC,ShipType.LC,ShipType.FF,ShipType.F], "nextFighters":375, "FighterAlternate":ShipType.FF  },
          "SCC05" : { "HP":50, "start":142, "types":[ShipType.LC,ShipType.DD,ShipType.C], "nextFighters":-1, "FighterAlternate":None },
          "SCC06" : { "HP":200, "start":50000, "types":[ShipType.HC,ShipType.LC,ShipType.AC,ShipType.DD,ShipType.FF,ShipType.C,ShipType.F], "nextFighters":-1, "FighterAlternate":None },
          "SCC07" : { "HP":75, "start":50000, "types":[ShipType.HC,ShipType.LC,ShipType.AC,ShipType.DD,ShipType.FF,ShipType.C,ShipType.F], "nextFighters":-1, "FighterAlternate":None },
          "SCC08" : { "HP":75, "start":50000, "types":[ShipType.HC,ShipType.LC,ShipType.AC,ShipType.DD,ShipType.FF,ShipType.C,ShipType.F], "nextFighters":-1, "FighterAlternate":None },
          "SCC09" : { "HP":75, "start":50000, "types":[ShipType.HC,ShipType.LC,ShipType.AC,ShipType.DD,ShipType.FF,ShipType.C,ShipType.F], "nextFighters":-1, "FighterAlternate":None },
          "SCC10" : { "HP":60, "start":1096, "types":[ShipType.HC,ShipType.LC,ShipType.AC,ShipType.DD,ShipType.FF,ShipType.F], "nextFighters":1104, "FighterAlternate":ShipType.F }
          }

shipCount = {
    ShipType.F: 16,
    ShipType.C: 0,
    ShipType.FF: 2,
    ShipType.DD: 8,
    ShipType.LC: 3,
    ShipType.AC: 3,
    ShipType.HC: 4,
    }

def applyLosses(day,sccs):
    if (411 == day):
        shipCount[ShipType.F] -= 8
        shipCount[ShipType.FF] -= 1
        shipCount[ShipType.DD] -= 4
        shipCount[ShipType.LC] -= 2
        shipCount[ShipType.AC] -= 1
        shipCount[ShipType.HC] -= 1
    elif (455 == day):
        shipCount[ShipType.DD] -= 2
        shipCount[ShipType.LC] -= 1
    elif (610 == day):
        shipCount[ShipType.DD] -= 1
        shipCount[ShipType.FF] -= 1
    elif (838 == day):
        shipCount[ShipType.FF] -= 1
        shipCount[ShipType.DD] -= 2
        shipCount[ShipType.LC] -= 1
    elif (892 == day):
        shipCount[ShipType.C] -= 1
    elif (1013 == day):
        shipCount[ShipType.F] -= 4
    elif (1035 == day):
        sccs[1].markDestroyed()
        shipCount[ShipType.DD] -= 1
        shipCount[ShipType.F] -= 13
    elif (1096 == day):  # SCC#10 activates and ships from Saurian campaign added to inventory
        shipCount[ShipType.F] += 9
        shipCount[ShipType.FF] += 3
        shipCount[ShipType.DD] += 5
        shipCount[ShipType.LC] += 3
        shipCount[ShipType.AC] += 2
        shipCount[ShipType.HC] += 2
    else:
        pass
def initializeSCCs(centers):
    '''Set up the initial state of the various SCCs based on their
    production schedule'''
    y=1000 #we're not worrying about maintenance in this sim

    #SCC 1
    lc = Starship(14,'military',y)
    lc.daysLeft = 140
    centers[0].addToQueue(lc)
    lc = Starship(14,'military',y)
    lc.daysLeft = 280
    centers[0].addToQueue(lc)
    centers[0].addToQueue(Starship(14,'military',y))
    centers[0].addToQueue(Starship(5,'military',y))

    #SCC 2
    ac = Starship(16,'military',y)
    centers[1].addToQueue(ac)
    dd = Starship(6,'military',y)
    dd.daysLeft = 45
    centers[1].addToQueue(dd)
    dd = Starship(6,'military',y)
    dd.daysLeft = 90
    centers[1].addToQueue(dd)
    dd = Starship(6,'military',y)
    dd.daysLeft = 135
    centers[1].addToQueue(dd)
    dd = Starship(6,'military',y)
    centers[1].addToQueue(dd)
    centers[1].addToQueue(Starship(1,'military',y))
    centers[1].addToQueue(Starship(1,'military',y))
    centers[1].addToQueue(Starship(1,'military',y))
    centers[1].addToQueue(Starship(1,'military',y))
    centers[1].addToQueue(Starship(1,'military',y))
    centers[1].addToQueue(Starship(1,'military',y))

    #SCC 3
    hc = Starship(18,'military',y)
    hc.daysLeft = 180
    centers[2].addToQueue(hc)
    hc = Starship(18,'military',y)
    hc.daysLeft = 360
    centers[2].addToQueue(hc)
    centers[2].addToQueue(Starship(18,'military',y))
    centers[2].addToQueue(Starship(5,'military',y))

    #SCC 4
    centers[3].addToQueue(Starship(16,'military',y))
    lc = Starship(14,'military',y)
    lc.daysLeft = 210
    centers[3].addToQueue(lc)
    centers[3].addToQueue(Starship(14,'military',y))
    centers[3].addToQueue(Starship(1,'military',y))
    centers[3].addToQueue(Starship(1,'military',y))
    centers[3].addToQueue(Starship(1,'military',y))
    centers[3].addToQueue(Starship(1,'military',y))
    centers[3].addToQueue(Starship(1,'military',y))

    #SCC 5
    lc = Starship(14,'military',y)
    lc.daysLeft = 210
    centers[4].addToQueue(lc)
    centers[4].addToQueue(Starship(14,'military',y))
    centers[4].addToQueue(Starship(18,'military',y))
    centers[4].addToQueue(Starship(4,'military',y))

    #SCC 10
    f = Starship(1,'military',y)
    f.daysLeft = 8
    centers[9].addToQueue(f)
    ff = Starship(5,'military',y)
    ff.daysLeft = 128
    centers[9].addToQueue(ff)
    dd = Starship(6,'military',y)
    dd.daysLeft = 158
    centers[9].addToQueue(dd)
    lc = Starship(14,'military',y)
    lc.daysLeft = 338
    centers[9].addToQueue(lc)
    ac = Starship(16,'military',y)
    ac.daysLeft = 38
    centers[9].addToQueue(ac)
    hc = Starship(18,'military',y)
    hc.daysLeft = 158
    centers[9].addToQueue(hc)



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
    initializeSCCs(centers)
    return centers


def buildFighters(scc,day):
    if (SCCData[scc]["nextFighters"] == day):
        SCCData[scc]["nextFighters"] += 30 + SCCData[scc]["FighterAlternate"].value*30
        return True
    else:
        return False

if __name__ == '__main__':
    print ("#Running Sathar Starship Construction Simulation.")
    sccs = createSSCList()


    day = 0
    daysToSimulate = 4*400

    #for scc in sccs:
    #    print (scc.getName(), scc.getMaxTotalHullSizes())

    ships = []
    while (day < daysToSimulate):
        year = 59 + day//400
        date = 1 + day%400
        applyLosses(day,sccs)
#        print(year,".",date)
        for scc in sccs:
            if (scc.isDestroyed()): 
#                print ("Skipping SCC", scc.getName())
                pass
            elif (day >= SCCData[scc.getName()]["start"]): #only update the SCC if past its "start date"
                # first get all the ships that were completed (if any)
                finishedShips = scc.update(day)
                if (len(finishedShips) > 0):
                    for ship in finishedShips:
                        for type in ShipType:
                            if (type.value == ship.getHullSize()):
                                # record the ship
                                if (day >= 400):
                                    if (doPrint): print(str(year)+"."+str(date),"-",scc.getName(),"produced a",type.name)
                                    ships.append(ship)
                                    shipCount[type] += 1
                                # start a new ship of the same type
                                # unless its a SCC that flips types
                                if (scc.getAvailableSpace()>0):
                                    if (type == SCCData[scc.getName()]["FighterAlternate"]): # we might have to build fighters
                                        if (buildFighters(scc.getName(),day)): # yep, build fighters
                                            for x in range(0,type.value):
#                                                if (doPrint): print (str(year)+"."+str(date),"-",scc.getName(),"added a ship of size 1")
                                                scc.addToQueue(Starship(1,'military',100))
                                        else:  #otherwise build another of the same type
#                                            if (doPrint): print (str(year)+"."+str(date),"-",scc.getName(),"added a ship of size",type.value)
                                            scc.addToQueue(Starship(type.value,'military',100))
                                    elif (type == ShipType.F):  # we just finished fighters and might need to build the alternate
                                        if (buildFighters(scc.getName(),day)): # no, still build fighters
                                            for x in range(0,type.value):
#                                                if (doPrint): print (str(year)+"."+str(date),"-",scc.getName(),"added a ship of size 1")
                                                scc.addToQueue(Starship(1,'military',100))
                                        else:  # otherwise build one of the alternates
                                            size = SCCData[scc.getName()]["FighterAlternate"].value
#                                            if (doPrint): print (str(year)+"."+str(date),"-",scc.getName(),"added a ship of size",size)
                                            scc.addToQueue(Starship(size,'military',100))
                                    else:  # otherwise, just build another of the same type
#                                        if (doPrint): print (str(year)+"."+str(date),"-",scc.getName(),"added a ship of size",type.value)
                                        scc.addToQueue(Starship(type.value,'military',100))

        if ((day+1)%40 == 0):
            string = "FY"+str(year)+"."+str(date).zfill(3)+":"
            for type in ShipType:
                string += "  "+type.name+": "+str(shipCount[type]).zfill(2)
            print (string)

        day += 1


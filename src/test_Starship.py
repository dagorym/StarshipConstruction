'''
Created on Aug 20, 2013

@author: tstephen
'''
import unittest
from Starship import Starship

class Test( unittest.TestCase ):


    def testCreateCivlian( self ):
        ship = Starship( 5, 'civilian', 1 )
        self.assertEqual( ship.getType(), 'civilian', "Incorrect ship type" )
        self.assertEqual( ship.getHullSize(), 5, "Incorrect hull size" )
        self.assertEqual( ship.getDaysRemaining(), 150, "Incorrect days remaining" )
        self.assertEqual( ship.isNew(), True, "New ship flag not set to proper default" )
        self.assertEqual( ship.getPassedCount(), 0, "passed count not set to proper default" )
    def testCreateMilitary( self ):
        ship = Starship( 12, 'military', 1 )
        self.assertEqual( ship.getType(), 'military', "Incorrect ship type" )
        self.assertEqual( ship.getHullSize(), 12, "Incorrect hull size" )
        self.assertEqual( ship.getDaysRemaining(), 360, "Incorrect days remaining" )
    def testBadType( self ):
        self.assertRaises( ValueError, Starship, 12, 'system' , 1 )
    def testBadHullSizeLow( self ):
        self.assertRaises( ValueError, Starship, 0, 'military' , 1 )
    def testBadHullSizeHigh( self ):
        self.assertRaises( ValueError, Starship, 21, 'military' , 1 )
    def testGenericCreation( self ):
        ship = Starship( 5, 'civilian', 1 )
        self.assertEqual( ship.getTimeToNextMaintenance(), 0, 'Incorrect maintenance time' )
    def testCreationDate( self ):
        ship = Starship( 5, 'civilian', 3 )
        ship.setCreationDate( 23 )
        self.assertEqual( ship.getTimeToNextMaintenance(), 1223, "Incorrect maintenance date" )
    def testSetRepairCompleted( self ):
        ship = Starship( 5, 'civilian', 2 )
        ship.setRepairsCompleted( 42 )
        self.assertEqual( ship.getTimeToNextMaintenance(), 842, "Incorrect maintenance date" )
    def testStartMaintenance( self ):
        ship = Starship( 10, 'civilian', 1 )
        ship.startMaintenance( 1 )
        self.assertTrue( ship.getDaysRemaining() in range ( 11, 21 ), 'Incorrect maintenance time remaining' )
        ship.startMaintenance( 2 )
        self.assertTrue( ship.getDaysRemaining() in range ( 12, 31 ), 'Incorrect maintenance time remaining' )
        ship.startMaintenance( 3 )
        self.assertTrue( ship.getDaysRemaining() in range ( 13, 41 ), 'Incorrect maintenance time remaining' )
        ship.startMaintenance( 4 )
        self.assertTrue( ship.getDaysRemaining() in range ( 14, 51 ), 'Incorrect maintenance time remaining' )
        ship.startMaintenance( 5 )
        self.assertTrue( ship.getDaysRemaining() in range ( 15, 61 ), 'Incorrect maintenance time remaining' )
        ship.startMaintenance( 6 )
        self.assertTrue( ship.getDaysRemaining() in range ( 16, 71 ), 'Incorrect maintenance time remaining' )
    def testIncrementPassCount( self ):
        ship = Starship( 10, 'civilian', 1 )
        ship.incrementPassedCount()
        ship.incrementPassedCount()
        self.assertEqual( ship.getPassedCount(), 2, "Passed count not properly incremented" )
    def testUpdateConstructionNotComplete( self ):
        ship = Starship( 10, 'civilian', 1 )
        self.assertFalse( ship.update( 10 ), "Ship claimed to be done when time was remaining" )
    def testUpdateConstructionComplete( self ):
        ship = Starship( 10, 'civilian', 1 )
        ship.daysLeft = 1
        self.assertTrue( ship.update( 10 ), "Ship did not properly leave construction" )
        self.assertEqual( ship.getTimeToNextMaintenance(), 410, "Next maintenance date not properly updated" )
    def testUpdateTimeForMaintenance( self ):
        ship = Starship( 10, 'civilian', 1 )
        ship.daysLeft = 1
        ship.update( 10 )
        self.assertFalse( ship.update( 11 ), "Ship claimed to need maintenance when it didn't really" )
    def testNoMaintenanceNeeded( self ):
        ship = Starship( 10, 'civilian', 1 )
        ship.daysLeft = 1
        ship.update( 10 )
        self.assertTrue( ship.update( 410 ), "Ship did not properly report maintenance needed" )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateCivlian']
    unittest.main()

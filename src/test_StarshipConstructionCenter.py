'''
Created on Aug 20, 2013

@author: tstephen
'''
import unittest
from StarshipConstructionCenter import StarshipConstructionCenter

class Test( unittest.TestCase ):

    def test_CreateDefaults( self ):
        ssc = StarshipConstructionCenter( 1 )
        self.assertEqual( ssc.getCurrentHullSizeTotal(), 0, "Incorrect total current hull sizes" )
        self.assertEqual( ssc.getNextShipSize(), 140, "Incorrect next ship size" )
        self.assertEqual( ssc.getName(), 'Type 1 Construction Center' )
        self.assertEqual( ssc.loaded(), False )

    def test_CreateType1( self ):
        ssc = StarshipConstructionCenter( 1 )
        self.assertEqual( ssc.getMaxHullSize(), 20 )
        self.assertEqual( ssc.getMaxMilitaryHullSize(), 20 )
        self.assertEqual( ssc.getMaxTotalHullSizes(), 140 )
        self.assertEqual( ssc.getHullProbability(), 1.0 )
        self.assertEqual( ssc.getOnlySystemShips(), False )

    def test_CreateType2( self ):
        ssc = StarshipConstructionCenter( 2 )
        self.assertEqual( ssc.getMaxHullSize(), 14 )
        self.assertEqual( ssc.getMaxMilitaryHullSize(), 6 )
        self.assertEqual( ssc.getMaxTotalHullSizes(), 50 )
        self.assertEqual( ssc.getHullProbability(), 0.75 )
        self.assertEqual( ssc.getOnlySystemShips(), False )

    def test_CreateType3( self ):
        ssc = StarshipConstructionCenter( 3 )
        self.assertEqual( ssc.getMaxHullSize(), 20 )
        self.assertEqual( ssc.getMaxMilitaryHullSize(), 0 )
        self.assertEqual( ssc.getMaxTotalHullSizes(), 20 )
        self.assertEqual( ssc.getHullProbability(), 0.35 )
        self.assertEqual( ssc.getOnlySystemShips(), True )

    def test_CreateType4( self ):
        ssc = StarshipConstructionCenter( 4 )
        self.assertEqual( ssc.getMaxHullSize(), 5 )
        self.assertEqual( ssc.getMaxMilitaryHullSize(), 3 )
        self.assertEqual( ssc.getMaxTotalHullSizes(), 10 )
        self.assertEqual( ssc.getHullProbability(), 1.0 )
        self.assertEqual( ssc.getOnlySystemShips(), True )

    def test_CreateBadTypeLow( self ):
        self.assertRaises( Exception, StarshipConstructionCenter, 0 )

    def test_CreateBadTypeHigh( self ):
        self.assertRaises( Exception, StarshipConstructionCenter, 5 )

    def test_GetName( self ):
        ssc = StarshipConstructionCenter( 1, "Triad SSC" )
        self.assertEqual( ssc.getName(), "Triad SSC", "Did not return passed in name" )

    def test_ClearLoaded( self ):
        ssc = StarshipConstructionCenter( 1, "Triad SSC" )
        ssc.isLoaded = True
        self.assertEqual( ssc.loaded(), True, "isLoaded variable not set properly" )
        ssc.clearLoaded()
        self.assertEqual( ssc.loaded(), False, "isLoaded variable not cleared properly" )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_CreateType1']
    unittest.main()

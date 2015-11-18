import colorsys

from ..helper import hex3
from ..helper import tupleTools as tup

class Color:
    def __init__(self, R, G, B):
        self.value = (R,G,B)
        
    def getHex(self):
        return hex3.toHex(*self.value)
        
    def getRGB(self):
        return tup.tuplePad( self.value )
        
    def getHSV(self):
        hsvTuple = tup.hsvToInteger( colorsys.rgb_to_hsv ( *tup.rgbToDecimal( self.value ) ) )
        hsvString = tup.tuplePad( hsvTuple )
        return hsvString
        
    def __str__(self):
        return self.getHex()
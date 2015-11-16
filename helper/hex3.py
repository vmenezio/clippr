#! python3
# -*- coding: utf-8 -*-

# Small utility to help convert RGB tuples into #
# hex triplets and vice-versa.                  #
#                                               #
#   - Vinícius Menézio                          #

def toHex( r, g, b ):
    hexR = hex(r)[2:].zfill(2)
    hexG = hex(g)[2:].zfill(2)
    hexB = hex(b)[2:].zfill(2)
    hexValue = "0x" + hexR + hexG +hexB
    return hexValue

def toHexHash( r, g, b ):
    hexValue = "#" + toHex( r, g, b )[2:]
    return hexValue
    
def toRGB( hex ):
    i = 1 if hex[0] == "#" else 2 if hex[0:2] == "0x" else 0
    r = int( hex[i:i+2], 16 )
    g = int( hex[i+2:i+4], 16 )
    b = int( hex[i+4:i+6], 16 )
    return ( r, g, b )

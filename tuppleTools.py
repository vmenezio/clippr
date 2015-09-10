# Collection of tupple operations to help dealing	#
# with colorsys weirdnesses while keeping main.py	#
# as clean as possible.								#
#													#
#	- Vinícius Menézio								#

def tuplePad( tup, pad=3 ):
	l = [str(a).rjust(pad) for a in tup]
	s = ", ".join(l)
	return "( "+s+" )"
	
def rgbToDecimal( rgb ):
	return tuple( [ c/255 for c in rgb ] )
	
def hsvToInteger( hsv ):
	return ( round(hsv[0]*360), round(hsv[1]*100), round(hsv[2]*100) )

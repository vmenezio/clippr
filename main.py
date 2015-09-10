#					[ clipper ]						#
#													#
# Hey, welcome to clipper! This is a small tool I	#
# have been building for personal use as a means	#
# to take, analyze and upload screenshots quickly.	#
#													#
# I'm not sure how common this specific task is for #
# anyone else, but since, personally, it'd be a 	#
# huge time saver to have the proccess automated	#
# and bound to a shortcut, I'm making the source	#
# available to whomever else happens to find this 	#
# useful as well. Enjoy!							#
#													#
#	- Vinícius Menézio								#

import hex3
import colorsys
import imgurUploader as imgur
import tuppleTools as tup
from PIL import ImageGrab

# trying to grab a bitmap from the clipboard, exits if it fails
im = ImageGrab.grabclipboard()
if ( im is None ):
	print("\nno image found in the clipboard!")
	exit()
	
# retrieving basic data about the image and saving a temporary local copy
totalPixels = im.width*im.height;
colorList = sorted(im.getcolors(), reverse=True)
im.save("out/temp.png")

# starting a session with imgur's API and uploading the image anonimously
client = imgur.startClient()
img_ur = imgur.uploadImage( client, "out/temp.png" )

# printing relevant image info
print("\ndimensions: "+str(im.width)+" x "+str(im.height)+" px")
print("filesize: "+str(img_ur["filesize"]/1000)+" KB | colors: "+str(len(colorList))+"\n")

print("url: "+str(img_ur["url"])+"\n")
	
print("  USAGE  |   HEX    |        RGB        |        HSV")
print("---------+----------+-------------------+-------------------")
for color in colorList:
	coloredPixels = color[0]
	usage = 100 * coloredPixels/totalPixels
	if ( usage <= 0.05 ):
		usageStr = " < 0.1 %"
	else:
		usageStr = (str( round( usage, 1 ) )+" %").rjust(8)
	rgbTuple = color[1]
	rgbStr = tup.tuplePad( rgbTuple )
	hsvTuple = tup.hsvToInteger( colorsys.rgb_to_hsv ( *tup.rgbToDecimal( rgbTuple ) ) )
	hsvStr = tup.tuplePad( hsvTuple )
	hexValue = hex3.toHex( *color[1] )
	print( usageStr +" | " + hexValue + " | " + rgbStr + " | " + hsvStr )

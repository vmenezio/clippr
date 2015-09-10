#					 [ clipper ]					#
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

import sys
import os
import hex3
import colorsys
import requests
import imgurpython
import imgurUploader as imgur
import tuppleTools as tup
from PIL import ImageGrab

# trying to grab a bitmap from the clipboard, exits if it fails
im = ImageGrab.grabclipboard()
if ( im is None ):
	print("\nNo image found in the clipboard!")
	exit()
	
# retrieving basic data about the image and saving a temporary local copy
totalPixels = im.width*im.height;
colorList = sorted(im.getcolors(), reverse=True)
im.save("out/temp.png")
imageLocalFilesize = str(os.path.getsize("out/temp.png")/1000)+" KB"

# setting default values for online image data, in case the upload fails
imageURL = "[upload failed]"
imageOnlineFilesize = "N/A"

# starting a session with imgur's API and uploading the image anonimously
try:
	client = imgur.startClient()
	try:
		img_ur = imgur.uploadImage( client, "out/temp.png" )
		imageURL = img_ur["url"]
		imageOnlineFilesize = str(img_ur["filesize"]/1000)+" KB"
	except FileNotFoundError as e:
		print("\nCan't find image to upload. Please check whther file out/temp.png has been deleted.")
	except requests.exceptions.ConnectionError as e:
		print("\nCan't upload file to server. Please check your connection.")
	except imgurpython.helpers.error.ImgurClientError as e:
		print("\nCan't validade client's key/secret combination. Please check your credentials.")
	except Exception as e:
		print("\nUnexpected error while uploading:", sys.exc_info()[0])
		print(e)
		exit()
except requests.exceptions.ConnectionError as e:
	print("\nCan't communicate with server. Please check your connection.")
except Exception as e:
	print("\nUnexpected error while connecting:", sys.exc_info()[0])
	print(e)


# printing relevant image info
print("\ndimensions: "+str(im.width)+" x "+str(im.height)+" px | colors: "+str(len(colorList)))
print("filesize: LOCAL "+imageLocalFilesize+", ONLINE "+imageOnlineFilesize+"\n" )

print("url: "+imageURL+"\n")
	
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

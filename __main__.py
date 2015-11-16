#! python3
# -*- coding: utf-8 -*-

#                    [ clipper ]                    #
#                                                   #
# Hey, welcome to clipper! This is a small tool I   #
# have been building for personal use as a means    #
# to take, analyze and upload screenshots quickly.  #
#                                                   #
# I'm not sure how common this specific task is for #
# anyone else, but since, personally, it'd be a     #
# huge time saver to have the proccess automated    #
# and bound to a shortcut, I'm making the source    #
# available to whomever else happens to find this   #
# useful as well. Enjoy!                            #
#                                                   #
#   - Vinícius Menézio                              #

import sys
import os

from .helper import hex3
from .helper import imgurUploader as imgur
from .helper import tuppleTools as tup

import colorsys
from PIL import ImageGrab

from requests.exceptions import ConnectionError
from imgurpython.helpers.error import ImgurClientError

def main():
    try:
        image = clip()
    except FileNotFoundError:
        print("\nNo image found in the clipboard!")
        exit()
        
    localData = analyze(image)
    onlineData = upload(localData["path"])
    printOutput( localData, onlineData )
        
# Print user friendly output
def printOutput( local, online ):
    print("dimensions:",local["width"],"x",local["height"],"px | colors:",local["colorCount"])
    print("filesize: LOCAL",local["filesize"]/1000,"KB, ONLINE",online["filesize"]/1000,"KB\n")
    
    print("url: "+online["url"]+"\n")
    
    if (local["colorList"] is None):
        print("Color count limit ("+local["paletteSize"]+") exceeded. Could not retrieve palette data.")
    else:
        print("  USAGE  |   HEX    |        RGB        |        HSV")
        print("---------+----------+-------------------+-------------------")
        for color in sorted(local["colorList"], reverse=True):
            coloredPixels = color[0]
            usage = 100 * coloredPixels/local["totalPixels"]
            if ( usage <= 0.05 ):
                usageStr = " < 0.1 %"
            else:
                usageStr = (str( round( usage, 1 ) )+" %").rjust(8)
            rgbTuple = color[1]
            rgbStr = tup.tuplePad( rgbTuple )
            hsvTuple = tup.hsvToInteger( colorsys.rgb_to_hsv ( *tup.rgbToDecimal( rgbTuple ) ) )
            hsvStr = tup.tuplePad( hsvTuple )
            hexValue = hex3.toHex( *color[1] )
            print( usageStr,"|",hexValue,"|",rgbStr,"|",hsvStr )

            
# Grab bitmap from the clipboard
def clip():
    try:
        img = ImageGrab.grabclipboard()
    except OSError:
        print("\nUnsupported clipboard image!")
        exit()
    
    if ( img is None ):
        raise FileNotFoundError
    else:
        return img
        
# Locally analyze image data
def analyze( img, paletteSize=32 ):
    data = {}
    # Getting real ugly real fast. Use a class. Make totalPixels a property
    data["width"] = img.width
    data["height"] = img.height
    data["totalPixels"] = img.width * img.height
    data["paletteSize"] = paletteSize
    data["colorList"] = img.getcolors(paletteSize)
    
    try:
        data["colorCount"] = len(data["colorList"])
    except TypeError:
        data["colorCount"] = "N/A"
        
    data["path"] = os.path.dirname(sys.argv[0])+"/out/temp.png"
    img.save(data["path"])
    data["filesize"] = os.path.getsize(data["path"])
    
    return data
        
# Upload image to Imgur
def upload( imgPath ):
    data = { "url":"[upload failed]", "filesize":"N/A" }
    try:
    
        client = imgur.startClient()
        try:
            img_ur = imgur.uploadImage( client, imgPath )
            data.update(img_ur)
        except FileNotFoundError:
            print("Can't find image to upload. Please check whther file out/temp.png has been deleted.")
        except ConnectionError:
            print("Can't upload file to server. Please check your internet connection.")
        except ImgurClientError:
            print("Can't validade client's ID. Please check your credentials.")
        except Exception as e:
            print("Unexpected error while uploading:", sys.exc_info()[0])
            print(e)
            exit()
            
    except requests.exceptions.ConnectionError as e:
        print("Can't communicate with server. Please check your connection.")
    except Exception as e:
        print("Unexpected error while connecting:", sys.exc_info()[0])
        print(e)
        
    return data
        
if __name__ == "__main__":
    main()

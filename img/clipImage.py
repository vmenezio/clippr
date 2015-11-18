from .palette import Palette, PaletteEmptyException

import sys
from os.path import getsize, dirname

from ..helper import imgurUploader as imgur

from PIL import ImageGrab
from prettytable import PrettyTable

from requests.exceptions import ConnectionError
from imgurpython.helpers.error import ImgurClientError

class ClipImage():
    def __init__(self, autoUpload=True):
        self.onlineSize = "N/A"
        self.url = "[upload failed]"
        self.clip()
        self.analyze()
        if ( autoUpload ):
            self.upload()
            
    @property
    def width(self):
        return self.pilImg.width
        
    @property
    def height(self):
        return self.pilImg.height
            
    @property
    def totalPixels(self):
        return self.width * self.height
        
    def clip(self):
        self.pilImg = ImageGrab.grabclipboard() # CHECK FOR OSError
        
        if ( self.pilImg is None ):
            raise FileNotFoundError("No image was found in the clipboard!")
            
    def analyze( self, paletteSize=32 ):
        
        try:
            self.palette = Palette( self.pilImg.getcolors(paletteSize) )
        except PaletteEmptyException:
            self.palette = []
        
        self.path, self.size = self.save()
        
    def save( self, path="/../out/temp.png" ):
        fullPath = dirname(__file__) + path
        
        self.pilImg.save( fullPath )
        size = getsize( fullPath )
        
        return fullPath, size
        
    def upload(self, path="/../out/temp.png" ): # still messy. Move this code into imgurUploader?
        try:
            client = imgur.startClient()
            try:
                img_ur = imgur.uploadImage( client, dirname(__file__) + path )
                self.url = img_ur["url"]
                self.onlineSize = img_ur["filesize"]
                self.deleteHash = img_ur["deleteHash"]
            except FileNotFoundError:   # substitute these prints with raises?
                print("Can't find image to upload. Please check whther file out/temp.png has been deleted.")
            except ConnectionError:
                print("Can't upload file to server. Please check your internet connection.")
            except ImgurClientError:
                print("Can't validade client's ID. Please check your credentials.")
            except Exception as e:
                print("Unexpected error while uploading:", sys.exc_info()[0])
                print(e)
                exit()
        except ConnectionError as e:
            print("Can't communicate with server. Please check your connection.")
        except Exception as e:
            print("Unexpected error while connecting:", sys.exc_info()[0])
            print(e)
        
    def getColorTable(self):
        table = PrettyTable(["USAGE", "HEX", "RGB", "HSV"])
        if not self.palette:
            return "Color count limit exceeded. Palette data could not be retrieved."
        for color in self.palette:
            colorUsage = round( 100 * self.palette.colorPixels[color] / self.totalPixels, 1 )
            usageString = "< 0.1 %" if colorUsage < 0.05 else ( str( colorUsage ) + " %" ).rjust(7)
            table.add_row([usageString, color, color.getRGB(), color.getHSV()])
        return table
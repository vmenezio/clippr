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

from .img.clipImage import ClipImage

from requests.exceptions import ConnectionError
from imgurpython.helpers.error import ImgurClientError

def main():
    clippy = ClipImage()
    
    print( "dimensions:", clippy.width, "x", clippy.height, "px | colors:", len(clippy.palette) )
    print("filesize: LOCAL", clippy.size/1000, "KB, ONLINE", clippy.onlineSize/1000,"KB\n") # BREAKS IF IT CAN'T UPLOAD / RETRIEVE FILESIZE
    
    print("url:",clippy.url,"\n")
    
    print(clippy.getColorTable())
        
if __name__ == "__main__":
    main()

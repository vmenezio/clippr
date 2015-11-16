#! python3
# -*- coding: utf-8 -*-

# Some functions to make integration with imgur's   #
# API nice and easy. Nothing too fancy.             #
#                                                   #
#   - Vinícius Menézio                              #

from imgurpython import ImgurClient

def startClient():
    return ImgurClient("63ee41f27565802", None)
    
def uploadImage( client, imagePath ):
    imageMeta = client.upload_from_path( imagePath )
    return { "url" : imageMeta["link"] , "deleteHash": imageMeta["deletehash"] , "filesize" : imageMeta["size"] }

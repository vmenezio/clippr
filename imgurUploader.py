#! python3
# -*- coding: utf-8 -*-

# Some functions to make integration with imgur's   #
# API nice and easy. Nothing too fancy.             #
#                                                   #
#   - Vinícius Menézio                              #

from imgurpython import ImgurClient

def startClient():
    with open("acc.txt") as acc:
        id, secret = acc.read().splitlines()

    return ImgurClient(id, secret)
    
def uploadImage( client, imagePath ):
    imageMeta = client.upload_from_path( imagePath )
    return { "url" : imageMeta["link"] , "deleteHash": imageMeta["deletehash"] , "filesize" : imageMeta["size"] }

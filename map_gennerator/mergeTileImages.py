#!/usr/bin/env python

from PIL import Image

def mergeTileImages(imageSizeX, imageSizeY, minX, maxX, minY, maxY, z, tileImageDir, mergeImagePath):
    img = Image.new("RGBA", (imageSizeX, imageSizeY), (0, 0, 0, 0))
    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            tileImage = Image.open(tileImageDir + str(z) + '_' + str(x) + '_' + str(y) + '.jpg')
            img.paste(tileImage, ((x - minX) * 256, (y - minY) * 256))
    img.save(mergeImagePath)

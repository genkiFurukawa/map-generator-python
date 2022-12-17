#!/usr/bin/env python

from datetime import datetime
from PIL import Image

def mergeTileImages(imageSizeX, imageSizeY, minX, maxX, minY, maxY, z, tileImageDir, mergeImagePath):
    img = Image.new("RGBA", (imageSizeX, imageSizeY), (0, 0, 0, 0))
    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            try:
                tileImagePath = tileImageDir + str(z) + '_' + str(x) + '_' + str(y) + '.jpg'
                tileImage = Image.open(tileImagePath)
                img.paste(tileImage, ((x - minX) * 256, (y - minY) * 256))
            except: # FIXME: 一旦例外全てで同じ処理
                print(str(datetime.now()) + ' [warn] タイル画像( ' + tileImagePath + ' )をopenできなかったため処理をスキップ')
                pass    
    img.save(mergeImagePath)

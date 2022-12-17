#!/usr/bin/env python

from datetime import datetime
from PIL import Image

def generateGridImages(inputFilePath, outputDir, minX, maxX, minY, maxY, gridSizeX, gridSizeY):
    img = Image.open(inputFilePath)

    blockSizeX = (maxX - minX + 1) // gridSizeX
    blockSizeY = (maxY - minY + 1) // gridSizeY

    number = 1
    # NOTE: 左上から右下の順で番号を付与していきたいのでyからループを回す 
    for y in range(blockSizeY):
        for x in range(blockSizeX):
            # 画像を切り出す範囲を計算する
            startX = (255 * gridSizeX) * x + gridSizeX * x
            endX = startX + (255 * gridSizeX)
            startY = (255 * gridSizeY) * y + gridSizeY * y
            endY = startY + (255 * gridSizeY)

            # 30pxの幅の余裕を持たせて画像を切り出す
            cropImg = img.crop((startX - 30, startY - 30 , endX + 30 , endY + 30))

            # 保存する
            cropImg.save(outputDir + str(number) + '.png')

            number += 1

            # 途中経過を出力する
            if number % 10 == 0:
                print(str(datetime.now()) + '   ファイル分割 ' + str(blockSizeY * blockSizeX) + '件中 ' + str(number) + '件完了')

    print(str(datetime.now()) + '   ファイル分割 ' + str(blockSizeY * blockSizeX) + '件中 ' + str(number - 1) + '件完了')

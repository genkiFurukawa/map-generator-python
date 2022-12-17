#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont

def drawDividingLines(inputFilePath, outputFilePath, minX, maxX, minY, maxY, gridSizeX, gridSizeY, fill = (0, 0, 0), width = 5, showNumber = True):
    img = Image.open(inputFilePath)
    blockSizeX = (maxX - minX + 1) // gridSizeX
    blockSizeY = (maxY - minY + 1) // gridSizeY

    draw = ImageDraw.Draw(img)
    number = 1
    font = ImageFont.truetype('Arial.ttf', 50)
    # NOTE: 左上から右下の順で番号を付与していきたいのでyからループを回す 
    for y in range(blockSizeY):
        for x in range(blockSizeX):
            # 線を引く
            startX = (255 * gridSizeX) * x + gridSizeX * x
            endX = startX + (255 * gridSizeX)
            startY = (255 * gridSizeY) * y + gridSizeY * y
            endY = startY + (255 * gridSizeY)
            draw.line(((startX, startY), (endX, startY), (endX, endY), (startX, endY)), fill = fill, width= width)
            # 番号を付与する
            if showNumber:
                centerX = (startX + endX) // 2 - 30
                centerY = (startY + endY) // 2 - 30
                draw.text((centerX, centerY), str(number), '#000000', font=font)
            number += 1

    img.save(outputFilePath)

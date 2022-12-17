#!/usr/bin/env python

import json
from map_gennerator.utils import calcPixcelCoordinate
from PIL import Image, ImageDraw, ImageFont

def drawPolygons(jsonpath, imagePath, outputPath, minX, maxX, minY, maxY, z):
    img = Image.open(imagePath)
    draw = ImageDraw.Draw(img)

    blockSizeX = maxX - minX + 1
    blockSizeY = maxY - minY + 1

    fontSize = 10
    font = ImageFont.truetype('Arial.ttf', fontSize)
    polygons = json.load(open(jsonpath, 'r'))['features']
    for polygon in polygons:
        coordinates = polygon['geometry']['coordinates'][0]
        # NOTE: タイル画像の中に含まれるかどうかチェック
        isContain = False
        for coordinate in coordinates:
            pixcelX, pixcelY, _ = calcPixcelCoordinate(coordinate[1], coordinate[0], z)
            x = pixcelX - 256 * minX
            y = pixcelY - 256 * minY
            
            if x > 0 and y > 0 and x < (256 * blockSizeX) and y < (256 * blockSizeY):
                isContain = True
                break

        # NOTE: 含まれる場合はポリゴンを描画
        if isContain:
            points = []
            sumX = 0
            sumY = 0
            for coordinate in coordinates:
                pixcelX, pixcelY, _ = calcPixcelCoordinate(coordinate[1], coordinate[0], z)
                x = pixcelX - 256 * minX
                y = pixcelY - 256 * minY
                                
                if x < 0:
                    x = 0
                
                if y < 0:
                    y = 0
                
                points.append(x)
                points.append(y)

                sumX += x
                sumY += y

            # NOTE: https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
            draw.polygon(points, outline = (0, 0, 0), fill = None, width=3)

            # NOTE: いい感じのところに地番名を出す
            centerX = sumX / len(coordinates) - (fontSize // 2)
            centerY = sumY / len(coordinates) - (fontSize // 2)
            draw.text((centerX, centerY), '1111', '#000000', font = font)
    
    img.save(outputPath)

#!/usr/bin/env python

from map_gennerator.utils import calcPixcelCoordinate, calcTileCoordinate, calcIntraTileCoordinate
from map_gennerator.drawPolygons import drawPolygons
from PIL import ImageFont, Image, ImageDraw
import requests

def main():
    top, bottom = 35.75621375767344, 35.740511743214284
    left, right = 140.2267393761772, 140.24713616224628
    z = 18
    
    print('>> 国土地理院のタイル画像から地図を生成 start')
    # 1. タイルの番号を計算(TSで実装)
    print('>> タイル座標を計算 start')
    minX, minY, _ = calcTileCoordinate(top, left, z)
    maxX, maxY, _ = calcTileCoordinate(bottom, right, z)
    xBlockSize = maxX - minX + 1
    yBlockSize = maxY - minY + 1
    print('X: ', minX, maxX, ', Y: ', minY, maxY, ', xBlockSize:', xBlockSize, ', yBlockSize:', yBlockSize)
    print('<< タイル座標を計算 done')

    # 2. タイルの画像を国土地理院からダウンロード
    print('>> 国土地理院からファイルをダウンロード start')
    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            url = 'https://cyberjapandata.gsi.go.jp/xyz/ort/' + str(z) + '/' + str(x) + '/' + str(y) + '.jpg'
            response = requests.get(url)
            with open('./tmp/divided/' + str(z) + '_' + str(x) + '_' + str(y) + '.jpg' , "wb") as f:
                f.write(response.content)
    print('<< 国土地理院からファイルをダウンロード done')

    # 3. 地図を合体(TSで実装)
    print('>> タイル画像を合成 start')
    # 透明の画像を作る
    img = Image.new("RGB", (256 * xBlockSize, 256 * yBlockSize), (0, 0, 0, 0))
    # タイル画像を貼り付ける
    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            tileImage = Image.open('./tmp/divided/' + str(z) + '_' + str(x) + '_' + str(y) + '.jpg')
            img.paste(tileImage, ((x - minX) * 256, (y - minY) * 256))
    img.save('./tmp/地図_タイル結合.png')
    print('<< タイル画像を合成 done')

    # 4. 地図に線を引いて区画を区切り、番号を付与して保存
    print('>> 地図を区切る線を追加 start')
    # 黒字で区画ごとに線を引く
    copy = img.copy()
    draw = ImageDraw.Draw(copy)
    number = 1
    font = ImageFont.truetype('Arial.ttf', 50)
    # NOTE: 左上から右下の順で番号を付与していきたいのでyからループを回す 
    for y in range(yBlockSize):
        for x in range(xBlockSize):
            # 線を引く
            startX = 255 * x + 1 * x
            endX = startX + 255
            startY = 255 * y + 1 * y
            endY = startY + 255
            draw.line(((startX, startY), (endX, startY), (endX, endY), (startX, endY)), fill=(0, 0, 0), width=5)
            # 番号を付与する
            centerX = (startX + endX) // 2 - 30
            centerY = (startY + endY) // 2 - 30
            draw.text((centerX, centerY), str(number), '#000000', font=font)
            number += 1
    copy.save('./img/overall_map.png')
    print('<< 地図を区切る線を追加 done')

    # 5. それぞれの区画にgeojsonのポリゴンの線を引いて、区画ごとに保存
    print('>> ポリゴンを引く start')
    draw = ImageDraw.Draw(img)
    number = 1

    for y in range(yBlockSize):
        for x in range(xBlockSize):
            # 線を引く
            startX = 255 * x + 1 * x
            endX = startX + 255
            startY = 255 * y + 1 * y
            endY = startY + 255
            draw.line(((startX, startY), (endX, startY), (endX, endY), (startX, endY)), fill=(127, 127, 127), width=5)
            # 
            number += 1

    drawPolygons('./json/2022_122319.json', draw, z, minX, minY, xBlockSize, yBlockSize)
    drawPolygons('./json/2022_122122.json', draw, z, minX, minY, xBlockSize, yBlockSize)

    img.save('./img/polygon_map.png')
    print('<< ポリゴンを引く done')

    print('<< 国土地理院のタイル画像から地図を生成 done')


if __name__ == '__main__':
    main()

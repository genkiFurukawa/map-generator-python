#!/usr/bin/env python

from map_gennerator.utils import calcPixcelCoordinate, calcTileCoordinate
from PIL import ImageFont, Image, ImageDraw

def main():
    top, bottom = 35.75621375767344, 35.740511743214284
    left, right = 140.2267393761772, 140.24713616224628
    z = 16
    
    print('>> 国土地理院のタイル画像から地図を生成 start')
    # 1. タイルの番号を計算(TSで実装)
    minX, minY, _ = calcTileCoordinate(top, left, z)
    maxX, maxY, _ = calcTileCoordinate(bottom, right, z)
    print('X: ', minX, maxX, ', Y: ', minY, maxY)

    # 2. タイルの画像を国土地理院からダウンロード(TSで未実装)
    
    # 3. 地図を合体(TSで実装)
    
    # 4. 地図に線を引いて区画を区切り、番号を付与して保存
    img = Image.open('./img/sample.png')
    # print(img.format, img.size, img.mode)
    # 黒字で区画ごとに線を引く
    xBlockSize = img.size[0] // 256
    yBlockSize = img.size[1] // 256
    # print(xBlockSize, yBlockSize)

    draw = ImageDraw.Draw(img)
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
            draw.line(((startX, startY), (endX, startY),
                       (endX, endY), (startX, endY)),
                      fill=(0, 0, 0),
                      width=5)
            # 番号を付与する
            centerX = (startX + endX) // 2 - 30
            centerY = (startY + endY) // 2 - 30
            draw.text((centerX, centerY), str(number), '#000000', font=font)
            number += 1
    img.save('./img/new.png')

    # 5. それぞれの区画にgeojsonのポリゴンの線を引いて、区画ごとに保存
    print('<< 国土地理院のタイル画像から地図を生成 done')


if __name__ == '__main__':
    main()

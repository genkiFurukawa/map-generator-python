#!/usr/bin/env python

from map_gennerator.utils import calcPixcelCoordinate, calcTileCoordinate, calcIntraTileCoordinate
from map_gennerator.drawPolygons import drawPolygons
from map_gennerator.downloadTileImages import downloadTileImages
from map_gennerator.mergeTileImages import mergeTileImages
from map_gennerator.drawDividingLines import drawDividingLines

def main():
    z = 18
    # NOTE: 左上と右下の緯度経度とグリッドサイズを指定する(いずれはコマンドラインでパースする)
    top, bottom = 35.75621375767344, 35.740511743214284
    left, right = 140.2267393761772, 140.24713616224628
    gridX, gridY = 3, 2

    print('>> 国土地理院のタイル画像から地図を生成 start')
    # 1. タイル画像をダウンロードする範囲を計算する
    minX, minY, _ = calcTileCoordinate(top, left, z)
    maxX, maxY, _ = calcTileCoordinate(bottom, right, z)
    
    # NOTE: 指定したグリッドサイズ単位で地図を生成したいため、足りない分の範囲を計算して上限値を変更する
    if (maxX - minX + 1) % gridX != 0:
        maxX += (gridX - ((maxX - minX + 1) % gridX))

    if (maxY - minY + 1) % gridY != 0:
        maxY += (gridY - ((maxY - minY + 1) % gridY))

    imageSizeX, imageSizeY = 256 * (maxX - minX + 1), 256 * (maxY - minY + 1)

    # 2. タイルの画像を国土地理院からダウンロード
    tileImageDir = './tileImages/' 
    downloadTileImages(minX, maxX, minY, maxY, z, tileImageDir)

    # 3. 国土地理院からダウンロードした地図を合成する
    mergeImagePath = './tmp/テスト.png'
    mergeTileImages(imageSizeX, imageSizeY, minX, maxX, minY, maxY, z, tileImageDir, mergeImagePath)

    # 4. 地図に線を引いて区画を区切り、番号を付与して保存
    dividingLineImagePath = './tmp/区切り線付き_地図.png'
    drawDividingLines(mergeImagePath, dividingLineImagePath, minX, maxX, minY, maxY, gridX, gridY, (0, 0, 0), 5, True)

    # 5. それぞれの区画にgeojsonのポリゴンの線を引いて、区画ごとに保存（区画は補助線をつける）
    dividingLineImagePath = './tmp/ポリゴン付き_地図.png'
    drawDividingLines(mergeImagePath, dividingLineImagePath, minX, maxX, minY, maxY, gridX, gridY, (127, 127, 127), 5, False)

    drawPolygons('./json/2022_122319.json', dividingLineImagePath, dividingLineImagePath, minX, maxX, minY, maxY, z)
    drawPolygons('./json/2022_122122.json', dividingLineImagePath, dividingLineImagePath, minX, maxX, minY, maxY, z)

    print('<< 国土地理院のタイル画像から地図を生成 done')

if __name__ == '__main__':
    main()

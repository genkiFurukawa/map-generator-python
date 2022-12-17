#!/usr/bin/env python

import os
import sys
from datetime import datetime
from glob import glob
import ulid
from map_gennerator.utils import calcTileCoordinate
from map_gennerator.drawPolygons import drawPolygons
from map_gennerator.downloadTileImages import downloadTileImages
from map_gennerator.mergeTileImages import mergeTileImages
from map_gennerator.drawDividingLines import drawDividingLines
from map_gennerator.generateGridImages import generateGridImages

def main():
    z = 18
    # NOTE: 左上と右下の緯度経度とグリッドサイズを指定する(いずれはコマンドラインでパースする)
    top, bottom = 35.75621375767344, 35.740511743214284
    left, right = 140.2267393761772, 140.24713616224628
    gridX, gridY = 3, 2
    resultDir = './result/sample01/'

    if not os.path.isdir(resultDir):
        print(str(datetime.now()) + ' [error] 結果を保存するディレクトリ( ' + resultDir + ' )が存在しません ')
        sys.exit(1)

    # 一時保存するディレクトリのパス
    tmpDir = './tmp/' + ulid.new().str + '/'
    if not os.path.isdir(tmpDir):
        os.mkdir(tmpDir)

    # 1. タイル画像をダウンロードする範囲を計算する
    print(str(datetime.now()) + ' [info] 国土地理院からタイル画像をダウンロードするためのタイル座標を計算(1/5)')
    minX, minY, _ = calcTileCoordinate(top, left, z)
    maxX, maxY, _ = calcTileCoordinate(bottom, right, z)
    
    # NOTE: 指定したグリッドサイズ単位で地図を生成したいため、足りない分の範囲を計算して上限値を変更する
    if (maxX - minX + 1) % gridX != 0:
        maxX += (gridX - ((maxX - minX + 1) % gridX))

    if (maxY - minY + 1) % gridY != 0:
        maxY += (gridY - ((maxY - minY + 1) % gridY))

    imageSizeX, imageSizeY = 256 * (maxX - minX + 1), 256 * (maxY - minY + 1)

    # 2. タイルの画像を国土地理院からダウンロード
    print(str(datetime.now()) +' [info] 国土地理院からタイル画像をダウンロード(2/5)')
    tileImageDir = './tileImages/' 
    downloadTileImages(minX, maxX, minY, maxY, z, tileImageDir)

    # 3. 国土地理院からダウンロードした地図を合成する
    print(str(datetime.now()) + ' [info] 国土地理院からタイル画像をダウンロードした画像を結合(3/5)')
    mergeImagePath = tmpDir + 'entire_map.png'
    mergeTileImages(imageSizeX, imageSizeY, minX, maxX, minY, maxY, z, tileImageDir, mergeImagePath)

    # 4. 地図に線を引いて区画を区切り、番号を付与して保存
    print(str(datetime.now()) + ' [info] 結合したタイル画像に対して区画番号を付与(4/5)')
    dividingLineImagePath = resultDir + '番号付き_全体地図.png'
    drawDividingLines(mergeImagePath, dividingLineImagePath, minX, maxX, minY, maxY, gridX, gridY, (0, 0, 0), 5, True)

    # 5. それぞれの区画にgeojsonのポリゴンの線を引いて、区画ごとに保存（区画は補助線をつける）
    print(str(datetime.now()) + ' [info] 区画番号ごとにポリゴンを描画して画像を保存(5/5)')
    # 地図全体に補助線を引く
    dividingLineImagePath = tmpDir + 'entire_map_with_polygons.png'
    drawDividingLines(mergeImagePath, dividingLineImagePath, minX, maxX, minY, maxY, gridX, gridY, (127, 127, 127), 5, False)

    # json形式のポリゴンを描画する
    jsonFiles = glob('./json/*.json')
    for jsonFile in jsonFiles:
        print(str(datetime.now()) + '   [info] 圃場ポリゴンを描画 (json: ' + jsonFile + ')')
        drawPolygons(jsonFile, dividingLineImagePath, dividingLineImagePath, minX, maxX, minY, maxY, z)

    # 番号ごとに分割してファイルを保存する
    dividedImageDir = resultDir + '分割/'
    if not os.path.isdir(dividedImageDir):
        os.mkdir(dividedImageDir )
    generateGridImages(dividingLineImagePath, dividedImageDir, minX, maxX, minY, maxY, gridX, gridY)

if __name__ == '__main__':
    main()

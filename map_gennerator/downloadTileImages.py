#!/usr/bin/env python

import os
import requests
from datetime import datetime

def downloadTileImages(minX, maxX, minY, maxY, z, tileImageDir):
    print(str(datetime.now()) + ' [info]   ダウンロードするタイルの画像枚数: ' + str((maxX + 1 - minX) * (maxY + 1 - minY)) + ' 件')
    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            path = tileImageDir + str(z) + '_' + str(x) + '_' + str(y) + '.jpg'
            # NOTE: ファイルがあるときは保存しない
            if not os.path.exists(path):
                url = 'https://cyberjapandata.gsi.go.jp/xyz/ort/' + str(z) + '/' + str(x) + '/' + str(y) + '.jpg'
                response = requests.get(url)
                with open(path , "wb") as f:
                    f.write(response.content)

import json
from map_gennerator.utils import calcPixcelCoordinate

def drawPolygons(filePath, draw, z, referenceX, referenceY, xBlockSize, yBlockSize):
    polygons = json.load(open(filePath, 'r'))['features']
    for polygon in polygons:
        coordinates = polygon['geometry']['coordinates'][0]
        # NOTE: タイル画像の中に含まれるかどうかチェック
        isContain = False
        for coordinate in coordinates:
            pixcelX, pixcelY, _ = calcPixcelCoordinate(coordinate[1], coordinate[0], z)
            x = pixcelX - 256 * referenceX
            y = pixcelY - 256 * referenceY
            
            if x > 0 and y > 0 and x < (256 * xBlockSize) and y < (256 * yBlockSize):
                isContain = True
                break

        # NOTE: 含まれる場合はポリゴンを描画
        if isContain:
            points = []
            for coordinate in coordinates:
                pixcelX, pixcelY, _ = calcPixcelCoordinate(coordinate[1], coordinate[0], z)
                x = pixcelX - 256 * referenceX
                y = pixcelY - 256 * referenceY
                                
                if x < 0:
                    x = 0
                
                if y < 0:
                    y = 0
                
                points.append(x)
                points.append(y)
            
            # NOTE: https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
            draw.polygon(points, fill = None, outline=(0, 0, 0), width=3)
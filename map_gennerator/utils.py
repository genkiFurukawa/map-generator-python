#!/usr/bin/env python

import math
from numpy import arctanh

L = 85.05112878

def calcPixcelCoordinate(lat, lng, zoomLevel):
    pixelX = math.floor((2 ** (zoomLevel + 7)) * (lng / 180 + 1))
    pixelY = math.floor((2 ** (zoomLevel + 7) / math.pi) * (-1 * arctanh(math.sin(math.pi * lat / 180)) + 1 * arctanh(math.sin(math.pi * L / 180))))
    return pixelX, pixelY, zoomLevel

def calcTileCoordinate(lat, lng, zoomLevel):
    pixelX, pixelY, z = calcPixcelCoordinate(lat, lng, zoomLevel)
    tileX = pixelX // 256
    tileY = pixelY // 256
    return tileX, tileY, z

def calcIntraTileCoordinate(lat, lng, zoomLevel):
    pixelX, pixelY, z = calcPixcelCoordinate(lat, lng, zoomLevel)
    tileX = pixelX // 256
    tileY = pixelY // 256
    intraTileX = pixelX % 256
    intraTileY = pixelY % 256
    return intraTileX, intraTileY, tileX, tileY, z
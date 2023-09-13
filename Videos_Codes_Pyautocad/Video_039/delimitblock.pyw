# Imports.
from pyautocad import Autocad, APoint
from _ctypes import COMError
import time

# Utiliy functions:

def point_order(x1: float, y1: float, x2: float, y2: float) -> tuple:
    # Returns the points ordered in function of X coordinate.
    if x1 <= x2:
        return x1, y1, x2, y2
    else:
        return x2, y2, x1, y1


def get_line_eq(x1: float, y1: float, x2: float, y2: float) -> tuple:
    # Returns the a and b constants of the line equation from two poins.
    if x1 == x2:  # For vertical lines.
        a = float(9999999999)  # Aproximate infinite.
        b = - a * x1
    else:  # For not vertical lines.
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
    return a, b


def get_lines_intersec(a1: float, b1: float, a2: float, b2: float) -> float:
    # Returns the intersection of two lines.
    x = (b2 - b1) / (a1 - a2)
    return x


def get_reverse_axes(points: list) -> tuple:
    # Inverts the X and Y coordinates from a list of points, [x1, y1, x2, y2] -> [y1, x1, y2, x2]
    reversed_points = []
    for i in range(int(len(points)/2)):
        reversed_points = reversed_points + [points[i * 2 + 1], points[i * 2]]
    return tuple(reversed_points)


def is_in_range(x: float, x1: float, x2: float) -> bool:
    # Returns 1 if the given X is in the range X1, X2.
    extension = sorted([x1, x2])
    return extension[0] <= x <= extension[1]


# Functions of point in polygon algorithm.

def is_in_limits(x: float, y: float, polyline: list) -> bool:
    # Returns 1 if the point is in the limits, 0 if is not.
    countIntersectionsX = 0
    a1, b1 = get_line_eq(x, y, x + 1, y)  # Line equation for point inside polygon.
    for i in range(int(len(polyline)/2 - 1)):
        x1, y1, x2, y2 = point_order(polyline[i * 2], polyline[i * 2 + 1], polyline[i * 2 + 2], polyline[i * 2 + 3])
        if is_in_range(y, y1, y2):
            a2, b2 = get_line_eq(x1, y1, x2, y2)  # Line equation for polygon side.
            try:
                if get_lines_intersec(a1, b1, a2, b2) >= x:
                    countIntersectionsX += 1
            except ZeroDivisionError:
                pass
    return bool(countIntersectionsX % 2)  # If mod 2 of countIntersection is 1 the point is in limits, otherwise is out.


def is_in_polygon(x: float, y: float, polygon: list) -> bool:
    # Returns 1 if the point is in the polygon 0 if is not.
    xLimits = is_in_limits(x, y, polygon)
    return bool(xLimits)


# Function for find nearest point of sides of polygon.

def nearest_side(x: float, y: float, polyline: list) -> tuple:
    # Returns nearest side of the polyline for the given point.
    x_root = float("inf")
    a1, b1 = get_line_eq(x, y, x + 1, y)  # Line equation for point.
    for i in range(int(len(polyline)/2 - 1)):
        x1, y1, x2, y2 = point_order(polyline[i * 2], polyline[i * 2 + 1], polyline[i * 2 + 2], polyline[i * 2 + 3])
        if is_in_range(y, y1, y2):
            a2, b2 = get_line_eq(x1, y1, x2, y2)  # Line equation for polygon side.
            try:
                root = get_lines_intersec(a1, b1, a2, b2)
                if abs(x - root) < abs(x - x_root):
                    x_root = root
            except ZeroDivisionError:
                pass
    return x_root, a1 * x_root + b1


# Asign main variable (api) of AutoCAD.
acad = Autocad()

# Getting block name and layer name, by user selection.
while True:
    try:
        time.sleep(0.5)
        blockName = acad.get_selection("Selecciona el tipo de bloque a acotar: ")
        blockName = blockName[0].Name.lower()
        break
    except COMError:
        pass

while True:
    try:
        time.sleep(0.5)
        layerName = acad.get_selection("Seleccione polilinea delimitante: ")
        layerName = layerName[0].Layer.lower()
        break
    except COMError:
        pass

# Searching blocks and polylines of current drawing.
blocks = acad.iter_objects("block", limit=None, dont_cast=True)
polylines = acad.iter_objects("polyline", limit=None, dont_cast=True)

# Filtering blocks and polylines.
filteredBlocks = [block for block in blocks if str(block.Name).lower() == blockName]
filteredPolylines = [pl for pl in polylines if str(pl.Layer).lower() == layerName]

# Graphic of dimensions.
for block in filteredBlocks:
    iPoint = block.InsertionPoint
    for poly in filteredPolylines:
        polyCoord = poly.Coordinates
        if is_in_polygon(iPoint[0], iPoint[1], polyCoord):
            xClose = nearest_side(iPoint[0], iPoint[1], poly.Coordinates)
            yClose = [*reversed(nearest_side(iPoint[1], iPoint[0], get_reverse_axes(polyCoord)))]
            acad.model.AddDimAligned(APoint(*xClose), APoint(iPoint), APoint((iPoint[0] + xClose[0])/2, xClose[1]))
            acad.model.AddDimAligned(APoint(*yClose), APoint(iPoint), APoint(yClose[0], (iPoint[1] + yClose[1])/2))

# Hello World! I am Axel, and... today is a good day!
#
# If this content is useful to you considerer to suscribe to my YouTube channel:
# https://www.youtube.com/channel/UCApz0-YSBjc3mLIPMu3EZ4w
#
# SUSCRIBE and LIKE! See you in the next one!

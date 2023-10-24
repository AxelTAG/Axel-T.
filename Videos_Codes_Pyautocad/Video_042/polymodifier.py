# Imports.
from pyautocad import Autocad, APoint
import pandas as pd


# Function that returns center of a line segment.
def segment_center(points: list) -> tuple:
    return (points[0] + points[2]) / 2, (points[1] + points[3]) / 2


# Returns geometric center of polygon/polyline.
def geometric_center(pl) -> tuple:
    coord = pl.Coordinates
    x_acum = 0
    y_acum = 0
    n = 0
    for index in range(0, len(coord) - 2, 2):
        sc = segment_center(coord[index:index + 4])
        x_acum += sc[0]
        y_acum += sc[1]
        n += 1
    return x_acum / n, y_acum / n


# Load csv to DataFrame.
file_path = input("Introduce csv file path: ")
df = pd.read_csv(file_path, index_col=0, delimiter=";")

print(df)

# Write areas in Polylines with ACAD APP.
acad = Autocad()

for i, handle in enumerate(df["handle"]):
    poly = acad.doc.HandleToObject(handle)
    center = geometric_center(poly)
    text = acad.model.AddText(str(df["area"][i]) + " m2", APoint(center[0], center[1]), 0.1)
    text.Alignment = 1
    text.TextAlignmentPoint = APoint(center[0], center[1])


# Hello World! I am Axel, and... today is a good day!
#
# If this content is useful to you considerer to suscribe to my YouTube channel:
# https://www.youtube.com/channel/UCApz0-YSBjc3mLIPMu3EZ4w
#
# SUSCRIBE and LIKE! See you in the next one!

# Imports.
from pyautocad import Autocad
import pandas as pd


# Utility functions.
def get_poly_areas(poly: list):
    return [[pl.Handle, pl.Area] for pl in poly]


# User inputs.
poly_layer = input("Introduce polylines layer: ")

# Getting polylines.
acad = Autocad()

# Getting polylines and filtering polylines.
polys = [poly for poly in acad.iter_objects_fast("Polyline") if poly.Layer == poly_layer]

# Export data to excel with pandas DataFrame.
df = pd.DataFrame(get_poly_areas(polys), columns=["handle", "area"])

dir_export = input("Introduce path of destination directory: ")
df.to_excel(dir_export)


# Hello World! I am Axel, and... today is a good day!
#
# If this content is useful to you considerer to suscribe to my YouTube channel:
# https://www.youtube.com/channel/UCApz0-YSBjc3mLIPMu3EZ4w
#
# SUSCRIBE and LIKE! See you in the next one!

import json
import pandas as pd

first = pd.read_csv("1-2in_interactionCurves.csv")
first = pd.read_csv("3-4in_interactionCurves.csv")


firstJson = {}

firstJson={
    "curve1X":first["curve1X"].to_list(),
    "curve1Y":first["curve1Y"].to_list(),
    
    "curve2X":first["curve2X"].to_list(),
    "curve2Y":first["curve2Y"].to_list(),
    
    "curve3X":first["curve3X"].to_list(),
    "curve3Y":first["curve3Y"].to_list(),
    
    "curve4X":first["curve4X"].to_list(),
    "curve4Y":first["curve4Y"].to_list()
    
}

json_first = json.dumps(firstJson)

with open("3-4in_interactionCurves.json","w") as outfile:
    outfile.write(json_first)

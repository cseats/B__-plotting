import pandas as pd
import plotly.express as px
import os

def getTension(strain):
    if strain<=0:
        strain = 0

    dcr = 100*strain/0.02
    return dcr

def getCompression(strain):
    if strain>=0:
        strain = 0
    dcr = 100*strain/0.0033
    return dcr

def addCompTens(inputName,parentDir):
    strains = ["strain-xx_top","strain-xx_mid","strain-xx_bot"]
    inputCSV = inputName+'.csv'

    inputPathCSV = os.path.join(parentDir,inputCSV)
    df = pd.read_csv(inputPathCSV)

    for s in strains:
        comp = []
        tens = []
        for index, row in df.iterrows():
            strain = row[s]
            comp.append(getCompression(strain))
            tens.append(getTension(strain))
            # print("calced")
        df[s+" Comp DCR"] = comp
        df[s+" Tens DCR"] = tens

    saveFileCSV = inputName+"_COMP_TENS.csv"
    savePathCSV = os.path.join(parentDir,saveFileCSV)

    df.to_csv(savePathCSV,index=False)

    return saveFileCSV
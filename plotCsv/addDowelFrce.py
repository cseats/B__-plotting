import pandas as pd
import plotly.express as px
import os
import math


def getTotalShear(fx,fy):
    #Total Shear = SQRT( Fx^2 + Fy^2)
    tS = math.sqrt(fx*fx + fy*fy)
    return tS

def calcDowelForce(inputName,parentDir):

    inputCSV = inputName+'.csv'

    inputPathCSV = os.path.join(parentDir,inputCSV)
    df = pd.read_csv(inputPathCSV)
    totalShearList = []
    for index,row in df.iterrows():

        fx = row["fx"]
        fy = row["fy"]
        totalShearList.append(getTotalShear(fx,fy))

    df['Total Shear'] = totalShearList

    saveFileCSV = inputName+"_totalShear.csv"
    savePathCSV = os.path.join(parentDir,saveFileCSV)

    df.to_csv(savePathCSV,index=False)

    return saveFileCSV
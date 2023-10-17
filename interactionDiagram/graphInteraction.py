import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

# Ploting fxns
def plotScatter(x,y,title):
    fig = px.scatter(x=x,y=y,title=title)
    fig.show()
    return fig

def plotLine(x,y,title):
    fig = px.line(x=x,y=y,title=title,markers=True)
    fig.show()
    return fig

def addTracePoint(x,y,fig,name):
    fig.add_trace(go.Scatter(x=x,y=y,mode='markers', name=name,marker_size=4,showlegend=False))
    return fig

def addTraceLine(x,y,fig,name):
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines+markers',name=name))
    return fig

#Data fxn
def getArray(df,col):
    array=np.array(df[col])
    return array[np.logical_not(np.isnan(array))]

def getCurves():
    curveDict={
        "curve1":[0,1],
        "curve2":[2,3],
        "curve3":[4,5],
        "curve4":[6,7]
        }

    df = pd.read_csv('InteractionCurves.csv')
    cols = list(df.columns)

    curves = []
    for c in cols:
        curves.append(getArray(df,c))
    
    return [curveDict,curves]



[curveDict,curves] = getCurves()
fig = go.Figure()
x = list(curves[4])
y = list(curves[5])
xInt = [-1*num for num in x]
addTraceLine(x,y,fig,"initial curve")

x = list(curves[6])
y = list(curves[7])
addTraceLine(x,y,fig,"initial curve")
# xInt = [-1*num for num in list(curves[2][0])]
# addTraceLine(xInt,y,fig,"flipped curve")



inputCSV = 'SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM'
df = pd.read_csv(inputCSV+'.csv')

sampleX = df['myy'].to_list()
sampleX = [-num for num in sampleX]

sampleY = df['fxx'].to_list()
sampleY = [-num for num in sampleY]
addTracePoint(sampleX,sampleY,fig,"Data")
# addTraceLine(sampleX,sampleY,fig,"")
fig.show()
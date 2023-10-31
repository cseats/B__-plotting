import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
import os

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
    fig.add_trace(go.Scatter(x=x,y=y,mode='markers', name=name,marker_size=14))
    return fig

def addTraceLine(x,y,fig,name):
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines+markers',name=name))
    return fig

#Data fxn
def getArray(df,col):
    array=np.array(df[col])
    return array[np.logical_not(np.isnan(array))]

def getCurves(thickness):
    curveDict={
        "curve1":[0,1],
        "curve2":[2,3],
        "curve3":[4,5],
        "curve4":[6,7]
        }
    cwd = os.getcwd()
    curvePath = os.path.join(cwd,"plotCsv","util")
    df = pd.read_csv(os.path.join(curvePath,thickness+'in_interactionCurves.csv'))
    cols = list(df.columns)

    curves = []
    for c in cols:
        curves.append(getArray(df,c))
    
    return [curveDict,curves]

#calculation fxns
def rotate(x,y,theta):
    xr = x*math.cos(math.radians(theta)) - y*math.sin(math.radians(theta))
    yr = y*math.cos(math.radians(theta)) + x*math.sin(math.radians(theta))
    return [xr,yr]

def calculate_angle(x, y):
    # Calculate the angle in radians using the arctangent function (atan2).
    angle = math.atan2(y, x)
    
    # Convert the angle from radians to degrees.
    angle_degrees = math.degrees(angle)
    
    # Ensure the angle is in the range [0, 360] degrees.
    if angle_degrees < 0:
        angle_degrees += 360
    
    return angle_degrees

def calcIntersection(x1,y1,x2,y2):
    if x1>x2:
        m = (y1-y2)/(x1-x2)
        xStart = x2
        yStart = y2
    elif x1<x2:
        m = (y2-y1)/(x2-x1)
        xStart = x1
        yStart = y1
                
    xTotal = xStart+-yStart/m

    return xTotal

# [curveDict,curves] = getCurves()

# xData = -830000
# yData = 14008082

# xData= -553909
# yData = 38485879
# xData=-xData

def getProportionUtil(xData,yData,thickness):
    [curveDict,curves] = getCurves(thickness)
    fig = go.Figure()
    if xData<0:
        curve = "curve4"
        curveFact = -1
        xData = -xData
    else:
        curve = "curve3"
        curveFact = 1

    addTracePoint([xData],[yData],fig,'SampleData')

    theta = 360-calculate_angle(xData, yData)
    [xS,yS] = rotate(xData,yData,theta)
    addTracePoint([xS],[yS],fig,'Rotated SampleData')

    currentCurveXY = curveDict[curve]
    # print(currentCurveXY)
    xCR = []
    yCR = []
    xC = []
    yC = []

    for i in range(len(curves[currentCurveXY[0]])):
        xi = curveFact*curves[currentCurveXY[0]][i]
        yi = curves[currentCurveXY[1]][i]
        xC.append(xi)
        yC.append(yi)
        [xR,yR] = rotate(xi,yi,theta)
        xCR.append(xR)
        yCR.append(yR)

    for i in range(len(yCR)-1):
        y1 = yCR[i]
        y2 = yCR[i+1]
        x1 = xCR[i]
        x2 = xCR[i+1]
        # print(f'Index is {i}')
        # print(f'Point 1 {x1} {y1}\n')
        # print(f'Point 2 {x2} {y2}\n')
        if y1>0 and y2<0 or y1<0 and y2>0:
            xTotal = calcIntersection(x1,y1,x2,y2)
            utilization = xS/xTotal*100
            # print('found it')
            break
        elif y1==0:
            xTotal=xCR[i]
            # print('found it')
            utilization = xS/xTotal*100
            break
        elif y2==0: 
            xTotal=xCR[i+1]
            utilization = xS/xTotal*100
            # print('found it')
            break
        else:
            # addTracePoint([xData],[yData],fig,'SampleData')
            # addTracePoint([xTotal],[0],fig,'SampleData')
            # addTraceLine([0,xTotal],[0,0],fig,"Radial Intersection")
            
            
            utilization = 999.999
    if utilization==999.999:
        addTracePoint([xData],[yData],fig,"Regular Data")
        addTracePoint([xS],[yS],fig,"rorated Data")
        addTraceLine(xC,yC,fig,"Regular Curve "+thickness+curve)
        addTraceLine(xCR,yCR,fig,"Rotated Curve "+thickness+curve)
        print(f"ERROR UTIL=999.99 with curve {curve} with thickness {thickness}")
        fig.show()
        print(xCR)
        print(yCR)
        raise Exception("F u")
    # print(xCR)
    # print(yCR)
    # print("Ended loop")
    # utilization = xS/xTotal*100
    # print(f'The utilization is{utilization}')




    # addTracePoint([xTotal],[0],fig,'SampleData')
    # addTraceLine([0,xTotal],[0,0],fig,"Radial Intersection")




    # addTraceLine(xC,yC,fig,"Regular Curve")
    # addTraceLine(xCR,yCR,fig,"Rotated Curve")

    # fig.update_xaxes(range=[-47E+6, 47E+6])
    # fig.update_yaxes(range=[-47E+6, 47E+6])
    # fig.update_layout(
    #     autosize=False,
    #     width=1250,
    #     height=1000,margin=dict(
    #         l=100,
    #         r=100,
    #         b=100,
    #         t=100,
    #         pad=4
    #     ))
    # fig.show()
    return utilization


def constForceCalc(xData,yData,thickness):
    [curveDict,curves] = getCurves(thickness)

    if xData<0:
        curveFact = -1
        xData = -xData
        xInt = curves[curveDict["curve2"][0]]
        xinit = curves[curveDict["curve2"][0]]
        xInt = [-1*num for num in xInt]
        yInt = list(curves[curveDict["curve2"][1]])
        xInt.reverse()
        yInt.reverse()

    else:
        
        curveFact = 1
        # xData = -xData
        xInt = curves[curveDict["curve1"][0]]
        yInt = list(curves[curveDict["curve1"][1]])
        # curve = "curve3"
        # curveFact = 1
    if yData in yInt:
        # print('there is a perfect match')
        index = yInt.index(yData)
        # print(f'Intersection occured at index: {index}')
        xTotal = xInt[index]
        yStart = yInt[index]
        xstart = xData
        
       
    else:
        for i in range(len(yInt)-1): #assumes this is a correct order, clockwise or counterclockwise (later will make a distinction of + or - axis) asume high to low
            y1 = yInt[i]
            y2 = yInt[i+1]
            x1 = xInt[i]
            x2 = xInt[i+1]

            if y1>yData and y2<yData:
                # print("here in if")
                #calculate slope, determine which point is the furthest right
                if x1>x2:
                    m = (y1-y2)/(x1-x2)
                    xStart = x2
                    yStart = y2
                elif x1<x2:
                    m = (y2-y1)/(x2-x1)
                    xStart = x1
                    yStart = y1
                
                xTotal = xStart+(yData-yStart)/m
                utilization = 100*(xData/xTotal)
                break
            else:
                utilization = 999.999
                xTotal = 0
                xStart=0
                yStart=0
                # print("not possible to compute utilization")
        # utilization = 0
    
    # utilization = 100*(xData/xTotal)
    # print(f'This is your utilizatioin {utilization}')
    # print(xData)
    # print(xTotal)
    if False:
        fig = go.Figure()
        addTracePoint([xData],[yData],fig,'SampleData')
        addTracePoint([-xData],[yData],fig,'Original Data')
        addTracePoint([xTotal],[yData],fig,'Intersection')
        addTraceLine([xData,xTotal],[yData,yData],fig,"Radial Intersection")



        # addTraceLine(curves[curveDict["curve2"][0]],yInt,fig,"Original Curve")
        addTraceLine(xInt,yInt,fig,"Reflected Curve")
        addTraceLine(xinit,yInt,fig,"Initial curve")
        # addTraceLine(xCR,yCR,fig,"Rotated Curve")

        fig.update_xaxes(range=[-47E+6, 47E+6])
        fig.update_yaxes(range=[-47E+6, 47E+6])
        fig.update_layout(
            autosize=False,
            width=1250,
            height=1000,margin=dict(
                l=100,
                r=100,
                b=100,
                t=100,
                pad=4
            ))
        fig.show()
        print(xInt)
        print(yInt)
    return utilization

# xData = -501820

# yData = -1187000
# [curveDict,curves] = getCurves()
# fig = go.Figure()
# x = list(curves[2])
# # print(x)
# y = list(curves[3])
# xInt = [-1*num for num in x]
# addTraceLine(x,y,fig,"initial curve")
# # xInt = [-1*num for num in list(curves[2][0])]
# addTraceLine(xInt,y,fig,"flipped curve")
# fig.show()

# utilF = constForceCalc(xData,yData)
def addUtilization_PropFrce(inputName,parentDir):

    inputCSV = inputName+'.csv'
    inputPathCSV = os.path.join(parentDir,inputCSV)

    df = pd.read_csv(inputPathCSV)

    thicknessList = ['1-2','3-4']

    sampleX = df['myy'].to_list()
    sampleX = [-num for num in sampleX]
    sampleY = df['fxx'].to_list()
    sampleY = [-num for num in sampleY]
    saveFiles = []
    for thickness in thicknessList:
        fig = go.Figure()
        proportionUtil = []
        utilCFrc = []

        for i in range(len(sampleX)):
            xData = sampleX[i]
            yData = sampleY[i]
            utilF = constForceCalc(xData,yData,thickness)
            pFrce = getProportionUtil(xData,yData,thickness)

            utilCFrc.append(utilF)
            proportionUtil.append(pFrce)
            if utilF<0 or pFrce<0:
                print(f"Constant Force: we have a problem with index {i}")

        df['Constant Force Utilization'] = utilCFrc
        df['Proportional Utilization'] = proportionUtil

        saveFileCSV = inputCSV+" "+thickness+'thick With UtilizationCurve.csv'
        saveFiles.append(saveFileCSV)
        df.to_csv(os.path.join(parentDir,saveFileCSV),index=False)

    return saveFiles
        
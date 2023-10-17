import pandas as pd
import plotly.express as px
import os
import math
import plotly.graph_objects as go

def addTracePoint(x,y,fig):
    fig.add_trace(go.Scatter(x=x,y=y,mode='markers', name='markers'))
    return fig

def addTraceLine(x,y,fig):
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines+markers',name='lines+markers'))
    return fig


def calculate_angle(x, y):
    # Calculate the angle in radians using the arctangent function (atan2).
    angle = math.atan2(y, x)
    
    # Convert the angle from radians to degrees.
    angle_degrees = math.degrees(angle)
    
    # Ensure the angle is in the range [0, 360] degrees.
    if angle_degrees < 0:
        angle_degrees += 360
    
    return angle_degrees


def rotate(x,y,theta):
    xr = x*math.cos(math.radians(theta)) - y*math.sin(math.radians(theta))
    yr = y*math.cos(math.radians(theta)) + x*math.sin(math.radians(theta))
    return [xr,yr]

def calcIntersectionProportional(x1,y1,x2,y2):
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


def calcProportional(interactionX,dataX,dataY):
    theta = 360-calculate_angle(dataX, dataY)
    intX = []
    intY = []
    rotX = []
    rotY = []

    for x,y in interactionX:
        intX.append(x)
        intY.append(y)

        # print(f'This is theta {theta}')
        [xr,yr] = rotate(x,y,theta)
        rotX.append(xr)
        rotY.append(yr)

    [xS,yS] = rotate(dataX,dataY,theta)
    for i in range(len(rotY)-1):
        y1 = rotY[i]
        y2 = rotY[i+1]
        x1 = rotX[i]
        x2 = rotX[i+1]
        # print(f'Index is {i}')

        if y1>0 and y2<0 or y1<0 and y2>0:
            xTotal = calcIntersectionProportional(x1,y1,x2,y2)
            # print('found it')
            break
        elif y1==0:
            xTotal=rotX[i]
            # print('found it')
            break
        elif y2==0: 
            xTotal=rotX[i+1]
            # print('found it')
            break
    # print("Ended loop")
    utilization = xS/xTotal*100
    # print(f'The utilization is{utilization}')

    return utilization


def constForceCalc(xData,yData,xInt,yInt):
  
    if yData in yInt:
        # print('there is a perfect match')
        index = yInt.index(yData)
        # print(f'Intersection occured at index: {index}')
        xTotal = xInt[index]
        
       
    else:
        for i in range(len(yInt)-1): #assumes this is a correct order, clockwise or counterclockwise (later will make a distinction of + or - axis) asume high to low
            y1 = yInt[i]
            y2 = yInt[i+1]
            x1 = xInt[i]
            x2 = xInt[i+1]

            if y1>yData and y2<yData:

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
        # utilization = 0
    
    # utilization = 100*(xData/xTotal)
    # print(f'This is your utilizatioin {utilization}')

    return utilization

inputCSV = 'SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM'
df = pd.read_csv(inputCSV+'.csv')

sampleX = df['myy'].to_list()
sampleY = df['fxx'].to_list()

interactionX = [
[ 0.00E+00,	5.00E+06],
[1.00E+06,	0.00E+00],
[7.50E+05,	-5.00E+06],
[5.00E+05,	-1.00E+07],
[0.00E+00,	-1.50E+07]
]
intX = []
intY = []
for x,y in interactionX:
    intX.append(x)
    intY.append(y)

fig = go.Figure()
fig = addTraceLine(intX,intY,fig)

proportional = []
constForce = []
for i in range(len(sampleX)):
    dataX = sampleX[i]
    negFlag=False
    if dataX<0:
        dataX=-dataX
        negFlag=True
    dataY = sampleY[i]

    theta = calculate_angle(x, y) 
    utilProport = calcProportional(interactionX,dataX,dataY)
    if utilProport>100:
        # print("Proportional: Greater than 100")
        _booger = 0
    if utilProport<0:
        print(f"Proportional: we have a problem with index {i}")
    proportional.append(utilProport)

    utilCFrce = constForceCalc(dataX,dataY,intX,intY)
    if utilCFrce>100:
        # print("Constant Force: Greater than 100")
        _booger = 0
    if utilCFrce<0:
        print(f"Constant Force: we have a problem with index {i}")
    constForce.append(utilCFrce)

    fig = addTracePoint([dataX],[dataY],fig)    
fig.show() 
df['Constant Force Utilization'] = constForce
df['Proportional Utilization'] = proportional

df.to_csv(inputCSV+' With Utilization.csv')
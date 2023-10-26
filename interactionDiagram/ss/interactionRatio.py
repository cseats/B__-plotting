import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os


def plotScatter(x,y,title):
    fig = px.scatter(x=x,y=y,title=title)
    fig.show()
    return fig
def plotLine(x,y,title):
    fig = px.line(x=x,y=y,title=title,markers=True)
    fig.show()
    return fig

def addTracePoint(x,y,fig):
    fig.add_trace(go.Scatter(x=x,y=y,mode='markers', name='markers'))
    return fig

def addTraceLine(x,y,fig):
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines+markers',name='lines+markers'))
    return fig

def constForce(xData,yData,xInt,yInt):
    
    print(xData,yData,xInt,yInt)

    # Check to see if there is a perfect match for Y
    print(f'this is ydata {yData}')
    print(f'this is yInt {yInt}')
    print(yData in yInt)
    if yData in yInt:
        print('there is a perfect match')
        index = yInt.index(yData)
        print(f'Intersection occured at index: {index}')
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




                # else: #they are equal





        print('need option 2')
        utilization = 0
    
    utilization = 100*(xData/xTotal)
    print(f'This is your utilizatioin {utilization}')

    return [xTotal,utilization]
    

interactionX = [
   [ 0.00E+00,	5.00E+06],
[1.00E+06,	0.00E+00],
[7.50E+05,	-5.00E+06],
[5.00E+05,	-1.00E+07],
[0.00E+00,	-1.50E+07]
]

sampleDataX = 2.00E+05
sampleDataY = -12.00E+06

intX = []
intY = []
for x,y in interactionX:
    intX.append(x)
    intY.append(y)

fig = go.Figure()

fig = addTracePoint([sampleDataX],[sampleDataY],fig)
fig = addTraceLine(intX,intY,fig)

[xTotal,utilization] = constForce(sampleDataX,sampleDataY,intX,intY)
fig = addTracePoint([xTotal],[sampleDataY],fig)
fig.show()
# plotLine(intX,intY,'interaction')



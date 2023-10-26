import plotly.express as px
import plotly.graph_objects as go
import math


def plotScatter(x,y,title):
    fig = px.scatter(x=x,y=y,title=title)
    fig.show()
    return fig
def plotLine(x,y,title):
    fig = px.line(x=x,y=y,title=title,markers=True)
    fig.show()
    return fig

def addTracePoint(x,y,fig,name):
    fig.add_trace(go.Scatter(x=x,y=y,mode='markers', name=name))
    return fig

def addTraceLine(x,y,fig,name):
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines+markers',name=name))
    return fig


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


interactionX = [
   [ 0.00E+00,	5.00E+06],
[1.00E+06,	0.00E+00],
[7.50E+05,	-5.00E+06],
[5.00E+05,	-1.00E+07],
[0.00E+00,	-1.50E+07]
]

sampleDataX = -2.00E+05
sampleDataY = 2.00E+06
# def calcConstForce(interactionX,)

intX = []
intY = []

rotX = []
rotY = []

theta = 360-calculate_angle(sampleDataX, sampleDataY)
for x,y in interactionX:
    intX.append(x)
    intY.append(y)

    print(f'This is theta {theta}')
    [xr,yr] = rotate(x,y,theta)
    rotX.append(xr)
    rotY.append(yr)

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


[xS,yS] = rotate(sampleDataX,sampleDataY,theta)
for i in range(len(rotY)-1):
    y1 = rotY[i]
    y2 = rotY[i+1]
    x1 = rotX[i]
    x2 = rotX[i+1]
    print(f'Index is {i}')

    if y1>0 and y2<0 or y1<0 and y2>0:
        xTotal = calcIntersection(x1,y1,x2,y2)
        print('found it')
        break
    elif y1==0:
        xTotal=rotX[i]
        print('found it')
        break
    elif y2==0: 
        xTotal=rotX[i+1]
        print('found it')
        break
print("Ended loop")
utilization = xS/xTotal*100
print(f'The utilization is{utilization}')






fig = go.Figure()
fig = addTraceLine(intX,intY,fig, "Original interaction")
fig = addTraceLine(rotX,rotY,fig,"Rotated Interaction")
fig = addTracePoint([sampleDataX],[sampleDataY],fig,"Original point")
fig = addTracePoint([xS],[yS],fig,'Rotated point')
fig = addTracePoint([xTotal],[yS],fig,'Intersection')
fig = addTraceLine([0,xTotal],[0,yS],fig,'X Allowed')
fig = addTraceLine([0,xS],[0,yS],fig,'X Utilized')

fig.update_xaxes(range=[-17E+6, 17E+6])
fig.update_yaxes(range=[-17E+6, 17E+6])
fig.show()

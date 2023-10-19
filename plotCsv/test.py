import pandas as pd
import plotly.graph_objects as go
# df = pd.read_csv('dowelPosition.csv')

# for index, rows in df.iterrows():
#     print(f'i am rows {rows}')
#     print(f'i am index {index}')
#     if rows['Ylocation'] != rows['Ylocation']:
#         print("no data for y location")
def addTraceLine(x,y,fig,name):
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines',name=name,marker_color="#0d0c0c",showlegend=False))
    return fig


def getDowels():
    df = pd.read_csv('dowelPosition.csv')
    angle = []
    ypos = []
    for index, rows in df.iterrows():
        if rows["Dowel"] == rows["Dowel"]:
            angle.append(rows["Dowel"])
        if rows['Ylocation'] == rows['Ylocation']:
            ypos.append(rows['Ylocation'])
    coords = []
    for ang in angle:
        xCord = []
        yCord = []
        for y in ypos:
            xCord.append(ang)
            yCord.append(y)
        
        coords.append([xCord,yCord])
    
    print(coords)
    print("\n")
    print("____________________________\n")
    print(coords[0])


# getDowels()

df = pd.read_csv('SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp.csv')

cyAll = df['cy'].to_list()
cy= list(set(cyAll))
print(f'Length of cyAll {len(cyAll)}')
print(f'Length of cy {len(cy)}')
fig = go.Figure()
for y in cy:
    dfSub = df[df["cy"]==y]
    fig = addTraceLine(dfSub['ang_deg'],dfSub['cy'],fig,"Test Dowels")

# fig.show()
print(df['cy'].max())
print(df['cy'].min())
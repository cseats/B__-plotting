import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os
def addTraceLine(x,y,fig,name):
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines+markers',name=name))
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
    for y in ypos:
        xCord = []
        yCord = []
        for ang in angle:
            xCord.append(ang)
            yCord.append(y)
        
        coords.append([xCord,yCord])
    return coords
def plot_dowels(fig,max,min):
    df = pd.read_csv('SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp.csv')

    cyAll = df['cy'].to_list()
    cy= list(set(cyAll))
    print(f'Length of cyAll {len(cyAll)}')
    print(f'Length of cy {len(cy)}')
    # fig = go.Figure()
    for y in cy:
        dfSub = df[df["cy"]==y]
        if y-.5>max or y+.5<min:
            booger = 0
            # print(f'sorry {y}, youre out of our range of {min} and {max}')
        else:
            fig.add_scatter(x=dfSub['ang_deg'],y=dfSub['cy'],mode='lines',showlegend=False,marker_color="#0d0c0c")
        # fig = addTraceLine(dfSub['ang_deg'],dfSub['cy'],fig,"Test Dowels")

    # fig.show()
    # print(df['cy'].max())
    # print(df['cy'].min())
    return fig
inputName = 'SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM'
inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx']
inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM3-4thick With UtilizationCurveNew','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM1-2thick With UtilizationCurveNew','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx_COMP_TENS','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp']


colNotResults = ['eid','cx','cy','cz','ang_rad','ang_deg']
degreeAxis = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
degreeAxis = [0,45,90,135,180,225,270,315,360]
# dowelCoords = getDowels()
dowelInfo = pd.read_csv('dowelPosition.csv')
formats = ['html','jpg']

for write in formats:
    for sheet in inputs:
        if not os.path.exists(sheet):
            os.mkdir(sheet)
        df = pd.read_csv(sheet+'.csv')    
        col = df.columns

        for i in col:
            if i not in colNotResults:
                print(i)
                # fig = go.Figure(go.Scatter(
                #         x=df['ang_deg'],y=df['cy'],mode='markers',
                #         labels=df['cx'].to_list(),
                #         text = df['eid'],
                #         hovertemplate = "%{label}: <br>Popularity: %{percent} </br> %{text}"
                #         # hovertemplate="<br>This is cx</br> %{label}"
                #     ))
                if i == "Constant Force Utilization" or i == "Proportional Utilization":
                    
                    fig = px.scatter(df,title=sheet+" " + i, x="ang_deg",y="cy",color=i,hover_name="eid",hover_data=["cx","cy","cz",'fxx (N)','myy (N-m)',"ang_deg"])
                    fig.update_coloraxes(cmin=0,cmax=150)
                    print('adjusted the range')
                    tickMax = 150
                    tickMin = 0
                elif "DCR" in i:
                    if "Tens" in i:
                        fig = px.scatter(df,title=sheet+" " + i, x="ang_deg",y="cy",color=i,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
                        fig.update_coloraxes(cmin=0,cmax=150)
                        print('adjusted the range')
                        tickMax = 150
                        tickMin = 0
                    else:
                        fig = px.scatter(df,title=sheet+" " + i, x="ang_deg",y="cy",color=i,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
                        fig.update_coloraxes(cmin=-150,cmax=0)
                        print('adjusted the range')
                        tickMax = 0
                        tickMin = -150
                else:
                    fig = px.scatter(df,title=sheet+" " + i, x="ang_deg",y="cy",color=i,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
                    tickMax = df[i].max()
                    tickMin = df[i].min()
                    fig.update_coloraxes(cmin=tickMin,cmax=tickMax)
                if write =="html":
                    # fig.update_traces(marker=dict(size=14))
                    if sheet=='SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp':
                        fig.update_traces(marker=dict(size=16))
                    else:
                        fig.update_traces(marker=dict(size=14))
                else:
                    if sheet=='SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp':
                        fig.update_traces(marker=dict(size=8))
                    else:
                        fig.update_traces(marker=dict(size=4))

                fig = plot_dowels(fig,df['cy'].max(),df['cy'].min())
                fig.update_layout(font_family="Times New Roman",
                                  title=dict(text=sheet+" " ,font=dict(size=14),yref="container"),title_pad_l=90,title_pad_t=30,
                                  xaxis = dict(tickmode="array",tickvals=degreeAxis),xaxis_title="0 = Right Springline | 90 = Crown | 180 = Left Springline | 270 = invert",yaxis_title="cy (meters)")
                                #   xaxis = dict(tickmode='linear',tick0=0,dtick=15))
                                # x
                fig.update_xaxes(title_font_family="Times New Roman")

                dtick = abs(tickMax-tickMin)/10
                fig.update_coloraxes(colorbar=dict(dtick=dtick),colorbar_ypad=20,colorbar_title_font_family="Times New Roman",colorbar_title_font_size=12,colorbar_title_side="top")

                # fig.update_coloraxes(colorbar_title_font=dict())
                # fig.update_coloraxes()
                # fig.update_coloraxes(colorbar_title_font_size=12)

                # for dowel_i in range(1,12):
                #     if dowel_i>0:
                        
                #         fig.add_scatter(x=dowelInfo["angle"+str(dowel_i)],y=dowelInfo["yposition"+str(dowel_i)],mode='lines',showlegend=False,marker_color="#0d0c0c")
                #         # fig.layout.coloraxis2 = fig2.layout.coloraxis

                #         # fig.add_scatter(x=dowelInfo["angle"+str(dowel_i)],y=dowelInfo["yposition"+str(dowel_i)],showlegend=False,color=dowelInfo["displacement"+str(dowel_i)])
                # fig.add_scatter()
                if write =="html":
                    # fig.show()
                    fig.write_html(os.path.join(sheet,i+'.html'))
                if write =="jpg":
                    fig.write_image(os.path.join(sheet,i+'.jpeg'))
        #         break
        # break

    # for index,rows in df.itterrows():
    #     if i
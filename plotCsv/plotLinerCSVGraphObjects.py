import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os
def addTraceLine(x,y,fig,name):
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines+markers',name=name))
    return fig

# def getDowels():
#     df = pd.read_csv('dowelPosition.csv')
#     angle = []
#     ypos = []
#     for index, rows in df.iterrows():
#         if rows["Dowel"] == rows["Dowel"]:
#             angle.append(rows["Dowel"])
#         if rows['Ylocation'] == rows['Ylocation']:
#             ypos.append(rows['Ylocation'])
#     coords = []
#     for y in ypos:
#         xCord = []
#         yCord = []
#         for ang in angle:
#             xCord.append(ang)
#             yCord.append(y)
        
#         coords.append([xCord,yCord])
#     return coords
def plot_dowels(fig,max,min,input):
    df = pd.read_csv(input)

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
            fig.add_scatter(x=dfSub['ang_deg'],y=dfSub['cy'],mode='lines',line={'width': 2},showlegend=False,marker_color="#0d0c0c")
        # fig = addTraceLine(dfSub['ang_deg'],dfSub['cy'],fig,"Test Dowels")

    # fig.show()
    # print(df['cy'].max())
    # print(df['cy'].min())
    return fig



inputName = 'SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM'
inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx']
inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM3-4thick With UtilizationCurveNew','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM1-2thick With UtilizationCurveNew','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx_COMP_TENS','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp']

inputs = ["SCFZ_L-SC-1_O-1full_1013_Inner_Plate_001_dowel_force","SCFZ_L-SC-1_O-1full_1013_Inner_Plate_001_tie-rod_force"]
inputs = ["SCFZ_L-SC-1_O-1full_1013_Inner_Plate_001_dowel_force"]




def plotResults(dowelInput,inputCSVs,savePath,parentDir):

    colNotResults = ['eid','cx','cy','cz','ang_rad','ang_deg']
    degreeAxis = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
    degreeAxis = [0,45,90,135,180,225,270,315,360]
    # dowelCoords = getDowels()
    formats = ['html','jpg']

    for write in formats:
        for sheet in inputCSVs:
            
            indvSavePath = os.path.join(savePath,sheet[:-4])
            if not os.path.exists(indvSavePath):
                os.mkdir(indvSavePath)

            # curSheet = sheet+'.csv'
            print(f'This is parent Dir {parentDir}')
            print(f'This is the current sheet {sheet}')
            df = pd.read_csv(os.path.join(parentDir,sheet))    
            col = df.columns

            for i in col:
                if i not in colNotResults:
                    print(i)
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
                        if 'dowel'in sheet: #=='SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp':
                            print("YEEP")
                            fig.update_traces(marker=dict(size=16))
                        else:
                            fig.update_traces(marker=dict(size=14))
                    else:
                        if 'dowel'in sheet:#sheet=='SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp':
                            fig.update_traces(marker=dict(size=8))
                        else:
                            fig.update_traces(marker=dict(size=4))

                    fig = plot_dowels(fig,df['cy'].max(),df['cy'].min(),dowelInput)
                    fig.update_layout(font_family="Times New Roman",
                                    title=dict(text=sheet+" " ,font=dict(size=14),yref="container"),title_pad_l=90,title_pad_t=30,
                                    xaxis = dict(tickmode="array",tickvals=degreeAxis),xaxis_title="0 = Right Springline | 90 = Crown | 180 = Left Springline | 270 = invert",yaxis_title="cy (meters)")
                                    #   xaxis = dict(tickmode='linear',tick0=0,dtick=15))
                                    # x
                    fig.update_xaxes(title_font_family="Times New Roman")

                    dtick = abs(tickMax-tickMin)/10
                    fig.update_coloraxes(colorbar=dict(dtick=dtick),colorbar_ypad=20,colorbar_title_font_family="Times New Roman",colorbar_title_font_size=12,colorbar_title_side="top")

                    if write =="html":
                        # fig.show()
                        
                        fig.write_html(os.path.join(indvSavePath,i+" - "+sheet[:-4]+'.html'))
                    if write =="jpg":
                        fig.write_image(os.path.join(indvSavePath,i+" - "+sheet[:-4]+'.jpeg'))
            #         break
            # break

        # for index,rows in df.itterrows():
        #     if i

def main():
    path = "C:\\Users\\camp.seats\\Arup\\285400-00 BART SILICON VALLEY CP2 - Reporter_Results"
    listDir = os.listdir(path)
    print(listDir)
    #iterate through folders
    for i in listDir:
        parentDir = os.path.join(path,i)
        inputCSVs = []
        if "." not in i:
            
            savePath = os.path.join("results",i) #where to save-- local Dir
            if not os.path.exists(savePath):
                os.mkdir(savePath)


            for j in os.listdir(parentDir):
                print(j)
                if "dowel_disp" in j:
                    dowelInput = os.path.join(parentDir,j)
                
                if ".csv" in j:

                    inputCSVs.append(j)
                    

            plotResults(dowelInput,inputCSVs,savePath,parentDir)

if __name__=="__main__":
    main()
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import json
import copy

# sys.path.insert(0,'C:\\Users\\camp.seats\\OneDrive - Arup\\Documents\\0-GitHub\\2 - FEA\\285400-43 BART Plotting\\BSV-plotting\\interactionDiagram')
# from plotConstForce_Proportion import test

import addDowelFrce
import addUtilztn
import addCompTens


def getColNames():
    cwd = os.getcwd()
    # print(cwd)
    f = open(os.path.join(cwd,"plotCsv","util",'unitNames.json'))
    data = json.load(f)
    return data

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
    # print(f'Length of cyAll {len(cyAll)}')
    # print(f'Length of cy {len(cy)}')
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



# inputName = 'SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM'
# inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx']
# inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM3-4thick With UtilizationCurveNew','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM1-2thick With UtilizationCurveNew','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx_COMP_TENS','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp']

# inputs = ["SCFZ_L-SC-1_O-1full_1013_Inner_Plate_001_dowel_force","SCFZ_L-SC-1_O-1full_1013_Inner_Plate_001_tie-rod_force"]
# inputs = ["SCFZ_L-SC-1_O-1full_1013_Inner_Plate_001_dowel_force"]




def plotResults(dowelInput,inputCSVs,savePath,parentDir):

    colNotResults = ['eid','cx','cy','cz','ang_rad','ang_deg']
    degreeAxis = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
    degreeAxis = [0,45,90,135,180,225,270,315,360]
    # dowelCoords = getDowels()
    formats = ['html','jpg']

    colNameDict = getColNames()
    for sheet in inputCSVs:
        for write in formats:
            inputName = sheet[:-4]
            print(f"This is sheet {sheet}")
            print(f"This is input name {inputName}")
            if "tshell_FM" in sheet:
                print(1)
                newSheet = addUtilztn.addUtilization_PropFrce(inputName,parentDir)
            elif "strain" in sheet:
                print(2)
                newSheet = addCompTens.addCompTens(inputName,parentDir)
            elif "dowel_force" in sheet:
                print(3)
                newSheet = addDowelFrce.calcDowelForce(inputName,parentDir)
            else:
                print(4)
                newSheet = sheet
            # # print(savePath)
            # # print(inputName)
            # indvSavePath = os.path.join(savePath,inputName)
            # # print(indvSavePath)
            # if not os.path.exists(indvSavePath):
            #     os.mkdir(indvSavePath)



            # dfPath = os.path.join(parentDir,newSheet)
            # print(f'This is parent Dir {parentDir}')
            # print(f'This is the current sheet {newSheet}')
            # print(f'This is the dfPath {dfPath}')
            # df = pd.read_csv(dfPath)    
            # col = df.columns

            # for metric in col:
            #     if metric not in colNotResults:
            #         print("_____________________________________")
            #         print(f"Currently plotting results for: {metric}\n Sheet: {newSheet}")
            #         print("_____________________________________")
            #         if metric == "Constant Force Utilization" or metric == "Proportional Utilization":
            #             print("Constant force or Proportional Utilization")
            #             print(f"Currently plotting results for: {metric}\n Sheet: {newSheet}")
            #             print(f'These are the current cols {col}')
            #             fig = px.scatter(df,title=newSheet+" " + metric, x="ang_deg",y="cy",color=metric,hover_name="eid",hover_data=["cx","cy","cz",'fxx','fxz','myy',"ang_deg"])
                        
            #             fig.update_coloraxes(cmin=0,cmax=150,colorbar_title_text=colNameDict[metric])
                        
            #             # print('adjusted the range')
            #             tickMax = 150
            #             tickMin = 0
            #         elif "DCR" in metric:
            #             if "Tens" in metric:
            #                 fig = px.scatter(df,title=newSheet+" " + metric, x="ang_deg",y="cy",color=metric,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
            #                 fig.update_coloraxes(cmin=0,cmax=150,colorbar_title_text=colNameDict[metric])
            #                 # print('adjusted the range')
            #                 tickMax = 150
            #                 tickMin = 0
            #             else:
            #                 fig = px.scatter(df,title=newSheet+" " + metric, x="ang_deg",y="cy",color=metric,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
            #                 fig.update_coloraxes(cmin=-150,cmax=0,colorbar_title_text=colNameDict[metric])
            #                 # print('adjusted the range')
            #                 tickMax = 0
            #                 tickMin = -150
            #         else:
            #             fig = px.scatter(df,title=newSheet+" " + metric, x="ang_deg",y="cy",color=metric,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
            #             tickMax = df[metric].max()
            #             tickMin = df[metric].min()
            #             fig.update_coloraxes(cmin=tickMin,cmax=tickMax,colorbar_title_text=colNameDict[metric])
            #         if write =="html":
            #             # fig.update_traces(marker=dict(size=14))
            #             if 'dowel'in newSheet: #=='SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp':
            #                 # print("YEEP")
            #                 fig.update_traces(marker=dict(size=16))
            #             else:
            #                 fig.update_traces(marker=dict(size=14))
            #         else:
            #             if 'dowel'in newSheet:#sheet=='SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp':
            #                 fig.update_traces(marker=dict(size=8))
            #             else:
            #                 fig.update_traces(marker=dict(size=4))

            #         fig = plot_dowels(fig,df['cy'].max(),df['cy'].min(),dowelInput)
            #         fig.update_layout(font_family="Times New Roman",
            #                         title=dict(text=newSheet+" " ,font=dict(size=14),yref="container"),title_pad_l=90,title_pad_t=30,
            #                         xaxis = dict(tickmode="array",tickvals=degreeAxis),xaxis_title="0 = Right Springline | 90 = Crown | 180 = Left Springline | 270 = invert",yaxis_title="cy (meters)")
            #                         #   xaxis = dict(tickmode='linear',tick0=0,dtick=15))
            #                         # x
            #         fig.update_xaxes(title_font_family="Times New Roman")

            #         dtick = abs(tickMax-tickMin)/10
            #         fig.update_coloraxes(colorbar=dict(dtick=dtick),colorbar_ypad=20,colorbar_title_font_family="Times New Roman",colorbar_title_font_size=12,colorbar_title_side="top")

            #         if write =="html":
            #             # fig.show()
                        
            #             fig.write_html(os.path.join(indvSavePath,metric+" - "+newSheet[:-4]+'.html'))
            #         if write =="jpg":
            #             fig.write_image(os.path.join(indvSavePath,metric+" - "+newSheet[:-4]+'.jpeg'))
            # #         break
            # # break

        # for index,rows in df.itterrows():
        #     if i

def main():
    curFolder = "S1"
    path = f"C:\\Users\\camp.seats\\OneDrive - Arup\Documents\\0-GitHub\\2 - FEA\\285400-43 BART Plotting\\BSV-plotting\\inputCSV\\10-25-2023_V02\\{curFolder}"
    saveLoc = "C:\\Users\\camp.seats\\OneDrive - Arup\\Documents\\0-GitHub\\2 - FEA\\285400-43 BART Plotting\\BSV-plotting\\inputCSV\\10-25-2023_V02\\figures"
    
    listDir = copy.deepcopy(os.listdir(path))
    print(listDir)
    #iterate through folders
    for i in listDir:
        parentDir = os.path.join(path,i)
        inputCSVs = []
        if "." not in i:
            
            savePath = os.path.join(saveLoc,curFolder,i) #where to save-- local Dir
            if not os.path.exists(savePath):
                os.mkdir(savePath)

            parentDirList = copy.deepcopy(os.listdir(parentDir))
            for j in parentDirList:
                print(j)
                if "dowel_disp" in j:
                    dowelInput = os.path.join(parentDir,j)
                
                if ".csv" in j:

                    inputCSVs.append(j)
            
            print("_______________________________________________")
            print("STARTING PLOTS FOR:::")       
            print(dowelInput)
            print("\n")
            print(inputCSVs)
            print("\n")
            print(savePath)
            print("\n")
            print(parentDir)
            print("::::::::::::::::::::::::::::::::::::::::")
            print("_______________________________________________")
            plotResults(dowelInput,inputCSVs,savePath,parentDir)

if __name__=="__main__":
    main()
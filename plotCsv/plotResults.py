import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import json
import copy


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


def plot_dowels(fig,max,min,input):
    df = pd.read_csv(input)

    cyAll = df['cy'].to_list()
    cy= list(set(cyAll))

    for y in cy:
        dfSub = df[df["cy"]==y]
        if y-.5>max or y+.5<min:
            booger = 0
        else:
            fig.add_scatter(x=dfSub['ang_deg'],y=dfSub['cy'],mode='lines',line={'width': 2},showlegend=False,marker_color="#0d0c0c")

    return fig







def plotResults(dowelInput,inputCSVs,savePath,parentDir):

    colNotResults = ['eid','cx','cy','cz','ang_rad','ang_deg']
    degreeAxis = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
    degreeAxis = [0,45,90,135,180,225,270,315,360]
    # dowelCoords = getDowels()
    formats = ['jpg','html']

    colNameDict = getColNames()
    firstStrain = True
    for sheet in inputCSVs:
        inputName = sheet[:-4]
        if "tshell_FM" in sheet and firstStrain:
            utilSheets = addUtilztn.addUtilization_PropFrce(inputName,parentDir)
            if firstStrain:
                newSheet = utilSheets[0]
                inputCSVs.append(utilSheets[1])
                firstStrain=False
            
        elif "strain" in sheet:
            newSheet = addCompTens.addCompTens(inputName,parentDir)
        elif "dowel_force" in sheet:
            newSheet = addDowelFrce.calcDowelForce(inputName,parentDir)
        else:
            newSheet = sheet
        # print(savePath)
        # print(inputName)
        folderExt = newSheet[:-4]
        indvSavePath = os.path.join(savePath,folderExt)
        # print(indvSavePath)
        if not os.path.exists(indvSavePath):
            os.mkdir(indvSavePath)



        dfPath = os.path.join(parentDir,newSheet)
        print(f'This is parent Dir {parentDir}')
        print(f'This is the current sheet {newSheet}')
        print(f'This is the dfPath {dfPath}')
        df = pd.read_csv(dfPath)    
        col = df.columns
        for write in formats:
            for metric in col:
                if metric not in colNotResults:
                    print("_____________________________________")
                    print(f"Currently plotting results for:{write} {metric}\n Sheet: {newSheet}")
                    
                    if metric == "Constant Force Utilization" or metric == "Proportional Utilization":
                        print("Constant force or Proportional Utilization")
                        print(f"Currently plotting results for: {metric}\n Sheet: {newSheet}")
                        print(f'These are the current cols {col}')
                        fig = px.scatter(df,title=newSheet+" " + metric, x="ang_deg",y="cy",color=metric,hover_name="eid",hover_data=["cx","cy","cz",'fxx','fxz','myy',"ang_deg"])
                        
                        fig.update_coloraxes(cmin=0,cmax=150,colorbar_title_text=colNameDict[metric])
                        
                        # print('adjusted the range')
                        tickMax = 150
                        tickMin = 0
                    elif "DCR" in metric:
                        if "Tens" in metric:
                            fig = px.scatter(df,title=newSheet+" " + metric, x="ang_deg",y="cy",color=metric,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
                            fig.update_coloraxes(cmin=0,cmax=150,colorbar_title_text=colNameDict[metric])
                            # print('adjusted the range')
                            tickMax = 150
                            tickMin = 0
                        else:
                            fig = px.scatter(df,title=newSheet+" " + metric, x="ang_deg",y="cy",color=metric,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
                            fig.update_coloraxes(cmin=-150,cmax=0,colorbar_title_text=colNameDict[metric])
                            # print('adjusted the range')
                            tickMax = 0
                            tickMin = -150
                    else:
                        fig = px.scatter(df,title=newSheet+" " + metric, x="ang_deg",y="cy",color=metric,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
                        tickMax = df[metric].max()
                        tickMin = df[metric].min()
                        fig.update_coloraxes(cmin=tickMin,cmax=tickMax,colorbar_title_text=colNameDict[metric])
                    if write =="html":
                        # fig.update_traces(marker=dict(size=14))
                        if 'dowel'in newSheet: #=='SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp':
                            # print("YEEP")
                            fig.update_traces(marker=dict(size=16))
                        else:
                            fig.update_traces(marker=dict(size=14))
                    else:
                        if 'dowel'in newSheet:#sheet=='SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp':
                            fig.update_traces(marker=dict(size=8))
                        else:
                            fig.update_traces(marker=dict(size=4))
                    if dowelInput:
                        fig = plot_dowels(fig,df['cy'].max(),df['cy'].min(),dowelInput)

                    fig.update_layout(font_family="Times New Roman",
                                    title=dict(text=newSheet+" " ,font=dict(size=14),yref="container"),title_pad_l=90,title_pad_t=30,
                                    xaxis = dict(tickmode="array",tickvals=degreeAxis),xaxis_title="0 = Right Springline | 90 = Crown | 180 = Left Springline | 270 = invert",yaxis_title="cy (meters)")
                                    #   xaxis = dict(tickmode='linear',tick0=0,dtick=15))
                                    # x
                    fig.update_xaxes(title_font_family="Times New Roman",autorange="reversed")

                    dtick = abs(tickMax-tickMin)/10
                    fig.update_coloraxes(colorbar=dict(dtick=dtick),colorbar_ypad=20,colorbar_title_font_family="Times New Roman",colorbar_title_font_size=12,colorbar_title_side="top")
                    metMax = max(df[metric].to_list())
                    metMin = min(df[metric].to_list())

                    fig.add_annotation(text=f"Max: {metMax}  |  Min: {metMin}",
                                        xref="paper", yref="paper",
                                         x=1, y=1.05, showarrow=False)
                    if write =="html":
                        # fig.show()
                        print("Writing Html file...")
                        fig.write_html(os.path.join(indvSavePath,metric+" - "+newSheet[:-4]+'.html'))
                        print("Html file is written.")
                    if write =="jpg":
                        print("Writing jpg file...")
                        fig.write_image(os.path.join(indvSavePath,metric+" - "+newSheet[:-4]+'.jpg'))
                        print("jpg file is written.")
                    
                    print("_____________________________________")
        #         break
        # break

    # for index,rows in df.itterrows():
    #     if i

def main():
    curFolder = "S4"
    curVersion = "11-01-2023_V01"

    mainPath = os.getcwd()
    inputsExtent = f"inputCSV\\{curVersion}\\{curFolder}"
    path = os.path.join(mainPath,inputsExtent)

    saveExtent = f"results"
    saveParent = os.path.join(mainPath,saveExtent,curVersion)
    if not os.path.exists(saveParent):
                os.mkdir(saveParent)

    saveLoc =os.path.join(saveParent,curFolder)      
    if not os.path.exists(saveLoc):
        print("The path does not exist making now ")
        os.mkdir(saveLoc)            


    listDir = copy.deepcopy(os.listdir(path))
    print(listDir)
    #iterate through folders
    for i in listDir:
        parentDir = os.path.join(path,i)
        inputCSVs = []
        if "." not in i:
            
            savePath = os.path.join(saveLoc,i) #where to save-- local Dir
            if not os.path.exists(savePath):
                os.mkdir(savePath)

            parentDirList = copy.deepcopy(os.listdir(parentDir))
            dowelInput = False
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

    print(f'Figures have been generated for {curFolder} in folder {curVersion}')
if __name__=="__main__":
    main()
    
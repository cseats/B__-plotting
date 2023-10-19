import pandas as pd
import plotly.express as px
import os


inputName = 'SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM'
inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx']
inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM With Utilization']


colNotResults = ['eid','cx','cy','cz','ang_rad','ang_deg']


for sheet in inputs:
    if not os.path.exists(sheet):
        os.mkdir(sheet)
    df = pd.read_csv(sheet+'.csv')    
    col = df.columns

    for i in col:
        if i not in colNotResults:
            print(i)
            if i == "Constant Force Utilization" or i == "Proportional Utilization":
                fig = px.scatter(df,title=sheet+" " + i, x="ang_deg",y="cy",color=i,hover_name="eid",hover_data=["cx","cy","cz",'fxx','myy',"ang_deg"],range_color=[-10,120])
                print('adjusted the range')
            else:
                fig = px.scatter(df,title=sheet+" " + i, x="ang_deg",y="cy",color=i,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
            fig.show()
            fig.write_image(os.path.join(sheet,i+'.jpeg'))
            fig.write_html(os.path.join(sheet,i+'.html'))

# for index,rows in df.itterrows():
#     if i
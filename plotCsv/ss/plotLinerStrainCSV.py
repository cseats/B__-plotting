import pandas as pd
import plotly.express as px
import os

def getTension(strain):
    if strain<=0:
        strain = 0

    dcr = 100*strain/0.02
    return dcr

def getCompression(strain):
    if strain>=0:
        strain = 0
    dcr = 100*strain/0.0033
    return dcr


inputName = 'SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx'
inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_FM','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_dowel_disp','SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx']
inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx']


colNotResults = ['eid','cx','cy','cz','ang_rad','ang_deg']

direction = ['tension','compression']
strains = ["strain-xx_top","strain-xx_mid","strain-xx_bot"]

# tension = df
# df = pd.read_csv(inputName+'.csv')

# for s in strains:
#     comp = []
#     tens = []
#     for index, row in df.iterrows():
#         strain = row[s]
#         comp.append(getCompression(strain))
#         tens.append(getTension(strain))
#         print("calced")
#     df[s+" Comp DCR"] = comp
#     df[s+" Tens DCR"] = tens

# df.to_csv('SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx_COMP_TENS.csv')

inputs = ['SCFZ_L-SC-1_O-2full_0922_Inner_Plate_002_IB032_tshell_strain_xx_COMP_TENS']

for sheet in inputs:
    if not os.path.exists(sheet):
        os.mkdir(sheet)
    df = pd.read_csv(sheet+'.csv')    
    col = df.columns

    for i in col:
        if i not in colNotResults:

            print(i)
            fig = px.scatter(df,title=sheet+" " + i, x="ang_deg",y="cy",color=i,hover_name="eid",hover_data=["cx","cy","cz","ang_deg"])
            fig.show()
            fig.write_image(os.path.join(sheet,i+'.jpeg'))
            fig.write_html(os.path.join(sheet,i+'.html'))

# # for index,rows in df.itterrows():
# #     if i
import os
import json
# path = "C:\\Users\\camp.seats\\Arup\\285400-00 BART SILICON VALLEY CP2 - Reporter_Results"
# listDir = os.listdir(path)
# print(listDir)
# for i in listDir:
#     if "." not in i:
#         print(i)
#         curPath = os.path.join("results",i)
#         if not os.path.exists(curPath):
#             os.mkdir(curPath)
#         iResults = os.path.join(path,i)
#         for j in os.listdir(iResults):
#             if "dowel_disp" in j:
#                 dowelRef = j



                
#         # print(os.listdir(iResults))    

# for i in range(7):
#     print(f"This is initial {i}")
#     if i==5:
#         i="dog"

#         print(f"This is after {i}")
import json
 
# Opening JSON file

cwd = os.getcwd()
print(cwd)
f = open(os.path.join(cwd,"plotCsv","util",'unitNames.json'))
# f = open('\\util\\unitNames.json')
 
# returns JSON object as 
# a dictionary
data = json.load(f)
print(data)
print(data["myy"])
print(data.myy)
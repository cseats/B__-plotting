import os

path = "C:\\Users\\camp.seats\\Arup\\285400-00 BART SILICON VALLEY CP2 - Reporter_Results"
listDir = os.listdir(path)
print(listDir)
for i in listDir:
    if "." not in i:
        print(i)
        curPath = os.path.join("results",i)
        if not os.path.exists(curPath):
            os.mkdir(curPath)
        iResults = os.path.join(path,i)
        for j in os.listdir(iResults):
            if "dowel_disp" in j:
                dowelRef = j



                
        # print(os.listdir(iResults))    
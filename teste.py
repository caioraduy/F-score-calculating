path= "C:\\Users\\raduy\\PycharmProjects\\InteractiveProcessDriftDetectionFW\\data\\output\\faltantes"
import os

for root, directories, files in os.walk(path):
    for file in files:
        if not 'IPDD_' in file:

            old_file = os.path.join(root,file)

            nfile =  file[0:4] +'_' + file[4:0]
            new_file = os.path.join(root, nfile)

            os.rename(old_file, new_file)































        











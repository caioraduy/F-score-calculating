path= "C:\\Users\\raduy\\PycharmProjects\\InteractiveProcessDriftDetectionFW\\data\\output\\console"
import os

for root, directories, files in os.walk(path):
    for file in files:
        old_file = os.path.join(root,file)

        nfile = 'IPDD_' +file
        new_file = os.path.join(root, nfile)

        os.rename(old_file, new_file)































        











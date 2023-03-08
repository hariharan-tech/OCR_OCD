import os
# count = 0
path = "D:\SSN ECE\sem6\ml_lab\mini_project_ML"
for root, dirs, files in os.walk(path):
    for file in files:
        if ".ttf" in file:
        # if "reep" in file:
            print(root,file)
# print(count)
import os
import csv
import shutil
import json

description = 'D:/DL/IQON3000/IQON3000/2598816/3877806/3877806.json'  # 取得json檔路徑
js = open(description)  # 打開json檔
des_dict = json.load(js)
for item in  des_dict['items']  :  # 取得分類資訊作為目標FOLDER
        print(item['itemId'])
        category = item['categorys']
        name = ''.join(category).split()
        print(name[-1])
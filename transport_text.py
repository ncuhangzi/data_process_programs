import os
import csv
import shutil
import json
import pandas as pd

paths = {
    'train_index':'../GPBPRcode/data/train.csv',
    'test_index':'../GPBPRcode/data/test.csv',
    'val_index':'../GPBPRcode/data/valid.csv',
    'dest_T_TA':'./data/top/train/',
    'dest_T_TE': './data/top/test/',
    'dest_T_VA': './data/top/valid/',
    'dest_B_TA': './data/bottom/train/',
    'dest_B_TE': './data/bottom/test/',
    'dest_B_VA': './data/bottom/valid/',
    'img_dest':'../IQON3000/IQON3000/',
}

dict = {}

def fit(csvfile, idx):
    #try:
        with open(paths[csvfile], newline='') as csvfile:
            rows = csv.reader(csvfile)
            print("success")
            curpath = ""
         #for i in tqdm(range(100)):
            #j=1
            exist=0
            dict_tmp = {}
            for row in rows:
                if(curpath != paths['img_dest']+row[0]):
                    curpath = paths['img_dest']+row[0] #打開到user資料夾
                    print('finding : '+ str(row[idx]))
                    #如果是下身 要改成row[2]
                curimg = row[idx]+ '_m.jpg' #目標圖片
                #os.chdir(curpath)
                results = os.listdir(curpath) #user資料夾內所有資料夾
                find = 0
                for res in results:
                    cur_res = curpath+'/'+res
                    results1 = os.listdir(cur_res)

                    if curimg in results1:
                        print('find!')
                        description = curpath+'/'+res+'/'+res+'.json' #取得json檔路徑
                        #print(description)
                        try:
                            js = open(description)  # 打開json檔
                            des_dict = json.load(js)
                        except:
                            continue

                        for item in  des_dict['items'] :#取得分類資訊作為目標FOLDER
                            if(str(item['itemId'])==row[idx]):
                                #print(item['itemId'])
                                title = item['itemName']
                                category = item['categorys']
                                category = ''.join(category)
                                total_description = title + category
                                if dict_tmp.__contains__(row[idx]):
                                    exist+=1
                                    find = 1
                                    break
                                else:
                                    dict_tmp[str(item['itemId'])] = total_description

                        if(find == 1):
                            break
                    else:
                        continue



                    js.close()
        return dict_tmp


#Top
dict.update(fit('train_index', 1))
print("Finish Top! train")

#Bottom
dict.update(fit('train_index', 2))
print("Finish Bottom! train")

#Top
dict.update(fit('test_index', 1))
print("Finish Top! test")

#Bottom
dict.update(fit('test_index', 2))
print("Finish Bottom! test")

#Top
dict.update(fit('val_index', 1))
print("Finish Top! val")

#Bottom
dict.update(fit('val_index', 2))
print("Finish Bottom! val")


#讀取dataframe轉化為tensor dict
df = pd.DataFrame.from_dict(dict, orient='index')
df.to_pickle('./textdict.pickle')



                #os.getcwd()
   # except:
       # print('ERROR NOT FOUND:' + paths[csv])
       # exit(1)

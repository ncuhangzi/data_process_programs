import os
import csv
import shutil
import json

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
def fit(csvfile, idx, dest):
    #try:
        with open(paths[csvfile], newline='') as csvfile:
            rows = csv.reader(csvfile)
            print("success")
            curpath = ""
         #for i in tqdm(range(100)):
            #j=1
            exist=0
            for row in rows:
                if(curpath != paths['img_dest']+row[0]):
                    curpath = paths['img_dest']+row[0] #打開到user資料夾
                    #如果是下身 要改成row[2]
                curimg = row[idx]+ '_m.jpg' #目標圖片
                #os.chdir(curpath)
                results = os.listdir(curpath) #user資料夾內所有資料夾
                find = 0
                for res in results:
                    cur_res = curpath+'/'+res
                    results1 = os.listdir(cur_res)
                    description = curpath+'/'+res+'/'+res+'.json' #取得json檔路徑
                    try:
                        js = open(description)  # 打開json檔
                        des_dict = json.load(js)
                    except:
                        continue

                    for item in  des_dict['items'] :#取得分類資訊作為目標FOLDER
                        if(str(item['itemId'])==row[idx]):
                            #print(item['itemId'])
                            category = item['categorys'] #取得category內的值
                            name = ''.join(category).split()
                            if len(name) >= 1:
                                path = os.path.join(paths[dest], name[-1])
                                if (name[-1] in os.listdir(paths[dest])):
                                    #print(name[-1] + 'is created!')
                                    exist+=1
                                else:
                                    os.mkdir(path)
                            else:
                                print("The list length is not enough : " + str(item['itemId']))


                    #print(results1)
                    for res1 in results1:
                        if(curimg==res1):
                            #print("moving...")
                            cur_res = cur_res + '/' + curimg
                            destlist = os.listdir(path) #打開目標資料夾
                            if (curimg in destlist): #確認是否已存在目標料夾
                                break
                            #如果是下身要改成 destB
                            destpath=path
                            shutil.copy(cur_res, destpath)

                            #確認這個圖片是否已經存在

                            #改名
                            #os.rename(destpath+'/'+curimg, destpath+'/'+str(j)+'.jpg')
                            #j += 1
                            find = 1
                            break
                    if(find == 1):
                        break

                    js.close()





                #os.getcwd()
   # except:
       # print('ERROR NOT FOUND:' + paths[csv])
       # exit(1)
#Top
fit('train_index', 1, 'dest_T_TA')
print("Finish Top! train")

#Bottom
fit('train_index', 2, 'dest_B_TA')
print("Finish Bottom! train")

#Top
fit('test_index', 1, 'dest_T_TE')
print("Finish Top! test")

#Bottom
fit('test_index', 2, 'dest_B_TE')
print("Finish Bottom! test")

#Top
fit('val_index', 1, 'dest_T_VA')
print("Finish Top! val")

#Bottom
fit('val_index', 2, 'dest_B_VA')
print("Finish Bottom! val")
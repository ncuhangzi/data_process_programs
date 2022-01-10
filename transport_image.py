import os
import csv
import shutil
import tqdm

paths = {
    'train_index':'./GPBPRcode/data/train.csv',
    'test_index':'./GPBPRcode/data/test.csv',
    'val_index':'./GPBPRcode/data/valid.csv',
    'dest_A':'./pix2pix/scripts/path/to/data/A/',
    'dest_B':'./pix2pix/scripts/path/to/data/B/',
    'img_dest':'./IQON3000/IQON3000/',
}
def fit(csvfile, folder, idx, dest):
    #try:
        with open(paths[csvfile], newline='') as csvfile:
            rows = csv.reader(csvfile)
            print("success")
            curpath = ""
         #for i in tqdm(range(100)):
            j=1
            for row in rows:
                if(curpath != paths['img_dest']+row[0]):
                    curpath = paths['img_dest']+row[0]
                    #如果是下身 要改成row[2]
                curimg = row[idx]+ '_m.jpg'
                #os.chdir(curpath)
                results = os.listdir(curpath)
                find = 0
                for res in results:
                    cur_res = curpath+'/'+res
                    results1 = os.listdir(cur_res)

                    #print(results1)
                    for res1 in results1:
                        if(curimg==res1):
                            print("moving...")
                            cur_res = cur_res + '/' + curimg
                            #如果是下身要改成 destB
                            destpath=paths[dest] + folder
                            shutil.copy(cur_res, destpath)
                            #改名
                            os.rename(destpath+'/'+curimg, destpath+'/'+str(j)+'.jpg')
                            j += 1
                            find = 1
                            break
                    if(find == 1):
                        break



                #os.getcwd()
   # except:
       # print('ERROR NOT FOUND:' + paths[csv])
       # exit(1)

fit('train_index', 'train', 1, 'dest_A')
print("FinishA!")
fit('train_index', 'train', 2, 'dest_B')
print("FinishB!")
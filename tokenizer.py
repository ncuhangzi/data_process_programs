from kuromojipy.kuromoji_server import KuromojiServer
import pandas as pd
import numpy as np
import keras
from tqdm import tqdm
import json
import pickle
import os
import torch




pickle_path = "./textdict.pickle"
df = pd.read_pickle(pickle_path)
dict_og = df.T.to_dict('list')
#print(dict_og)
if os.path.isfile('./tokenizedtext.json'):
    print('open existed dict!')
else:
    with KuromojiServer() as kuro_server:
        kuromoji = kuro_server.kuromoji
        tokenizer = kuromoji.Tokenizer.builder().build()
        print('Start tokenizing...')
        for key in tqdm(dict_og):
            tokens = tokenizer.tokenize(''.join(dict_og[key]))
            tmplist = []
            for token in tokens:
                tmplist.append(token.getSurfaceForm())
                # print(token.getSurfaceForm())

            dict_og[key] = tmplist

        dict_after = dict_og
        print('Finished!!')
        # print(dict_after)
    # f = open("tokenizedtext.pkl", "w")
    # pickle.dump(dict_after, f)

    json = json.dumps(dict_after)
    f = open("tokenizedtext.json", "w")
    f.write(json)
    f.close()

if os.path.isfile('./textfeatures'):
    ####load the tensor####
    text = torch.load('textfeatures', map_location=lambda a, b: a.cpu())
    print(text)

else:
    with open("tokenizedtext.json","r") as readfile:
        token_dict = json.load(readfile)
    # f = open('tokenizedtext.pkl')
    # token_dict = pickle.load(f)
        corpus  = token_dict.values()
        MAX_NUM_WORDS = 10000
        tokenizer = keras.preprocessing.text.Tokenizer(num_words=MAX_NUM_WORDS)
        tokenizer.fit_on_texts(corpus)
       # print(tokenizer.word_counts)

        for key in tqdm(token_dict):
            token_dict[key]  = tokenizer.texts_to_sequences(token_dict[key])
            arr = np.array(token_dict[key])
            #result = np.ndarray(shape=(1, arr.size))
            result = []
            for element in arr:
                if element:
                    result.append(element[0])
                else:
                    result.append(0)

                #print('element : '+str(element))
            #arr = np.ravel(np.array(result))
            token_dict[key] = result
            #token_dict[key] = np.ravel(arr.reshape((1,arr.size)))
            #print(token_dict[key])

        #print(token_dict)
        padding = keras.preprocessing.sequence.pad_sequences(token_dict.values(), maxlen=84)
        #print(padding)

        i = 0
        #mapping the padsequence to the dict
        #transform frmom numpy array to  torch tensor
        new_token_dict={}
        for key in token_dict:
            #key = int(key)
            token_dict[key] = padding[i]
            token_dict[key] = torch.tensor(token_dict[key])
            new_token_dict[int(key)] = token_dict[key]
            i+=1

        token_dict = new_token_dict
        # print(i)
        torch.save(token_dict, 'textfeatures')
        print([i for i in token_dict.keys()][-5:])
        print([i for i in token_dict.values()][-5:])
        #print(token_dict)






# df = pd.DataFrame.from_dict(dict_after, orient='index')
# print(df.head())
# df.to_pickle('./texttoken.pickle')



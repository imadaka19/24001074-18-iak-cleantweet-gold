import re
import pandas as pd
import db

#### cleansing data

stopword_table, abusive_table, kamus_alay_table = db.read_db()

kamus_alay_dict = dict(zip(kamus_alay_table['alay'], kamus_alay_table['tidak_alay']))

def norm_alay(data):
    return ' '.join([kamus_alay_dict[word] if word in kamus_alay_dict else word for word in data.split(' ')]) #mengganti kata di kamus alay

def remove_stopwords(data):
    return " ".join(x for x in data.split() if x not in stopword_table.stopword.values.tolist())
    # return ' '.join([word for word in data.split() if all(stop not in word for stop in set(stopword_table['stopword']))]) #menghapus kata yang ada di stopword_table

def clean_data(data):
    data = data.lower() #membuat semua huruf menjadi lower case
    data = data.strip() #menghapus white space di awal dan akhir
    # data = re.sub('\brt\b',' ',data, flags=re.IGNORECASE) #hapus rt
    data = re.sub('user',' ',data) #hapus kata user
    data = re.sub(r'#[\S]+', '', data)  #hapus hashtag
    data = re.sub('url',' ',data) #hapus 'url'
    data = re.sub(r'(http\S+)|((www\.[^\s]+))',' ',data) #hapus link url
    data = re.sub(r'\bx([a-fA-F0-9]{2})', '', data) #hapus unicode
    data = re.sub('[^a-zA-Z0-9]+', ' ', data) #hapus selain alfanumeric
    data = norm_alay(data) #merubah kosa kata alay menjadi tidak alay dari kamus alay
    data = remove_stopwords(data) #menghapus stopword
    data = data.strip() #menghapus white space di awal dan akhir
    return data
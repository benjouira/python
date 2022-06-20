import pandas as pd
import numpy as np
import re 
import pickle
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer

# ***************       prediction      ******************
def predict_bank (path):
    # prepper text
    pdf = pdfplumber.open(path)
    page = pdf.pages[0]
    text = page.extract_text()
    # delete tabs, newlines, etc,' ':
    text = re.sub('\s+',' ',text)
    pdf_head_text = text[0:100]

    # load model and old dataSet to re-transform to TFIDF
    model1 = pickle.load(open('./ML/model.pkl','rb'))
    df_tfidf = pickle.load(open("./ML/data_frame_for_TFIDF.pickle", "rb"))
    tfidf_new = TfidfVectorizer()

    # prepper df
    df2 = {'text' : pdf_head_text  ,'target' :'other' , 'Y' : '20'}
    df = df_tfidf
    df = df.append(df2 , ignore_index = True  )
    df3 = df[df['Y']== '20']

    tfidf_new = TfidfVectorizer()
    # apply TFIDF on old data
    features_new = tfidf_new.fit_transform(df_tfidf.text).toarray()

    # apply TFIDF on new data
    new_X_test = tfidf_new.transform(df3.text).toarray()
    

    # predict bank
    y_pred = model1.predict(new_X_test)

    return y_pred[0]

    

print (predict_bank("/project/app_uploaded_files/MAS_AB02_AOUT_2021.pdf"))
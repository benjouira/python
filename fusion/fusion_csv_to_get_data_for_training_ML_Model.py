import glob
import pdfplumber
import csv
import re


path_Glob = r"C:\\Users\\rabi3\\Desktop\\PFE\\MAS_2021"
folders = glob.glob(path_Glob + "\\*")
all_folders = [x.split("\\")[-1] for x in folders]

document = []
for folder in all_folders:
    all_paths = glob.glob(path_Glob+"\\"+ folder + "\\*.pdf")
    all_files = [x.split("\\")[-1] for x in all_paths]
    for filename in all_files:
        dataSet={}
        try:
            pdf = pdfplumber.open(path_Glob+"\\"+folder+"\\"+filename)
            page = pdf.pages[0]
            text = page.extract_text()                   
            # delete tabs, newlines, etc,' ':
            text = re.sub('\s+',' ',text)        
            dataSet ['text'] = text[0:100]
            dataSet ['target'] = folder
            document.append(dataSet)
        except:
            continue
    

# print (document)


try:
    with open('corpus.csv', 'w', encoding='utf-8-sig', newline='') as output_file:
        fc = csv.DictWriter(output_file, delimiter=';' , fieldnames= document[0].keys(),)
        fc.writeheader()
        fc.writerows(document)
except:
    print('the csv file is already open')

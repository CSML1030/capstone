import os
import eventlet
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

excel_data_filename = r'Basis State Industry List 071621.xlsx'
training_df = pd.read_excel(os.path.join('data', excel_data_filename), 
                            sheet_name=r'Training List',
                            engine='openpyxl')
training_df = training_df[~training_df['Organization - New Industry'].isnull()] 
web_descriptions = []
web_keywords = []
for website in training_df['Organization - Website']:
    print(website)
    if website != website: # if website is missing i.e. NaN
        web_descriptions.append('')
        web_keywords.append('')
    else:
        try:
            page = requests.get(website, timeout=20, verify=False).text
            soup = BeautifulSoup(page, 'lxml')

            try:
                description_tag = soup.select('meta[name="description"]')
                if description_tag != []:
                    web_descriptions.append(description_tag[0]['content'])  
                else:
                    web_descriptions.append('')
            except:
                web_descriptions.append('')

            try:
                keyword_tag = soup.select('meta[name="keywords"]')
                if keyword_tag != []:
                    web_keywords.append(keyword_tag[0]['content'])
                else:
                    web_keywords.append('')
            except:
                web_keywords.append('')
        except:
            web_descriptions.append('')
            web_keywords.append('')

training_df['web_description'] = pd.Series(web_descriptions)
training_df['web_keywords'] = pd.Series(web_keywords)
training_df.to_csv('training.csv')
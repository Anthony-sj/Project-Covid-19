#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

import pandas as pd
import numpy as np

df_case = pd.read_csv('../datas/covid_worldwide.csv')
df_wid = pd.read_csv('../datas/외교부_국가(지역)별 일반현황_20220629.csv', encoding='cp949')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)


# In[2]:


df_world_map=pd.read_excel('../datas/worldcities.xlsx',engine='openpyxl')
df_world_map=df_world_map[['country','lat','lng']]
df_world_map=df_world_map.drop_duplicates(['country'])
df_world_map=df_world_map.reset_index(drop=True)
df_world_map=df_world_map.sort_values('country')
df_world_map=df_world_map.rename(columns={'country':'국가명', 'lat' : '위도', 'lng': '경도'})
df_world_map=df_world_map.sort_values('국가명')
list_m=df_world_map['국가명'].unique()


# In[3]:


df_world_map


# In[4]:


dfc0 = df_case.rename(columns={'Serial Number': '고유번호', 'Country' : '국가명', 'Total Cases' : '확진수',
                        'Total Deaths' : '사망수', 'Total Recovered' : '회복수',
                        'Active Cases': '현발병', 'Total Test': '검사수', 'Population' : '인구'})
print(dfc0.columns)

dfc0.drop(['고유번호','현발병'], axis=1, inplace=True)

dfc0 = dfc0.replace(',','',regex=True) 
dfc0 = dfc0.set_index(['국가명'])

dfc=dfc0.dropna()

for i in dfc.columns:
    dfc[i]=dfc[i].astype('int')

dfc.drop(dfc[dfc['인구']  < (dfc['인구'].mean()*0.05)].index, inplace=True)


# In[5]:


dfc


# In[6]:


dfc_fin = dfc.copy()
dfc_fin

dw1= df_wid[['영문 국가명','면적']]
dw1=dw1.rename(columns={'영문 국가명' : '국가명'})
dw1

dfc_fin=dfc_fin.reset_index()
dfc_fin


C = {'UAE': 83600 , 'Hong Kong': 1114, 'UK':243610 , 'Czechia':78867, 'Italy':302072, 'S. Korea': 100210,
     'USA': 9830000,'Papua New Guinea': 452860, 'CAR' : 623000, 'DRC':2345408, 'Burundi' :  27834}


# In[7]:


dft = pd.merge(dfc_fin,df_world_map,how='outer',on='국가명')
dft = dft.set_index(['국가명'])
dft = pd.merge(dft,dw1, how ='outer', on = '국가명')
dft = dft.set_index(['국가명'])
dft


# In[8]:


for a in dft.index:
    if a in C:
        dft.loc[a]['면적'] = C[a]


# In[10]:


dict_loc = {'UAE':[23.7139,54.3035], 'CAR': [6.5741,20.4869], 'DRC' : [-2.6046, 22.2650], 'Congo':[-2.9244, 23.7446],
            'Gambia' :[13.4363, -15.4027],'North Macedonia' : [41.6505, 21.6511], 'USA' :[39.5265, -102.0569],
            'UK' :[54.9817, -2.8012], 'S. Korea':[37.5666, 126.9780]}

for nat in dft.index:
    if nat in dict_loc:
        dft.loc[nat]['위도'] = dict_loc[nat][0]
        dft.loc[nat]['경도'] = dict_loc[nat][1]
        
dft


# In[11]:


df_tot = dft.dropna()


# In[12]:


df_tot


# In[13]:


# 확진률 (확진수/검사수)
# 사망률 (사망수/확진수)
# 회복률 (회복수/확진수)
# 검사율 (검사수/인구)

col_dict = {'확진수':'검사수', '사망수':'확진수', '회복수': '확진수', '검사수':'인구'}

for j in col_dict:
    j = str(j)
    T = []
    for i in df_tot.index:
        i = str(i)
        T.append(df_tot.loc[i,j]/df_tot.loc[i,str(col_dict[j])]*100)
    df_tot[f'{j}율(%)']= T
        


# In[14]:


df_tot = df_tot.sort_values(by='검사수율(%)', ascending=False)
df_tot


# In[15]:


def pop_den(df):  # 인구밀도 열 추가
    T =[]
    for i in df.index:
        T.append(df.loc[i]['인구']/df.loc[i]['면적'])
    df['인구밀도'] = T


# In[16]:


pop_den(df_tot)
df_tot


# In[20]:


df_tot.info()


# In[21]:


df_tot.loc['총합'] = df_tot.iloc[:130,:5].sum()
df_tot.loc['평균'] = df_tot.iloc[:130,:].mean()


# In[22]:


df_tot


# In[ ]:


df_data=df_tot.copy()
df_data.drop(['총합','평균'],axis=0,inplace=True)


# In[32]:


df_data


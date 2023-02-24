#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

df_case = pd.read_csv('../datas/covid_worldwide.csv')
df_wid = pd.read_csv('../datas/외교부_국가(지역)별 일반현황_20220629.csv', encoding='cp949')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)


# In[2]:


dfc0 = df_case.rename(columns={'Serial Number': '고유번호', 'Country' : '국가명', 'Total Cases' : '확진수',
                        'Total Deaths' : '사망수', 'Total Recovered' : '회복수',
                        'Active Cases': '현발병', 'Total Test': '검사수', 'Population' : '인구'})
print(dfc0.columns)


# In[3]:


dfc0.drop(['고유번호','현발병'], axis=1, inplace=True)


# In[4]:


dfc0 = dfc0.replace(',','',regex=True) 
dfc0 = dfc0.set_index(['국가명'])


# In[5]:


dfc=dfc0.dropna()


# In[6]:


for i in dfc.columns:
    dfc[i]=dfc[i].astype('int')


# In[7]:


dfc.drop(dfc[dfc['인구']  < (dfc['인구'].mean()*0.05)].index, inplace=True)


# In[8]:


dfc.loc['총합'] = dfc.sum()
dfc


# In[9]:


# 확진률 (확진수/검사수)
# 사망률 (사망수/확진수)
# 회복률 (회복수/확진수)
# 검사율 (검사수/인구)

col_dict = {'확진수':'검사수', '사망수':'확진수', '회복수': '확진수', '검사수':'인구'}

for j in col_dict:
    j = str(j)
    T = []
    for i in dfc.index:
        i = str(i)
        T.append(dfc.loc[i,j]/dfc.loc[i,str(col_dict[j])]*100)
    dfc[f'{j}율(%)']= T
        
dfc


# In[10]:


dfc_fin = dfc.copy()


# In[11]:


dfc_fin = dfc_fin.sort_values(by='검사수율(%)', ascending=False)
dfc_fin.info()


# In[12]:


dfc_fin=dfc_fin.drop('총합')


# In[13]:


dfc_fin.info()


# In[ ]:





# In[14]:


dfc_1= dfc_fin.iloc[:21]
dfc_1


# In[15]:


dfc_2= dfc_fin.iloc[120:]
dfc_2.info()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





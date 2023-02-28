#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

import pandas as pd
import numpy as np


# In[2]:


# 판다스 보기 설정
pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)
pd.options.display.float_format = '{:.2f}'.format


# In[3]:


# csv 파일 로드
df_case = pd.read_csv('../datas/covid_worldwide.csv')
df_wid = pd.read_csv('../datas/외교부_국가(지역)별 일반현황_20220629.csv', encoding='cp949')
df_world_map=pd.read_excel('../datas/worldcities.xlsx',engine='openpyxl')


# In[4]:


df23 = df_case.sort_values(by ='Population')
df23


# In[ ]:





# In[5]:


# 위도 경도 파일 로드
df_world_map=df_world_map[['country','lat','lng']]
df_world_map=df_world_map.drop_duplicates(['country'])
df_world_map=df_world_map.reset_index(drop=True)
df_world_map=df_world_map.sort_values('country')
df_world_map=df_world_map.rename(columns={'country':'국가명', 'lat' : '위도', 'lng': '경도'})
df_world_map=df_world_map.sort_values('국가명')


# In[6]:


# 코로나 집계 데이터 프레임 열 인덱스 재설정
dfc0 = df_case.rename(columns={'Serial Number': '고유번호', 'Country' : '국가명', 'Total Cases' : '확진수',
                        'Total Deaths' : '사망수', 'Total Recovered' : '회복수',
                        'Active Cases': '현발병', 'Total Test': '검사수', 'Population' : '인구'})
print(dfc0.columns)


# In[ ]:





# In[7]:


# 필요없는 자료열 제거


# In[8]:


# 정수형 변환을 위해 특수문자 제거, 인덱스 설정, NaN값 자료행 제거
dfc0 = dfc0.replace(',','',regex=True) 
dfc0 = dfc0.set_index(['국가명'])


# In[9]:


for i in dfc0.columns:
    dfc0[i]=dfc0[i].astype('float')


# In[10]:


for a in dfc0.index:
    if np.isnan(dfc0.loc[a,'회복수']):
        dfc0.loc[a,'회복수'] = dfc0.loc[a,'확진수']-dfc0.loc[a,'사망수']
dfc0


# In[11]:


dfc0.drop(['고유번호','현발병'], axis=1, inplace=True)
dfc0
dfc=dfc0.dropna()


# In[12]:


# 각 요소를 정수형으로 변환
for i in dfc.columns:
    dfc[i]=dfc[i].astype('int')


# In[13]:


# 자료숫자가 매우 적은 행(나라) 제거
dfc.drop(dfc[dfc['인구']  < (dfc['인구'].mean()*0.05)].index, inplace=True)


# In[14]:


dfc


# In[15]:


dfc_fin = dfc.copy()
dfc_fin
# 면적 자료 데이터프레임 설정 및 가공
dw1= df_wid[['영문 국가명','면적']]
dw1=dw1.rename(columns={'영문 국가명' : '국가명'})
dw1
# merge 위해 위의 자료의 인덱스를 다시 열로 설정
dfc_fin=dfc_fin.reset_index()
dfc_fin


# In[16]:


# 면적과 위경도 데이터프레임 일괄 병합
dft = pd.merge(dfc_fin,df_world_map,how='outer',on='국가명')
dft = dft.set_index(['국가명'])
dft = pd.merge(dft,dw1, how ='outer', on = '국가명')
dft = dft.set_index(['국가명'])
dft


# In[17]:


# 일부 주요나라 누락자료(면적) 입력을 위한 딕셔너리 생성 - 수작업
C = {'UAE': 83600 , 'Hong Kong': 1114, 'UK':243610 , 'Czechia':78867, 'Italy':302072, 'S. Korea': 100210,
     'USA': 9830000,'Papua New Guinea': 452860, 'CAR' : 623000, 'DRC':2345408, 'Burundi' :  27834}


# In[18]:


# 누락된 면적 요소 삽입
for a in dft.index:
    if a in C:
        dft.loc[a]['면적'] = C[a]


# In[19]:


# 국가별 누락 데이터 딕셔너리 (위경도)
dict_loc = {'UAE':[23.7139,54.3035], 'CAR': [6.5741,20.4869], 'DRC' : [-2.6046, 22.2650], 'Congo':[-2.9244, 23.7446],
            'Gambia' :[13.4363, -15.4027],'North Macedonia' : [41.6505, 21.6511], 'USA' :[39.5265, -102.0569],
            'UK' :[54.9817, -2.8012], 'S. Korea':[37.5666, 126.9780]}


# In[20]:


# 위경도 요소 삽입
for nat in dft.index:
    if nat in dict_loc:
        dft.loc[nat]['위도'] = dict_loc[nat][0]
        dft.loc[nat]['경도'] = dict_loc[nat][1]
        
dft


# In[21]:


# 누락데이터 행 제거
df_tot = dft.dropna()


# In[ ]:





# In[22]:


df_tot


# In[23]:


# 확진률 (확진수/검사수)
# 사망률 (사망수/확진수)
# 회복률 (회복수/확진수)
# 검사율 (검사수/인구)
# 열 추가 함수

col_dict = {'확진수':'검사수', '사망수':'확진수', '회복수': '확진수', '검사수':'인구'}

for j in col_dict:
    j = str(j)
    T = []
    for i in df_tot.index:
        i = str(i)
        T.append(df_tot.loc[i,j]/df_tot.loc[i,str(col_dict[j])]*100)
    df_tot[f'{j}율']= T
        


# In[24]:


# 정렬
df_tot = df_tot.sort_values(by='검사수율', ascending=False)
 


# In[25]:


def pop_den(df):  # 인구밀도 열 추가 함수
    T =[]
    for i in df.index:
        T.append(df.loc[i]['인구']/df.loc[i]['면적'])
    df['인구밀도'] = T
    
def pop_par(df):  # 감염율 열 추가 함수
    P =[]
    for i in df.index:
        P.append(df.loc[i]['확진수']/df.loc[i]['인구']*100)
    df['감염율'] = P


# In[26]:


pop_den(df_tot)
pop_par(df_tot)
df_tot


# In[27]:


df_tot.info()


# In[28]:


df_tot.loc['총합'] = df_tot.iloc[:130,:5].sum()
df_tot.loc['평균'] = df_tot.iloc[:130,:].mean()


# In[29]:


df_tot.head()


# In[30]:


df_data=df_tot.copy()
df_data.drop(['총합','평균'],axis=0,inplace=True)


# In[31]:


df_data


# In[32]:


df_data.sort_values('확진수율')


# In[33]:


df_data.sort_values('사망수율')


# In[34]:


df_data.sort_values('검사수율')


# In[35]:


df_data.sort_values('인구밀도')


# In[36]:


df_data.사망수율.describe()


# In[37]:


df_data.to_csv('./df_data_137.csv')
df_tot.to_csv('./df_tot_137.csv')


# In[ ]:





# In[ ]:





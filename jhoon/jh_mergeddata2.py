#!/usr/bin/env python
# coding: utf-8

# In[12]:



import sys
sys.path.append("C:\\Users\\hunmi\\OneDrive\\바탕 화면\\project A\\Project-Covid-19\\ssj")

import pandas as pd
import poroject_DF as sj
import jhoon1 as jh


# In[2]:


df_upper=sj.dfc_1
df_rower=sj.dfc_2
df_location=jh.df_world_map
df_location.rename(columns={'Country' : '국가명',
                      
                      'lat':'위도','lng':'경도'},inplace=True)
df_upper.reset_index(drop=False, inplace=True)
df_rower.reset_index(drop=False, inplace=True)


# In[3]:


df1=pd.merge(df_upper,df_location,how='outer' ,on='국가명')
df2=pd.merge(df_rower,df_location,how='outer' ,on='국가명')


# In[ ]:





# In[4]:


df1=df1.set_index('국가명')


# In[5]:


df1=df1.iloc[:21]


# In[6]:


df1.loc['UAE']['위도']=23.7139
df1.loc['UAE']['경도']=54.3035
df1


# In[7]:


df2=df2.iloc[:19]
df2=df2.set_index('국가명')


# In[8]:


df2.loc['CAR']['위도']=6.5741
df2.loc['CAR']['경도']=20.4869
df2.loc['DRC']['위도']=-2.6046
df2.loc['DRC']['경도']=22.2650


# In[9]:


df2


# In[ ]:





# In[10]:


import matplotlib.pyplot as plt

# '검사수율(%)'을 x축, '사망수율(%)'을 y축으로 지정
x1 = df1['검사수율(%)']
y1 = df1['사망수율(%)']

# 산점도 그리기
plt.scatter(x1, y1)

# 축 레이블 설정
plt.xlabel('검사수율(%)')
plt.ylabel('사망수율(%)')

# 그래프 타이틀 설정
plt.title('')

# 그래프 보여주기
plt.show()


# In[11]:


import matplotlib.pyplot as plt

# '검사수율(%)'을 x축, '사망수율(%)'을 y축으로 지정
x2 = df2['검사수율(%)']
y2 = df2['사망수율(%)']

# 산점도 그리기
plt.scatter(x2, y2)

# 축 레이블 설정
plt.xlabel('검사수율(%)')
plt.ylabel('사망수율(%)')

# 그래프 타이틀 설정
plt.title('')

# 그래프 보여주기
plt.show()


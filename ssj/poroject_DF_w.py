#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

sys.path.append('C:\\Users\\82104\\Desktop\\SemiPro1\\jhoon')

import pandas as pd
import numpy as np
import poroject_DF as sj
import jhoon1 as jh


# In[2]:


dfc1 = sj.dfc_1


# In[3]:


dfc1=dfc1.reset_index()


# In[4]:


dfc2=sj.dfc_2


# In[5]:


dfc2=dfc2.reset_index()


# In[6]:


dw1= sj.df_wid[['영문 국가명','면적']]
dw1=dw1.rename(columns={'영문 국가명' : '국가명'})
dw1


# In[7]:


A = {'UAE': 83600 , 'Hong Kong': 1114, 'UK':243610 , 'Czechia':78867, 'Italy':302072, 'USA': 9830000}
B = {'Papua New Guinea': 452860, 'CAR' : 623000, 'DRC':2345408}


# In[8]:


df1 = pd.merge(dfc1,dw1,how='outer',on='국가명')
df1 = df1.iloc[:20, :]
df1


# In[ ]:





# In[9]:


df1[df1.면적.isna( )]['국가명'].unique()


# In[10]:


df2 = pd.merge(dfc2,dw1,how='outer',on='국가명')
df2 = df2.iloc[:19, :]
df2


# In[11]:


df1 = df1.set_index(['국가명'])

for a in df1.index:
    if a in A:
        df1.loc[a,'면적'] = A[a]

df1


# In[12]:


df2[df2.면적.isna( )]['국가명'].unique()


# In[14]:


df2 = df2.set_index(['국가명'])

for b in df2.index:
    if b in B:
        df2.loc[b,'면적'] = B[b]

df2


# In[ ]:





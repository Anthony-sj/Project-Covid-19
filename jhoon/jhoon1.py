#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium

from matplotlib import font_manager, rc

plt.rc('font', family='Malgun Gothic')
#세계 코로나 현황
df_covid_case=pd.read_csv('../datas/covid_worldwide.csv')
df_covid_case = df_covid_case.replace(',', '',regex=True)
df_covid_case.drop(['Serial Number','Active Cases'], axis=1, inplace=True)
df_covid_case['Total Cases']=df_covid_case['Total Cases'].astype(int)
df_covid_case=df_covid_case.sort_values('Country')
list_c=df_covid_case['Country'].unique()


# In[2]:


#나라 경위도
df_world_map=pd.read_excel('../datas/worldcities.xlsx',engine='openpyxl')
df_world_map=df_world_map[['country','lat','lng']]
df_world_map=df_world_map.drop_duplicates(['country'])
df_world_map=df_world_map.reset_index(drop=True)
df_world_map=df_world_map.sort_values('country')
df_world_map=df_world_map.rename(columns={'country':'Country'})
df_world_map=df_world_map.sort_values('Country')
list_m=df_world_map['Country'].unique()


# In[3]:


#나라이름 통일전 안맞는거확인
slist_c=pd.Series(list_c)
slist_m=pd.Series(list_m)
concat_countries=pd.concat([slist_c,slist_m],axis=1)

pd.set_option('display.max_columns', None) ## 모든 열 출력
pd.set_option('display.max_rows', None) ## 모든 행 출력
contry_list = list(concat_countries[1])

for row in concat_countries.index:
    if concat_countries.loc[row,0] in contry_list:
        concat_countries.loc[row,0] = np.NaN
concat_countries.sort_values(0).head(40)


# In[4]:


#나라이름 통일
df_world_map['Country'].replace('United States', 'USA', inplace=True)
df_world_map['Country'].replace('United Kingdom', 'UK', inplace=True)
df_world_map['Country'].replace('South Korea', 'S. Korea', inplace=True)
df_world_map['Country'].replace('Antigua And Barbuda', 'Antigua and Barbuda', inplace=True)
df_world_map['Country'].replace('Congo (Brazzaville)', 'Congo', inplace=True)
df_world_map['Country'].replace('Macau', 'Macao', inplace=True)


# In[5]:


#경위도와 세계코로나현황 합친거
merged_df = pd.merge(df_covid_case,df_world_map,how='inner',on='Country')
merged_df.head()


# In[6]:


#코로나 발생현황을 지도에 표시

merged_df.head()
merged_df.rename(columns={'Country' : '국가명', 'Total Cases' : '확진수',
                        'Total Deaths' : '사망수', 'Total Recovered' : '회복수',
                       'Total Test': '검사수', 'Population' : '인구','lat':'위도','lng':'경도'},inplace=True)

merged_df


# In[7]:


from folium import CircleMarker
world_map1=folium.Map(location=[0,0],zoom_start=1.5,tiles='stamen Toner')

# 데이터프레임에서 위도와 경도 열 추출
locations = merged_df[['위도', '경도']].values.tolist()

# 총 확진자 수 열 추출
cases = merged_df['확진수'].tolist()

# 최대 총 확진자 수 계산
max_cases = max(cases)

# CircleMarker를 사용하여 총 확진자 수에 따라 크기가 다른 원을 지도에 추가
for location, case in zip(locations, cases):
    CircleMarker(
        location=location,
        radius=case / max_cases * 50,  # 원의 크기는 최대 50으로 설정
        color='#cc0000',
        fill=True,
        fill_color='#800000',
    ).add_to(world_map1)
world_map1


# In[8]:


world_map=folium.Map(location=[0,0],zoom_start=1.5,tiles='stamen Toner')
from folium.plugins import HeatMap
HeatMap(
    data=merged_df[['위도', '경도','확진수']], 
    radius=20,
).add_to(world_map)




world_map


# In[9]:


#계산하기위해서 intiger로 변경
merged_df=merged_df.dropna()
merged_df[['사망수','회복수','검사수','인구']] = merged_df[['사망수','회복수','검사수','인구']].astype(int).copy()


# In[10]:


merged_df['검사비율']=(merged_df['검사수']/merged_df['인구'])
merged_df['사망률']=(merged_df['사망수']/merged_df['확진수'])
merged_df


# In[11]:


plt.scatter(merged_df['검사비율'], merged_df['사망수'])
plt.title('검사빈도에따른 국가별사망자수')
plt.xlabel('검사비율')
plt.ylabel('사망수')
plt.ylim(-20000,800000)
plt.show()


# In[12]:


merged_df = merged_df[merged_df['검사수']>=6386235]
merged_df


# In[13]:


plt.scatter(merged_df['검사비율'], merged_df['사망수'])
plt.title('검사빈도에따른 국가별사망자수')
plt.xlabel('검사비율')
plt.ylabel('사망수')
plt.ylim(-20000,800000)
plt.show()


# In[14]:


def zscore(x):
    z = (x - np.mean(x)) / np.std(x)
    return z


# In[15]:


merged_df=merged_df.set_index('국가명')


# In[16]:


import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False
zscore(merged_df['확진수'])

zscore(merged_df['확진수']).plot(kind='bar', figsize=(30, 5))

plt.title('')
plt.xlabel('Country',fontsize=20)
plt.ylabel('z-score')
plt.ylim(-1,8)
plt.show()


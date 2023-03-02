#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import random 
import seaborn as sns

pd.options.display.float_format = '{:.4f}'.format
import matplotlib.font_manager as fm

pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)
pd.options.display.float_format = '{:.2f}'.format
# 설치된 폰트 출력
sns.set(font='Malgun Gothic')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', family='Malgun Gothic')


# In[2]:


data1 = pd.read_csv('./df_data_137.csv')
data1.set_index('국가명',inplace=True)
data1


# In[3]:


# 열기준 정렬 함수
def sort_data(df,str_x):
    str_x =str(str_x)
    #x = str(input(f'정렬할 기준 열 이름 입력 : {df.columns}'))
    print()
    df = df.sort_values(str_x)
    return df

# 표준 점수
def z_score(x):
    return (x-x.mean())/x.std()

# 정규화 함수
def nomaliz(x):
    return (x-x.min())/(x.max()-x.min())


# In[4]:


# 시각화를 위한 요소간 격차를 줄이는 감쇠 매핑함수
def weakn(df,root_num):
    root_num = int(root_num)
    #root_num = int(input('.pipe(n 제곱근), 숫자(정수) n 입력 : '))
    print()
    return df.pipe(lambda a : a**(1/root_num)).pipe(nomaliz)

# 데이터 프레임에서 원하는 수만큼 
def random_nums(df,sample_idx):
    sample_idx = int(sample_idx)
    #sample_idx = int(input(f'랜덤 추출 수 입력( 0 ≤ x ≤ {len(df.index)} ) : '))
    print()
    nums = random.sample(range(0,len(df.index)), sample_idx)
    return nums


# In[5]:


def groupABC(value):
    if value == 'A-1':
        return 'A'
    elif value == 'A-2':
        return 'A'
    elif value == 'A-3':
        return 'A'
    elif value == 'B':
        return 'B'
    else:
        return 'C'


# In[6]:


def groupin(df,x):
    x =str(x)
    df['분할'] = df['분할'].apply(groupABC)
    df = df.groupby('분할')
    df = df.get_group(x)
    return df


# In[7]:


def binning():
    df3 = data1[['사망수율','검사수율']]
    count, bin_dividers= np.histogram(df3['사망수율'], bins=5)
    bin_names = ['C','B','A-3','A-2','A-1']
    df3['분할']= pd.cut(x=df3['사망수율'],
                       bins=bin_dividers,
                       labels=bin_names,
                       include_lowest=True)


    df3.reset_index(inplace=True)
    df3.set_index(['국가명'],inplace=True)
    df3= sort_data(df3,'사망수율')

    return df3   


# In[8]:


def corr_heatmap():
    corr = pd.DataFrame(index= data1.columns, columns= data1.columns)
    corr.drop(['회복수','위도','경도','면적','회복수율'], axis=0, inplace=True)
    corr.drop(['회복수','위도','경도','면적','회복수율'], axis=1, inplace=True)

    for colx in corr.columns:
        for coly in corr.columns:
            a = np.corrcoef(data1[colx], data1[coly])
            corr.loc[colx][coly] = a[0,1]
    

    A = corr
    A = A.pipe(lambda c: c*100)
    A = A.astype(int)
    ax = sns.heatmap(A,cmap = 'seismic')


# In[9]:


# df를 열이름 x의 오름차순으로 정렬후 10~120번째까지 자료들로 pair_plot 그리는 함수
# '검사수율','확진수율', '사망수율', '감염율','인구밀도' 열 사용
# 검사수율 = 검사수/인구 , 확진수율 = 확진수/검사수  , 사망수율 = 사망수/확진수, 감염율 = 확진수/인구 , 인구밀도 = 인구/ 면적
def pair_plt(str_x,num):
    df = data1.loc[:,['검사수율','확진수율', '사망수율', '감염율','인구밀도']]
    df = sort_data(df,str_x)
    df = weakn(df,num)
    
    g1= sns.pairplot(df, kind='reg',markers='o')
    


# In[10]:


# 4개 열 요소를 이용한 조인트함수
def joint_gr(str_x,sample_idx,x):
    
    df = data1[['검사수율', '사망수율', '감염율','인구밀도']]
    df.columns = ['Rate_Tst', 'Rate_Dth', 'Rate_Inf', 'Pop_den'] # 한글 폰트 깨짐 해결이 안됨;;;ㅠ
    sort_data(df,str_x)
    nums = random_nums(df,sample_idx)
    df = df.iloc[nums]
    df = weakn(df,x)

    sns.set_style('whitegrid')
    j1 = sns.jointplot(x='Rate_Tst', y='Rate_Dth',kind='reg', data=df)
    j2 = sns.jointplot(x='Pop_den', y='Rate_Inf',kind='reg', data=df)

    plt.show()


# In[11]:


def DCaseChart_group(x):
    df = data1[['사망수율','검사수율']]
    df = binning()
    df = groupin(df,x)
    df.columns = ['Death_Case','Case_Population','분할']
    df = sort_data(df,'Death_Case')

    plt.style.use('ggplot')
    plt.rcParams['axes.unicode_minus']=True
    ax1 = df['Case_Population'].plot(kind='bar',figsize = (20,10), stacked=False)
    ax2 = ax1.twinx()
    ax2.plot(df.index, df.Death_Case, ls ='--',marker='o',color = 'green')
    
    plt.show()


# In[12]:


# 이중차트 - x축을 col1 열을 기준으로 오름차순으로 정렬돤 col2(bar)와 col3(line)의 그래프를 생성하는 함수
def DCaseChart(col1, col2, col3, x):
    df = data1[[col1, col2, col3]]
    df.columns = [col1, col2, 'line']
    df = sort_data(df, col1)
    df = weakn(df,5)
    plt.style.use('ggplot')
    plt.rcParams['axes.unicode_minus']=True
    ax1 = df[col2].plot(kind='bar',figsize = (20,10), stacked=False)
    ax2 = ax1.twinx()
    ax2.plot(df.index, df.line, ls ='--',marker='o',color = 'green')
    
    plt.show()
    


# In[13]:


# 상관관계 히트맵 빨강/파랑 : 양/음의 상관관계
corr_heatmap()


# In[14]:


pair_plt('검사수율',3)
# 모든 요소가 세제곱근 배 적용된 그래프 -> 검사수율, 3 차례로 입력


# In[15]:


joint_gr('Rate_Tst',80,5)
# 'Rate_Tst'열을 기준으로 정렬 -> 80개 의 샘플 선택 -> 간격 축소 5


# In[16]:


DCaseChart('사망수율','검사수율','사망수율',5)


# In[17]:


DCaseChart_group('A')

# 자료상 


# In[18]:


DCaseChart_group('B')


# In[19]:


DCaseChart_group('C')


# In[ ]:





# In[ ]:





# In[ ]:





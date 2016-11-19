# _*_coding=utf-8_*_
import pandas as pd
all_ratings=pd.read_csv('ratings.dat',header=None,delimiter="::",engine='python',names=["userid","movieid","rating","timestap"])
all_ratings["timestap"]=pd.to_datetime(all_ratings["timestap"],unit='s')
print(all_ratings[:5])
#判断是否喜欢某一部电影
all_ratings["favorable"]=all_ratings["rating"]>3
print(all_ratings[1:10])
#提取前200名用户
rate_200=all_ratings[all_ratings['userid'].isin(range(200))]
# print(rate_200)
#下面的方法也可以筛选除前200名用户id
# print(all_ratings[all_ratings["userid"]<200])
#筛选出特定的打分
# rate_3=all_ratings[all_ratings["rating"].isin({3})]
# print(rate_3)
#得到用户喜欢的电影
favorable_rates=rate_200[rate_200["favorable"]]
# print(favorable_rates)
#按照USERID进行分类
favorable_rates_by_userid=dict((k,frozenset(v.values))
                               for k,v in favorable_rates.groupby("userid")["movieid"] )
#group(x)中其他的相加
num_favorable_by_movie=favorable_rates[["movieid","favorable"]].groupby("movieid").sum()
#按欢迎程度排序
print(num_favorable_by_movie.sort_values(by="favorable",ascending=False))
##Apriori算法
frequent_itemsets={}
min_support=50.0
#frozenset((movieid,))??????frozenset(v.values)
frequent_itemsets[1]=dict((frozenset((movieid,)),row["favorable"])
                          for movieid,row in num_favorable_by_movie.iterrows()
                          if row["favorable"] > min_support)
print(frequent_itemsets[1])
from collections import defaultdict
def find_frequent_itemsets(favorable_rates_by_userid,k_1_itemsets,min_support):
    counts=defaultdict(int)
    for userid,reviews in favorable_rates_by_userid.items():

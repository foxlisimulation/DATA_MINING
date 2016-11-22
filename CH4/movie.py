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
print(favorable_rates_by_userid)
# for k,v in favorable_rates_by_userid.items():
#     print(k,v)

# group(x)中其他的相加
num_favorable_by_movie=favorable_rates[["movieid","favorable"]].groupby("movieid").sum()
#按欢迎程度排序
print(num_favorable_by_movie.sort_values(by="favorable",ascending=False))
##Apriori算法
frequent_itemsets={}
min_support=50.0
#frozenset((movieid,))??????frozenset(v.values)
<<<<<<< HEAD
# frequent_itemsets[1]=dict((frozenset((movieid,)),row["favorable"])
#                           for movieid,row in num_favorable_by_movie.iterrows()
#                           if row["favorable"] > min_support)
frequent_itemsets[1]=dict((movieid,row["favorable"])
                          for movieid,row in num_favorable_by_movie.iterrows()
                          if row["favorable"] > min_support)
print(frequent_itemsets)
=======
#dict的键值为KEY,对应的为item,引用时A.items(),引用所有，若是A择则是引用键值
frequent_itemsets[1]=dict((frozenset((movieid,)),row["favorable"])
                          for movieid,row in num_favorable_by_movie.iterrows()
                          if row["favorable"] > min_support)
print(frequent_itemsets[1])
# for item in frequent_itemsets[1]:
#     print(item)

>>>>>>> origin/master
from collections import defaultdict

def find_frequent_itemsets(favorable_rates_by_userid,k_1_itemsets,min_support):
    counts=defaultdict(int)
    for userid,reviews in favorable_rates_by_userid.items():
        for itemset in k_1_itemsets:
            if itemset.issubset(reviews):
<<<<<<< HEAD
                for other_reviewed in reviews-itemset:
                    current_superset=itemset|frozenset((other_reviewed,))
                    counts[current_superset]+=1
    return dict([itemset,frequency] for itemset,frequency in counts.items() if frequency>min_support)
=======
                for other_reviews in reviews-itemset:
                    current_superset=itemset|frozenset((other_reviews,))
                    counts[current_superset]+=1
                    #计算在一个人的电影名单中同时出现的次数
    return dict([itemset,frequence] for itemset,frequence in counts.items() if frequence>=min_support)
import sys
for k in range(2,4):
    cur_frequent_itemset=find_frequent_itemsets(favorable_rates_by_userid,frequent_itemsets[k-1],min_support)
    frequent_itemsets[k]=cur_frequent_itemset
    print(cur_frequent_itemset,len(cur_frequent_itemset))
    if len(cur_frequent_itemset)==0:
        print("can't find any frequent itemset")
        sys.stdout.flush()
        break
    else:
        print("i find {} of length {}".format(len(cur_frequent_itemset),k))
        sys.stdout.flush()
del frequent_itemsets[1]
candidate_rules=[]
for itemset_lengeth,itemset_counts in frequent_itemsets.items():
    for items in itemset_counts.keys():
        for conclution in items:
            premise=items-set((conclution,))
            candidate_rules.append((premise,conclution))
print(candidate_rules[:1000])
#计算每条规则的置信度
correct_counts=defaultdict(int)
wrong_counts=defaultdict(int)
for userid,reviews in favorable_rates_by_userid.items():
    for candidate_rule in candidate_rules:
        premise,conclution=candidate_rule
        if premise.issubset(reviews):
            if conclution in reviews:
                correct_counts[candidate_rule]+=1
            else:
                wrong_counts[candidate_rule]+=1
rule_confidence={candidate_rule:correct_counts[candidate_rule]/float(correct_counts[candidate_rule]+wrong_counts[candidate_rule])
                 for candidate_rule in candidate_rules}
print(rule_confidence.items())
from operator import itemgetter
sorte_confidence=sorted(rule_confidence.items(),key=itemgetter(1),reverse=True)
print(sorte_confidence[:5])
# for index in range(5):
#电影名称与编号的映射
movie_names=pd.read_csv("movies.dat",delimiter="::",header=None)
movie_names.columns=["movieid","movie_names","movie_type"]
print(movie_names)
def get_movie_names(movieid):
    movie_name=movie_names[movie_names["movieid"]==movieid]["movie_names"]
    return  movie_name
print(get_movie_names(2571))
for index in range(5):
    print("rule{}".format(index))
    (premise,conclution)=sorte_confidence[index][0]
    print(id for id in premise)
    premise_names=" ".join(get_movie_names(id) for id in premise)
    conclution_name=get_movie_names(conclution)
    print("rule:if a person recomand {0},he weill also recomand {1},and the confidence "
          "is {3:.3f}".format(premise_names,conclution_name,rule_confidence[(premise,conclution)]))
>>>>>>> origin/master

#_*_coding:utf-8_*_
import pandas as pd
dataset=pd.read_csv('data.txt',parse_dates=["Date"])
dataset.columns=["Date","Startclock","Visitor_team","Visitor_pts","Home_team","Home_pts","Score_type","OT?","Notes"]
dataset["Homewin"]=dataset["Visitor_pts"]<dataset["Home_pts"]
# print(dataset)
y_true=dataset["Homewin"].values

from collections import defaultdict
won_last=defaultdict(int)
dataset["Homelastwin"]=False
dataset["Visitorlastwin"]=False
for index,row in dataset.iterrows():
    # print(index,row)
    home_team=row["Home_team"]
    visitor_team=row["Visitor_team"]
    row["Homelastwin"]=won_last[home_team]
    row["Visitorlastwin"]=won_last[visitor_team]
    dataset.ix[index]=row
    won_last[home_team] = row["Homewin"]
    won_last[visitor_team] = not row["Homewin"]

# print(dataset.ix[20:25])
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
clf=DecisionTreeClassifier(random_state=14)
x_prewin=dataset[["Homelastwin","Visitorlastwin"]].values
print(x_prewin)
scores=cross_val_score(clf,x_prewin,y_true,scoring="accuracy")
print(scores)
standing=pd.read_csv('data11.txt',encoding='gbk',header=1)
print(standing)
dataset["Hometeamrankshigher"]=0
for index,row in dataset.iterrows():
    home_team=row["Home_team"]
    visitor_team=row["Visitor_team"]
    if home_team=="New Orleans Pelicans":
        home_team="New Orleans Hornets"
    elif visitor_team=="New Orleans Pelicans":
        visitor_team="New Orleans Hornets"
    home_rank=standing[standing["Team"]==home_team]["Rk"].values[0]
    visitor_rank=standing[standing["Team"]==visitor_team]["Rk"].values[0]
    # print(home_rank,visitor_rank)
    row["Hometeamrankshigher"]=int(home_rank>visitor_rank)
    # print(row["Hometeamrankshigher"])
    dataset.ix[index]=row
x_homehigher=dataset[["Homelastwin","Visitorlastwin","Hometeamrankshigher"]].values
scores=cross_val_score(clf,x_homehigher,y_true,scoring="accuracy")
print(scores)
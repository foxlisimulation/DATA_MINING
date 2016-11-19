#_*_coding:utf-8_*_
import pandas as pd
import numpy as np

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
# print(scores)
standing=pd.read_csv('data11.txt',encoding='gbk',header=1)
# print(standing)
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
<<<<<<< HEAD
# scores=cross_val_score(clf,x_homehigher,y_true,scoring="accuracy")
# print(scores)
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
random_forest=RandomForestClassifier(random_state=14,n_jobs=4,oob_score=True,n_estimators=100)
scores1=cross_val_score(random_forest,x_homehigher,y_true,scoring="accuracy")
print(scores1)
parameter_space={"n_estimators":[100,],"criterion":["gini","entropy"],"min_samples_leaf":[2,4,6],}
clf2=RandomForestClassifier(random_state=14)
grid=GridSearchCV(clf2,parameter_space)
grid.fit(x_homehigher,y_true)
print(grid.best_score_)
print(grid.best_estimator_)
=======
scores=cross_val_score(clf,x_homehigher,y_true,scoring="accuracy")
print(scores)
last_match_winner=defaultdict(int)
dataset["hometeamlastwin"]=0
# print(dataset.ix[:2])
for index,row in dataset.iterrows():
    home_team=row["Home_team"]
    visitor_team=row["Visitor_team"]
    teams=tuple(sorted([home_team,visitor_team]))
    row["hometeamlastwin"]=1 if last_match_winner[teams]==row["Home_team"] else 0
    dataset.ix[index]=row
    # winner=row["Home_team"] if row["Homewin"] else row["Visitor_team"]
    # last_match_winner[teams]=winner
x_lastwinner=dataset[["Hometeamrankshigher","hometeamlastwin"]].values
scores1=cross_val_score(clf,x_lastwinner,y_true,scoring="accuracy")
print(scores1)
#将字符串类型的球队名转换为整型
from sklearn.preprocessing import LabelEncoder
encoding=LabelEncoder()
encoding.fit(dataset["Home_team"].values)
home_teams=encoding.transform(dataset["Home_team"].values)
visitor_teams=encoding.transform(dataset["Visitor_team"].values)
x_teams=np.vstack([home_teams,visitor_teams]).T
print(x_teams)
from sklearn.preprocessing import OneHotEncoder
onehot=OneHotEncoder()
x_team=onehot.fit_transform(x_teams).todense()
print(x_team)
score2=cross_val_score(clf,x_teams,y_true,scoring="accuracy")
print(score2)
>>>>>>> origin/master

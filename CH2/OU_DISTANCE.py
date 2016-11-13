#_*_coding:utf-8_*_#
import numpy as np
import csv
#预分配内存空间
x=np.zeros((351,34),dtype=float)
y=np.zeros((351,),dtype='bool')
with open('ionosphere.txt','r') as f:
    reader=csv.reader(f)
    for i,row in enumerate(reader):
        # print(row)
        #将数据分开
        data=[float(data1) for data1 in row[:-1]]
        x[i]=data
        y[i]=row[-1]=='g'
#将数据分为训练集和测试集
from sklearn.cross_validation import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=14)
#导入K临近分类器
from sklearn.neighbors import KNeighborsClassifier
n_neighbor=range(1,100,1)
all_soces=[]
averange_scores=[]
for n in n_neighbor:
   estimator=KNeighborsClassifier(n_neighbors=n)
# estimator.fit(x_train,y_train)
# y_predict=estimator.predict(x_test)
# print(y_predict==y_test)
# accurance=np.mean(y_test!=y_predict)
# print(accurance)
   from sklearn.cross_validation import cross_val_score
   scores=cross_val_score(estimator,x,y,scoring='accuracy')
   mean_accuracy=np.mean(scores)
   all_soces.append(scores)
   averange_scores.append(mean_accuracy)
   print(scores,mean_accuracy)
print(all_soces)
import matplotlib.pyplot as plt
plt.plot(n_neighbor,averange_scores)
x_broken=np.array(x)
# print(x_broken)
x_broken[:,::2]/=10
# print(x_broken)
estimator2=KNeighborsClassifier()
broken_socore=cross_val_score(estimator2,x_broken,y,scoring='accuracy')
print(broken_socore)
from sklearn.preprocessing import StandardScaler
x_transformed=StandardScaler().fit_transform(x_broken)
transformed_scores=cross_val_score(estimator2,x_transformed,y,scoring='accuracy')
print(transformed_scores)
from sklearn.pipeline import Pipeline
scaling_pipeline=Pipeline([('scale',StandardScaler()),('predict',KNeighborsClassifier())])
print(scaling_pipeline)
scores=cross_val_score(scaling_pipeline,x_broken,y,scoring='accuracy')
print(scores)
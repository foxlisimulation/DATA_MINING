# _*_coding:utf_8_*_#
from sklearn.datasets import load_iris
import numpy as np
dataset=load_iris()
x=dataset.data
y=dataset.target
Attribute_means=x.mean(axis=0)
x_d=np.array(x>=Attribute_means,dtype='int')
from sklearn.cross_validation import train_test_split
random_state=14
#random_state随机抽样的伪随机数生成器
x_train,x_test,y_train,y_test=train_test_split(x_d,y,random_state=10)
from collections import defaultdict
from operator import itemgetter
def train_feature_value(x,y_true,feature_index,value):
    class_counts=defaultdict(int)
    for sample,y in zip(x,y_true):
        print(sample,y)
        if sample[feature_index]==value:
            class_counts[y]+=1
    print(class_counts.items())
    sorted_class_counts=sorted(class_counts.items(),key=itemgetter(1),reverse=True)
    most_frequence_class=sorted_class_counts[0][0]
    incorrect_predictions=[class_count for class_value,class_count in class_counts.items()
                               if class_value!=most_frequence_class]
    print(incorrect_predictions)
    error=sum(incorrect_predictions)
    return most_frequence_class,error

def train(x,y_true,feature):
    n_samples,n_features=x.shape
    assert 0<=feature<n_features
    values=set(x[:,feature])
    print(values)
    predictors=dict()
    errors=[]
    for current_value in values:
        print(1)
        most_frequent_class,error=train_feature_value(x,y_true,feature,current_value)
        predictors[current_value]=most_frequent_class
        errors.append(error)
    total_error=sum(errors)
    return  predictors,total_error
all_predictors={variable:train(x_train,y_train,variable) for variable in range(x_train.shape[1])}
print(all_predictors)
errors={variable:error for variable,(mapping,error) in all_predictors.items()}
best_variable,best_error=sorted(errors.items(),key=itemgetter(1))[0]
print(best_error,best_variable)
print(x_train.shape[1])



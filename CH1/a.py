import numpy as np
dataset_filename="affinity_dataset.txt"
x=np.loadtxt(dataset_filename)
features = ["bread", "milk", "cheese", "apples", "bananas"]
print(x[:5])
num_apple=0
n_x,n_features=x.shape
print(n_features)
for sample in x:
    if sample[3]==1:
        num_apple+=1
print("there are:",num_apple,"apples")
from collections import  defaultdict
valid_rules=defaultdict(int)
invalid_rules=defaultdict(int)
num_occurance=defaultdict(int)
for sample in x:
    for n in range(n_features):
        if sample[n]==0: continue
        num_occurance[n]+=1
        for conclusion in range(n_features):
            if n==conclusion:continue
            if sample[conclusion]==1:
              valid_rules[(n,conclusion)]+=1
            else:
              invalid_rules[(n,conclusion)]+=1
support=valid_rules
# print(valid_rules)
confidence=defaultdict(float)
for n,conclusion in valid_rules.keys():
    rule=(n,conclusion)
    confidence[rule]=valid_rules[rule]/num_occurance[n]
def print_rule(n,conclusion,support,confidence,features):
    n_name=features[n]
    conclusion_name=features[conclusion]
    print("if a person buy {0} they will also buy {1}".format(n_name,conclusion_name))
    print("support:{0}".format(support[(n,conclusion)]))
    print("confidece:{0:0.3f}".format(confidence[(n,conclusion)]))
# for n in range(5):
#     for conclusion in range(5):
#         if n==conclusion:continue
#         print_rule(n,conclusion,support,confidence,features)

from operator import itemgetter
sorted_support=sorted(support.items(),key=itemgetter(1),reverse=True)
sorted_confidence=sorted(confidence.items(),key=itemgetter(1),reverse=True)
print(sorted_support[0][0])
for index in range(5):
    n,conclusion=sorted_confidence[index][0]
    print_rule(n, conclusion, support, confidence, features)

import soccer_ml_package.functions as smp
from Neural_Networks_Framework import Neural_Network
import random
import numpy as np
import csv

all_data = []
with open("./letter-recognition.csv","r") as datacsv:
    for line in datacsv:
        all_data.append(line[:-1].split(","))

#Για γράμματα Α και Π έχουμε συνολικά 1592 δεδομένα
my_letters = ['A','P']
# my_data_x = []
# for set in all_data:
#     if set[0] in my_letters:
#         floated_set = [set[0]]
#         for i in range(1,len(set)):
#             floated_set.append(float(set[i]))
#         my_data_x.append(floated_set)
#
# random.shuffle(my_data_x)
# a = 0
# p = 0
# for set in my_data_x:
#     if set[0] == 'P':
#         p+=1
#     else:
#         a+=1
# print("A: ",a,"\nP: ",p)
# input()
#
# my_data_y = []
# for i,set in enumerate(my_data_x):
#     y = [0]*len(my_letters)
#     pos = my_letters.index(set[0])
#     y[pos] = 1
#     my_data_y.append(y)
#     my_data_x[i].pop(0)


data_x = []
with open("./letters_x.csv","r") as datacsv:
    for line in datacsv:
        data_x.append(line[:-1].split(","))

data_y = []
with open("./letters_y.csv","r") as datacsv:
    for line in datacsv:
        data_y.append(line[:-1].split(","))

my_data_x = []
for list in data_x:
    my_data_x.append([int(float(item)) for item in list])

my_data_y = []
for list in data_y:
    my_data_y.append([int(float(item)) for item in list])


k = 10
training_sets,testing_sets = smp.k_fold_cross_validation(my_data_x,k)
training_outputs,testing_outputs = smp.k_fold_cross_validation(my_data_y,k)

input_features = len(my_data_x[0]) #16
learning_rate = 0.02
epochs = 10
batch_size = 60
scores = []

all_nets = []
for fold in range(k):
    print("\n\nExamining Fold : ",fold+1,"/",k," for ",epochs," epochs, with batch size:",batch_size)
    net = Neural_Network(input_features,[10,4,2],learning_rate)
    net.train(training_sets[fold],training_outputs[fold],epochs,batch_size)
    net.test(testing_sets[fold],testing_outputs[fold])
    all_nets.append(net)
    score = net.get_Eval()
    print("\nClassifier's Accuracy: ",score,"%")
    scores.append(score)
    best_fold = scores.index(max(scores))

print("\nThe most accurate prediction came from fold ",best_fold+1," with prediction accuracy: ",scores[best_fold],"%")

print("\nSo we will use the neural network which was trained by fold: ",best_fold+1,"\n")

print("LETTER GIVEN =====> PREDICTION\n")
correctly_classified = 0
for i,observed in enumerate(testing_outputs[best_fold]):
    predicted = all_nets[best_fold].feed_forward_result(testing_sets[best_fold][i])
    observed_pos = observed.index(max(observed))
    predicted_pos = predicted.index(max(predicted))
    if(observed_pos == predicted_pos):
        correctly_classified += 1
        print("\t",my_letters[observed_pos],"  =====> ",my_letters[predicted_pos]," | CORRECT!!")
    else:
        print("\t",my_letters[observed_pos],"  =====> ",my_letters[predicted_pos]," | FALSEE:((")

print("\n",correctly_classified,"/",len(testing_outputs[best_fold])," of cases where classified correctly.")

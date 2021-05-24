import soccer_ml_package.functions as smp
from Neural_Networks_Framework import Neural_Network
import random
import numpy as np

all_data = []
with open("./letter-recognition.csv","r") as datacsv:
    for line in datacsv:
        all_data.append(line[:-1].split(","))

#Για γράμματα Α και Π έχουμε συνολικά 1592 δεδομένα
my_letters = ['A','P']

#Ο παρακάτω κώδικας μπορεί να χρησιμοποιηθεί αν δεν διαβάσουμε τελικα
#τα αρχεία letters_x και letters_y. Τα letters_x και letters_y δημιουργήθηκαν
#προκειμένου να ΄έχουμε πάντα τα ΄ίδια δεδομένα με την ίδια σειρά.

#Αν δεν θέλουμε να χρησιμοποιήσουμε τα letters_x και letters_y, δηλαδή κάθε φορά
#που θα τρέχει το πρόγραμμα οι πίνακες my_data_x και my_data_y θα έχουν διαφορετική μορφή,
#αρκεί να κάνουμε σχόλια τις γραμμές 43-61 και να βγάλουμε απο σχόλια τις γραμμές 24-40.
#Αν επιλέξουμε να το κάνουμε αυτό, μας δίνεται η δυνατότητα να ψάξουμε όποια γράμματα θέλουμε
#απλά βάζοντας τa στον πίνακα my_letters παραπάνω

# my_data_x = []
# for set in all_data:
#     if set[0] in my_letters:
#         floated_set = [set[0]]
#         for i in range(1,len(set)):
#             floated_set.append(float(set[i]))
#         my_data_x.append(floated_set)
#
# random.shuffle(my_data_x)
#
# my_data_y = []
# for i,set in enumerate(my_data_x):
#     y = [0]*len(my_letters)
#     pos = my_letters.index(set[0])
#     y[pos] = 1
#     my_data_y.append(y)
#     my_data_x[i].pop(0)

# #Διαβάζουμε το csv με τα features
data_x = []
with open("./letters_x.csv","r") as datacsv:
    for line in datacsv:
        data_x.append(line[:-1].split(","))

# #Διαβάζουμε το csv με τα αποτελέσματα των αντίστοιχων features
data_y = []
with open("./letters_y.csv","r") as datacsv:
    for line in datacsv:
        data_y.append(line[:-1].split(","))

#Μετατρέπουμε όλα τα στοιχεία του πίνακα data_x σε float
my_data_x = []
for list in data_x:
    my_data_x.append([int(float(item)) for item in list])

#Μετατρέπουμε όλα τα στοιχεία του πίνακα data_y σε float
my_data_y = []
for list in data_y:
    my_data_y.append([int(float(item)) for item in list])


#Επιλέγουμε το κ και καλούμε την συνάρτηση k_fold_cross_validation προκειμένου
#να μας χωρίσει το dataset στα αντίστοιχα δεδομ΄΄ενα
k = 10
training_sets,testing_sets = smp.k_fold_cross_validation(my_data_x,k)
training_outputs,testing_outputs = smp.k_fold_cross_validation(my_data_y,k)

#Θέτουμε τις βασικές παραμέτρους του νευρωνικύ δικτύου
input_features = len(my_data_x[0]) #16
output = len(my_letters)
learning_rate = 0.02
epochs = 10
batch_size = 40
scores = []

#Εκτελούμε τα νευρωνικά δίκτυα για όλα τα folds
all_nets = []
for fold in range(k):
    print("\n\nExamining Fold : ",fold+1,"/",k," for ",epochs," epochs, with batch size:",batch_size)
    net = Neural_Network(input_features,[10,4,output],learning_rate)
    net.train(training_sets[fold],training_outputs[fold],epochs,batch_size)
    net.test(testing_sets[fold],testing_outputs[fold])
    all_nets.append(net)
    score = net.get_Eval()
    print("\nClassifier's Accuracy: ",score,"%")
    scores.append(score)
    best_fold = scores.index(max(scores))

print("\nThe most accurate prediction came from fold ",best_fold+1," with prediction accuracy: ",scores[best_fold],"%")

print("\nSo we will use the neural network which was trained by fold: ",best_fold+1,"\n")


#Τυπώνουμε τα γράμματα τα οποία δώσαμε και την πρόβλεψη την οποία έκανα ο classifier μας.
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

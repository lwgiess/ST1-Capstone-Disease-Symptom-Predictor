import sklearn
from sklearn.utils import shuffle
from sklearn import datasets
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style
from sklearn import svm
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing

# Load libraries
import numpy
from matplotlib import pyplot as plt
from pandas import read_csv
from pandas import set_option
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

# Data file import
symptom_data = pd.read_csv("Disease_symptom_and_patient_profile_dataset.csv")

# Calculate the frequency of each unique value in the "Disease" column
disease_frequency = symptom_data['Disease'].value_counts()

# Identify values with frequency >= 10
valid_diseases = disease_frequency[disease_frequency >= 10].index.tolist()

# Filter the DataFrame based on valid diseases
filtered_df = symptom_data[symptom_data['Disease'].isin(valid_diseases)]

# Attribute to be predicted
predict = "Outcome Variable"

# Dataset/Column to be Predicted, X is all attributes and y is the features
#x = np.array(symptom_data.drop([predict], 1)) # Will return a new data frame that doesnt have outcome variable in it
#y = np.array(symptom_data[predict])
le = preprocessing.LabelEncoder()
Disease = le.fit_transform(list(filtered_df["Disease"])) # Disease (Asthma, Stroke, Osteoporosis, Hypertension, Diabetes, Migraine)
Fever = le.fit_transform(list(filtered_df["Fever"])) # Fever (1 = yes; 0 = no)
Cough = le.fit_transform(list(filtered_df["Cough"])) # Coughing (1 = yes; 0 = no)
Fatigue = le.fit_transform(list(filtered_df["Fatigue"])) # Fatigue (1 = yes; 0 = no)
Difficulty_Breathing = le.fit_transform(list(filtered_df["Difficulty Breathing"])) # Difficulty Breathing (1 = yes; 0 = no)
Age = le.fit_transform(list(filtered_df["Age"]))  # Age in years
Gender = le.fit_transform(list(filtered_df["Gender"]))  # Gender (1 = male; 0 = female)
Blood_Pressure = le.fit_transform(list(filtered_df["Blood Pressure"]))  # Blood Pressure
Cholesterol_Level = le.fit_transform(list(filtered_df["Cholesterol Level"]))  # Cholesterol Level
Outcome_Variable = le.fit_transform(list(filtered_df["Outcome Variable"]))  # Outcome Variable


x = list(zip(Disease, Fever, Cough, Fatigue, Difficulty_Breathing, Age, Gender, Blood_Pressure, Cholesterol_Level))
y = list(Outcome_Variable)
# Test options and evaluation metric
num_folds = 5
seed = 7
scoring = 'accuracy'

# Model Test/Train
# Splitting what we are trying to predict into 4 different arrays -
# X train is a section of the x array(attributes) and vise versa for Y(features)
# The test data will test the accuracy of the model created
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.20, random_state=seed)
#splitting 20% of our data into test samples. If we train the model with higher data it already has seen that information and knows

# Check with  different Scikit-learn classification algorithms
models = []
models.append(('DT', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
models.append(('GBM', GradientBoostingClassifier()))
models.append(('RF', RandomForestClassifier()))
# evaluate each model in turn
results = []
names = []

for name, model in models:
	kfold = KFold(n_splits=num_folds,shuffle=True,random_state=seed)
	cv_results = cross_val_score(model, x_train, y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	msg += '\n'
	print(msg)

# Compare Algorithms' Performance
fig = pyplot.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
pyplot.boxplot(results)
ax.set_xticklabels(names)
pyplot.show()


# Make predictions on validation/test dataset
dt = DecisionTreeClassifier()
nb = GaussianNB()
gb = GradientBoostingClassifier()
rf = RandomForestClassifier()

best_model = gb
best_model.fit(x_train, y_train)
y_pred = best_model.predict(x_test)
model_accuracy = accuracy_score(y_test, y_pred)
print("Best Model Accuracy Score on Test Set:", model_accuracy)

#Model Evaluation Metric 1
print(classification_report(y_test, y_pred))

#Model Evaluation Metric 2
#Confusion matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()

#Model Evaluation Metric 3
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

best_model = gb
best_model.fit(x_train, y_train)
rf_roc_auc = roc_auc_score(y_test,best_model.predict(x_test))
fpr,tpr,thresholds = roc_curve(y_test, best_model.predict_proba(x_test)[:,1])

plt.figure()
plt.plot(fpr,tpr,label = 'GradientBoostingClassifier(area = %0.2f)'% rf_roc_auc)
plt.plot([0,1],[0,1],'r--')
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.05])
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc='lower right')
plt.savefig('LOC_ROC')
plt.show()

#Check actual/ground truth vs predicted diagnosis
for x in range(len(y_pred)):
	print("Predicted: ", y_pred[x], "Actual: ", y_test[x], "Data: ", x_test[x],)


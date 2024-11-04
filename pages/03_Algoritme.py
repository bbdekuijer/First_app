import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Laad de dataset
data_path = "Data/Raw/train.csv"
data = pd.read_csv(data_path)

# Voorbereiden van de gegevens
data = data.dropna(subset=['Age', 'Embarked'])  # Voorbeeld van gegevens schoonmaken
X = data[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare']]
X['Sex'] = X['Sex'].map({'male': 0, 'female': 1})  # Convert to numerical
y = data['Survived']

# Split de dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Beslissingsboom model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Model nauwkeurigheid
accuracy = accuracy_score(y_test, y_pred)
st.title("Algoritme")
st.write("Model nauwkeurigheid: {:.2f}%".format(accuracy * 100))

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

st.title("Machine Learning Algoritme")

# Voorbereiden van data
X = data.drop('Survived', axis=1)  # kenmerken
y = data['Survived']                # doelvariabele

# Dataverwerking: bijvoorbeeld one-hot encoding
X = pd.get_dummies(X, drop_first=True)

# Splitsen van de dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Trainen van het model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Voorspellingen doen
y_pred = model.predict(X_test)

# Nauwkeurigheid tonen
accuracy = accuracy_score(y_test, y_pred)
st.write(f"Nauwkeurigheid van het model: {accuracy:.2f}")

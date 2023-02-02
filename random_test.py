import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Prepare a labeled dataset
data = [
    ("open youtube", "open youtube"),
    ("open website", "open website"),
    ("date and time", "date and time"),
    ("talk like a friend", "talk like a friend"),
    ("define", "define"),
    ("calculate", "calculate"),
    ("quit", "quit"),
    ("play music", "play music")
]

df = pd.DataFrame(data, columns=["text", "label"])

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Build a pipeline to vectorize the text inputs and train a classifier
pipe = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', SVC(kernel='linear'))
])

pipe.fit(X_train, y_train)

# Make predictions on the test set
y_pred = pipe.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

def predict_command(text_input):
    return pipe.predict([text_input])[0]

# Accept input from the user
text_input = input("Enter a command: ")

# Display the predicted output
print("Predicted Output:", predict_command(text_input))

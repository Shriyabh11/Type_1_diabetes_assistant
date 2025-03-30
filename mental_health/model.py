import pandas as pd
import numpy as np
import random
import nltk
import joblib
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import wordnet
from transformers import BertTokenizer, BertModel

# Load dataset
df = pd.read_csv("diabetes_mood_dataset.csv")  
print(f"Dataset size: {df.shape}")

# Download NLTK resources if not already available
nltk.download("punkt")
nltk.download("wordnet")

# Initialize BERT tokenizer & model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertModel.from_pretrained("bert-base-uncased")

# Function to extract BERT embeddings
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()  # Mean pooling
    return embeddings

# Data Augmentation (Synonym Replacement)
def synonym_replace(text, n=1):
    words = nltk.word_tokenize(text)
    new_words = words[:]
    for _ in range(n):
        word = random.choice(words)
        synonyms = wordnet.synsets(word)
        if synonyms:
            synonym = synonyms[0].lemmas()[0].name()
            new_words = [synonym if w == word else w for w in new_words]
    return " ".join(new_words)

# Apply augmentation to dataset (50% chance per sample)
df["text_aug"] = df["text"].apply(lambda x: synonym_replace(x) if random.random() > 0.5 else x)

# Convert text to BERT embeddings
df["embedding"] = df["text_aug"].apply(get_bert_embedding)
X = np.vstack(df["embedding"])  # Stack embeddings into 2D array

# Encode labels
encoder = LabelEncoder()
df["sentiment_encoded"] = encoder.fit_transform(df["sentiment"])  
y = df["sentiment_encoded"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train logistic regression model
clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(X_train, y_train)

# Predictions & Evaluation
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy:.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save model & encoder for future use
joblib.dump(clf, "sentiment_model.pkl")
joblib.dump(encoder, "label_encoder.pkl")


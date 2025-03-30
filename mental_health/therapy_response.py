import joblib
import torch
from transformers import BertTokenizer,BertModel
import openai

# Load trained sentiment model & encoder
clf = joblib.load("sentiment_model.pkl")
encoder = joblib.load("label_encoder.pkl")

# Load BERT tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# OpenAI API Key (set your own key)
openai.api_key = "your_openai_api_key"
bert_model = BertModel.from_pretrained("bert-base-uncased")

# Function to get BERT embedding
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings

# Function to classify sentiment
def get_sentiment(text):
    embedding = get_bert_embedding(text).reshape(1, -1)  # Reshape for prediction
    sentiment_id = clf.predict(embedding)[0]  # Get the predicted label index
    sentiment_label = encoder.inverse_transform([sentiment_id])[0]  # Convert back to label
    return sentiment_label
def send_to_openai(query):
    sentiment = get_sentiment(query)

    # Customize prompt based on sentiment
    if sentiment == "positive":
        prompt = f"The user is feeling positive. Provide an uplifting response to: {query}"
    elif sentiment == "negative":
        prompt = f"The user is feeling down. Provide a supportive and empathetic response to: {query}"
    else:
        prompt = f"The user is neutral. Provide a straightforward response to: {query}"

    # Send to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4 or GPT-3.5
        messages=[{"role": "system", "content": "You are a helpful AI therapist."},
                  {"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# Example Usage
user_query = "I feel really stressed today."
response = send_to_openai(user_query)
print(response)



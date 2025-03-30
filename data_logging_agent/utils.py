from firebase_config import db
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
#from sentiment_model import analyze_mood
import json
import pandas as pd
from datetime import datetime

openai_model = ChatOpenAI(model_name="gpt-4", temperature=0)
embeddings = OpenAIEmbeddings()
vector_db = FAISS.load_local("user_logs_db", embeddings)

# 🏷 Step 1: Extract Structured Data (Carbs, BG, Exercise, Mood, Periods)
def extract_health_data(user_input):
    messages = [
        SystemMessage(content="Extract health data (carbs, BG, exercise, periods, mood) from logs."),
        HumanMessage(content=f"Log entry: {user_input}\n\nFormat: {{'carbs': '', 'blood_glucose': '', 'exercise': '', 'mood': '', 'period_status': ''}}")
    ]
    response = openai_model(messages)
    structured_data = json.loads(response.content)

    # 🌟 Sentiment Analysis for Mood Detection
    if structured_data["mood"]:
        structured_data["mood"] = analyze_mood(structured_data["mood"])

    return structured_data

# 📥 Step 2: Store Log in Firebase
def store_log(user_id, log_text):
    structured_data = extract_health_data(log_text)
    structured_data["timestamp"] = datetime.now().isoformat()

    db.collection("user_logs").document(user_id).collection("logs").add(structured_data)

    # Store in Vector DB for Retrieval
    vector_db.add_texts([log_text], [structured_data])
    vector_db.save_local("user_logs_db")

    return "Log stored successfully."

# 📊 Step 3: Trend Analysis (BG, Mood, Exercise)
def analyze_trends(user_id):
    logs_ref = db.collection("user_logs").document(user_id).collection("logs").stream()
    logs = [log.to_dict() for log in logs_ref]

    df = pd.DataFrame(logs)

    feedback = []

    # Blood Glucose Trend
    if "blood_glucose" in df:
        df["blood_glucose"] = pd.to_numeric(df["blood_glucose"], errors="coerce")
        if df["blood_glucose"].mean() > 180:
            feedback.append("Your BG levels are consistently high. Consider reviewing your carb intake.")

    # Mood Trend
    if "mood" in df:
        mood_counts = df["mood"].value_counts()
        if "Stressed" in mood_counts and mood_counts["Stressed"] > 3:
            feedback.append("You’ve been feeling stressed for a few days. Want relaxation tips?")

    # Exercise Trend
    if "exercise" in df:
        df["exercise"] = df["exercise"].fillna("No").apply(lambda x: "Yes" if x.lower() != "no" else "No")
        if (df["exercise"] == "No").sum() > 3:
            feedback.append("You've skipped exercise for 3+ days. A short walk could help!")

    return feedback if feedback else ["No major issues detected!"]

# 🔍 Step 4: Query Past Logs
def query_logs(user_query):
    results = vector_db.similarity_search(user_query, k=3)
    logs = [r.page_content for r in results]

    summary_prompt = f"Summarize these logs: {logs}"
    return openai_model([HumanMessage(content=summary_prompt)]).content

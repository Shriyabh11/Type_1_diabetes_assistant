import os
import openai
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY", "your_openai_api_key")  # Replace with actual key

# Step 1: Setup LLM (Mistral with HuggingFace)
HF_TOKEN = os.getenv("HF_TOKEN", "hf_mytoken")  # Replace with actual token

HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

def load_llm(huggingface_repo_id, token):
    return HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        model_kwargs={"max_length": 512},
        token=token
    )

# Step 2: Define Custom Prompt
CUSTOM_PROMPT_TEMPLATE = """
Use the provided context to answer the user's question.
If you don’t know the answer, just say you don’t know. Don't make up an answer.
Provide answers only based on the given context. Simplify responses to be more user-friendly.

Context: {context}
Question: {question}

Start the answer directly. No small talk.
"""

def set_custom_prompt(template):
    return PromptTemplate(template=template, input_variables=["context", "question"])

# Step 3: Load FAISS Database
DB_FAISS_PATH = r"C:\Users\shriy\Documents\Personal projects\T1D_ASSISTANT\memory\faiss_db"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

try:
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={'k': 3})  # Retrieve top 3 matches
except Exception as e:
    print(f"Error loading FAISS database: {e}")
    retriever = None  # No FAISS fallback

# Step 4: Create QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=load_llm(HUGGINGFACE_REPO_ID, HF_TOKEN),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={'prompt': set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
)

# OpenAI Fallback Function
def query_openai(query):
    print("\n⚠️ FAISS retrieval failed. Using OpenAI as fallback.\n")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing diabetes-related answers."},
            {"role": "user", "content": query}
        ]
    )
    return response["choices"][0]["message"]["content"]

# Step 5: Run a Predefined Query for Testing
test_query = "How often should I change my insulin pump site?"  # Predefined test query
print(f"\n🔹 TESTING WITH QUERY: {test_query}")

response = qa_chain.invoke({"query": test_query})

# Handle FAISS response & fallback
if "result" in response and response["result"].strip():
    final_answer = response["result"]
    print("\n✅ FAISS Response:", final_answer)
else:
    final_answer = query_openai(test_query)
    print("\n✅ OpenAI Fallback Response:", final_answer)

import time
import streamlit as st
import psycopg2
import ollama
from datetime import datetime

# Initialize the Ollama client
client = ollama.Client()

# Database connection setup
conn = psycopg2.connect(
    dbname="queries_db",
    user="testuser",
    password="test1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Function to get a response from Ollama
def get_response_from_ollama(query, model_name):
    start_time = time.time()  # Start the timer
    response = client.generate(prompt=query, model=model_name)
    end_time = time.time()  # End the timer
    response_time = end_time - start_time  # Calculate time taken
    return response.get('response', 'No response available'), response_time

def store_query_and_response(query, response, model_name, response_time):
    cursor.execute(
        "INSERT INTO query_response (query, response, model_name, response_time) VALUES (%s, %s, %s, %s)",
        (query, response, model_name, response_time)
    )
    conn.commit()

# Streamlit UI
st.title("Chat with LLM - Model Testing")

# Dropdown for model selection
model_name = st.selectbox(
    "Select a model to use:",
    (
        "muhammad-albasha/llama3.1-python",
        "ALIENTELLIGENCE/pythonconsultant",
        "geradeluxer/llama3.1-q4-python"
    )
)

query = st.text_input("Enter your query:", "")
if st.button("Send"):
    if query:
        response, response_time = get_response_from_ollama(query, model_name)
        st.write(f"Response: {response}")
        st.write(f"Time Taken: {response_time:.2f} seconds")
        store_query_and_response(query, response, model_name, response_time)

# Display chat history
st.subheader("Chat History")
cursor.execute("SELECT query, response, model_name, response_time, created_at FROM query_response ORDER BY created_at DESC")
rows = cursor.fetchall()
for row in rows:
    response_time_display = f"{row[3]:.2f} seconds" if row[3] is not None else "N/A"
    st.write(f"{row[4]} - Model: {row[2]} - You: {row[0]}")
    st.write(f"Model Response: {row[1]}")
    st.write(f"Time Taken: {response_time_display}")
    st.write("---")


cursor.close()
conn.close()

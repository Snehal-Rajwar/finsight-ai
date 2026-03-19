from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Try environment variable first, then Streamlit secrets
try:
    import streamlit as st
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
except:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def get_ai_insight(transactions_summary, anomalies_summary, user_question):
    """
    Sends data to Groq's Llama model for plain-English insights.
    """
    system_prompt = """You are a friendly personal finance assistant.
You receive transaction history and anomaly flags.
Respond in plain, clear English. Be specific with dollar amounts.
Keep answers under 4 sentences unless asked for more detail.
Be helpful and actionable, not alarmist."""

    user_prompt = f"""
Transactions:
{transactions_summary}

Unusual charges flagged:
{anomalies_summary}

User question: {user_question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content
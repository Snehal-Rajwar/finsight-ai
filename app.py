import streamlit as st
import pandas as pd
from anomaly import detect_anomalies
from ai_chat import get_ai_insight

st.set_page_config(page_title="FinSight AI", page_icon="💸", layout="centered")
st.title("💸 FinSight AI")
st.caption("Upload your transactions. I'll flag unusual spending and answer your questions.")
st.divider()

uploaded = st.file_uploader(
    "Upload your transactions CSV",
    type=["csv"],
    help="CSV needs columns: date, description, amount, category"
)

if uploaded is not None:
    df = pd.read_csv(uploaded)
    
    st.subheader("📊 Your Transactions")
    st.dataframe(df, use_container_width=True)
    
    anomalies = detect_anomalies(df)
    
    st.subheader("🚨 Unusual Charges")
    if not anomalies.empty:
        st.warning(f"{len(anomalies)} unusually large transaction(s) detected:")
        st.dataframe(
            anomalies[['date', 'description', 'amount', 'category']],
            use_container_width=True
        )
    else:
        st.success("No anomalies found — spending looks consistent.")
    
    st.subheader("🤖 Ask me anything")
    st.caption('Try: "Why were these flagged?" or "Where am I overspending?"')
    
    question = st.text_input("Your question:")
    if question:
        tx_str = df.to_string(index=False)
        an_str = anomalies.to_string(index=False) if not anomalies.empty else "None"
        
        with st.spinner("Thinking..."):
            answer = get_ai_insight(tx_str, an_str, question)
        st.info(f"**FinSight:** {answer}")



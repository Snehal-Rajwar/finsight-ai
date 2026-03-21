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
    
# Auto-Analysis (Agentic Feature #1)
    st.subheader("📊 Automatic Insights")
    
    total_spending = df['amount'].abs().sum()
    category_totals = df.groupby('category')['amount'].apply(lambda x: x.abs().sum()).sort_values(ascending=False)
    top_3_charges = df.nlargest(3, 'amount', keep='first')[['date', 'description', 'amount', 'category']]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Spending", f"${total_spending:,.2f}")
    with col2:
        top_category = category_totals.index[0]
        st.metric("Top Category", f"{top_category} (${category_totals.iloc[0]:,.2f})")
    
    st.write("**Top 3 Largest Charges:**")
    st.dataframe(top_3_charges, use_container_width=True, hide_index=True)
    
    # Anomaly Detection
    st.subheader("🚨 Unusual Charges Detected")
    anomalies = detect_anomalies(df)
    
    if not anomalies.empty:
        st.warning(f"{len(anomalies)} unusually large transaction(s) flagged:")
        st.dataframe(
            anomalies[['date', 'description', 'amount', 'category']],
            use_container_width=True,
            hide_index=True
        )
        
        # Proactive Suggestions (Agentic Feature #2)
        st.subheader("💡 Proactive Recommendations")
        
        suggestions = []
        
        # Suggestion 1: Category spending comparison
        if len(category_totals) >= 2:
            top_cat = category_totals.index[0]
            top_amt = category_totals.iloc[0]
            second_cat = category_totals.index[1]
            second_amt = category_totals.iloc[1]
            pct_diff = ((top_amt - second_amt) / second_amt * 100)
            if pct_diff > 20:
                suggestions.append(f"💰 You spent ${top_amt:.2f} on {top_cat}, {pct_diff:.0f}% more than {second_cat}. Consider whether this aligns with your budget priorities.")
        
        # Suggestion 2: Anomaly review
        largest_anomaly = anomalies.nlargest(1, 'amount').iloc[0]
        avg_in_category = df[df['category'] == largest_anomaly['category']]['amount'].abs().mean()
        multiplier = largest_anomaly['amount'] / avg_in_category
        suggestions.append(f"🔍 Your ${abs(largest_anomaly['amount']):.2f} {largest_anomaly['category']} charge ({largest_anomaly['description']}) is {multiplier:.1f}x your average {largest_anomaly['category']} spending. Verify this transaction is legitimate.")
        
        # Suggestion 3: Budget alert
        if total_spending > 2000:
            suggestions.append(f"⚠️ Total spending this period: ${total_spending:.2f}. Consider setting up budget alerts to track high-spend months.")
        
        for suggestion in suggestions:
            st.info(suggestion)
        
    else:
        st.success("✅ No anomalies found — spending looks consistent across categories.")
    
    st.subheader("🤖 Ask me anything")
    st.caption('Try: "Why were these flagged?" or "Where am I overspending?"')
    
    question = st.text_input("Your question:")
    if question:
        tx_str = df.to_string(index=False)
        an_str = anomalies.to_string(index=False) if not anomalies.empty else "None"
        
        with st.spinner("Thinking..."):
            answer = get_ai_insight(tx_str, an_str, question)
        st.info(f"**FinSight:** {answer}")



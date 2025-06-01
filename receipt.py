# receipt.py
import streamlit as st
from datetime import datetime

def generate_receipt(username, candidate):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    receipt_text = f"""
    -------------------------------
             Voting Receipt         
    -------------------------------
    🧑 Voter: {username}
    🗳️ Voted For: {candidate['party']} ({candidate['candidate']})
    🪧 Symbol: {candidate['symbol']}
    🕒 Time: {timestamp}
    -------------------------------
    """

    st.markdown("### 🧾 Voting Receipt")
    st.code(receipt_text.strip(), language='text')

    # Save to file with correct name
    receipt_path = f"receipt_{username}.txt"
    with open(receipt_path, 'w', encoding='utf-8') as f:
        f.write(receipt_text)

    with open(receipt_path, "rb") as f:
        st.download_button("📥 Download Receipt", f, file_name=receipt_path)

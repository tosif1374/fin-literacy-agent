# streamlit_app.py

import streamlit as st

from app.retriever import retrieve, contains_pii_request
from app.llm import generate_answer
from app.translate import (
    detect_language,
    to_english,
    from_english,
)

st.set_page_config(
    page_title="Digital Financial Literacy Agent",
    page_icon="💰",
)

SCAM_SAFETY_MESSAGE = """
Never share OTPs, UPI PINs, CVV numbers, passwords, or bank account credentials.
If you suspect fraud, contact your bank immediately and report the incident to the National Cyber Crime Portal.
"""

st.title("💰 Digital Financial Literacy Agent")
st.caption(
    "Ask about UPI, scams, interest rates, or budgeting — in your language."
)

query = st.text_input("Your question")

if st.button("Ask") and query:

    with st.spinner("Thinking..."):

        try:
            lang = detect_language(query)

            if contains_pii_request(query):
                st.warning(SCAM_SAFETY_MESSAGE)
                st.stop()

            question_en = to_english(query, lang)

            results = retrieve(question_en)

            context_chunks = [doc for doc, _ in results]

            answer_en = generate_answer(
                question_en,
                context_chunks
            )

            answer = from_english(
                answer_en,
                lang
            )

            st.success("Response received")

            st.markdown("### Answer")
            st.write(answer)

            if results:
                st.markdown("### Sources")

                for _, meta in results:
                    source = meta.get("source", "Unknown")
                    url = meta.get("url", "#")

                    st.markdown(
                        f"- [{source}]({url})"
                    )

        except Exception as e:
            st.error(f"Error: {str(e)}")
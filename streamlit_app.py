# ui/streamlit_app.py

import streamlit as st
import requests

st.set_page_config(
    page_title="Digital Financial Literacy Agent",
    page_icon="💰"
)

st.title("💰 Digital Financial Literacy Agent")
st.caption(
    "Ask about UPI, scams, interest rates, or budgeting — in your language."
)

query = st.text_input("Your question")

if st.button("Ask") and query:
    with st.spinner("Thinking..."):

        try:
            response = requests.post(
                "http://localhost:8000/ask",
                json={"question": query},
                timeout=120
            )

            st.write("Status Code:", response.status_code)

            if response.status_code != 200:
                st.error("API Error")
                st.code(response.text)
            else:
                resp = response.json()

                st.success("Response received")

                st.write("### Answer")
                st.write(resp.get("answer", "No answer returned"))

                if resp.get("sources"):
                    st.markdown("### Sources")
                    for s in resp["sources"]:
                        st.markdown(
                            f"- [{s['source']}]({s['url']})"
                        )

        except Exception as e:
            st.error(f"Request failed: {str(e)}")
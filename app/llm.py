# app/llm.py
import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()

credentials = Credentials(
    url=os.getenv("WATSONX_URL"),
    api_key=os.getenv("WATSONX_API_KEY"),
)

model = ModelInference(
    model_id="ibm/granite-4-h-small",   # check watsonx console for the latest available Granite model id
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    params={"decoding_method": "greedy", "max_new_tokens": 400, "temperature": 0.2},
)

SYSTEM_PROMPT = """You are a financial literacy assistant for Indian users.
Answer ONLY using the provided context. If the context does not contain the answer, say so.
Never give personalized investment advice. Never ask for OTP, PIN, card number, or Aadhaar number.
Always end with: "This is general educational information, not professional financial advice."
"""

def generate_answer(query: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    response = model.generate_text(prompt=prompt)
    return response
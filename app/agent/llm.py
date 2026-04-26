from app.core.config import settings
from groq import Groq
from app.core.exceptions import ServiceException

try:
    client = Groq(api_key=settings.GENAI_API_KEY)
except Exception as e:
    client = None

def generate_response(context: str, user_query: str) -> str:
    if not client:
        raise ServiceException("LLM", "Groq client failed to initialize or missing API key.")
    
    try:
        # Prompt engineering
        system_prompt = """You are a helpful AI assistant.
Use ONLY the provided context to answer the question.
If the answer is not in the context, say "I don't know based on the provided information."
Be concise and accurate."""

        user_prompt = f"""
Context:
{context}

Question:
{user_query}

Answer:
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2  # keeps it grounded
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        raise ServiceException("LLM", f"Failed to generate response: {str(e)}")

if __name__ == "__main__":
    print(generate_response("What is the capital of France?"))
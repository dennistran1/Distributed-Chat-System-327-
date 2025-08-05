import openai
import os
from dotenv import load_dotenv

# Load API key from .env file or environment variable
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def handle_llm_request(prompt):
    if not openai.api_key:
        return "[LLM Error] OpenAI API key not found."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for distributed systems."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        return f"[LLM Bot]: {reply}"

    except Exception as e:
        return f"[LLM Error] {str(e)}"

# Example usage
if __name__ == '__main__':
    question = input("Ask the LLM: ")
    print(handle_llm_request(question))

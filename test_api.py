import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ API key was not found.")
    exit()

print("✅ API key was found.")

client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model="gpt-5-mini",
        input="Say hello in one short sentence."
    )

    print("AI response:")
    print(response.output_text)

except Exception as e:
    print("❌ API request failed:")
    print(e)
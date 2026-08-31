import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def main():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ API key was not found.")
        return 1

    print("✅ API key was found.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input="Say hello in one short sentence."
        )
    except Exception as error:
        print("❌ API request failed:")
        print(error)
        return 1

    print("AI response:")
    print(response.output_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())

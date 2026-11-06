
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")
else:
    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": "Explain data analysis in two simple sentences."
                }
            ],
            temperature=0.5,
        )

        print("Groq API connected successfully!")
        print(response.choices[0].message.content)

    except Exception as e:
        print("Groq API error:", e)

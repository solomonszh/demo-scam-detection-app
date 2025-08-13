import os
import random
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

SEA_LION_API_KEY = os.getenv("SEA_LION_API_KEY", None)
client = OpenAI(
    api_key=SEA_LION_API_KEY,
    base_url="https://api.sea-lion.ai/v1",
)

def generate_random_result(chat: dict):
    answers = ["🚨 scam", "✅ not scam"]
    return random.sample(answers, k=1)[0]

def generate_result(chat: dict):
    completion = client.chat.completions.create(
        model="aisingapore/Llama-SEA-LION-v3-70B-IT",
        messages=[
            {
                "role": "assistant",
                "content": "You are a highly skilled scam detection bot. "
                    "Your job is to analyze chat transcripts and label them as either a 'scam' or 'Not a Scam'. "
                    "For each verdict, you must provide a bulleted list of the reasons for your conclusion."
            
                    "\n\nHere are a few examples:"
                    "\nExample 1 (Not a Scam):"
                    "\nTranscript: Hey, do you want to grab coffee later?"
                    "\nVerdict: Not a Scam"
                    "\nReasons:"
                    "\n- No requests for money or personal information."
                    "\n- The conversation is casual and typical of friendly exchanges."

                    "\n\nExample 2 (Scam):"
                    "\nTranscript: I'm a prince from a foreign country. "
                        "I need you to send me $1000 so I can unlock my inheritance. "
                        "I will send you $1,000,000 when I arrive."
                    "\nVerdict: Scam"
                    "\nReasons:"
                    "\n- The sender is making an outrageous claim."
                    "\n- The sender is asking for a large sum of money with a promise of an even larger, unbelievable return."
                    "\n- The sender is creating a sense of urgency and emotional appeal."
            },
            {
                "role": "user",
                "content": f"Please analyze the following chat history:\n {chat}"
            }
        ]
    )

    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content
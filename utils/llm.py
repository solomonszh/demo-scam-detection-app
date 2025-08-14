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
                    
                    "\n\nCRITICAL FORMATTING REQUIREMENT:"
                    "\nYou MUST format your response with 'Reasons:' on a separate line. Do NOT put 'Reasons:' on the same line as the verdict."
                    
                    "\nCorrect format:"
                    "\nVerdict: [Scam or Not a Scam]"
                    "\nReasons:"
                    "\n* [First reason]"
                    "\n* [Second reason]"
                    
                    "\nINCORRECT format (DO NOT USE):"
                    "\nVerdict: Scam Reasons:"
                    
                    "\n\nHere are examples with the EXACT format you must follow:"
                    "\nExample 1:"
                    "\nVerdict: Not a Scam"
                    "\nReasons:"
                    "\n* No requests for money or personal information."
                    "\n* The conversation is casual and typical of friendly exchanges."

                    "\n\nExample 2:"
                    "\nVerdict: Scam"
                    "\nReasons:"
                    "\n* The sender is making an outrageous claim."
                    "\n* The sender is asking for a large sum of money with a promise of an even larger, unbelievable return."
                    "\n* The sender is creating a sense of urgency and emotional appeal."
                    
                    "\n\nREMEMBER: 'Reasons:' must be on its own line, never on the same line as the verdict!"
            },
            {
                "role": "user",
                "content": f"Please analyze the following chat history:\n {chat}"
            }
        ]
    )

    result = completion.choices[0].message.content
    
    # Simple post-processing to fix formatting issues
    import re
    
    # Only fix if "Verdict:" and "Reasons:" are on the same line
    # Pattern: "Verdict: Something Reasons:" -> "Verdict: Something\nReasons:"
    result = re.sub(r'(Verdict:\s*[^\n]+?)\s+Reasons:', r'\1\nReasons:', result)
    
    # For Streamlit display, ensure line breaks are preserved
    # Convert newlines to double newlines for markdown
    result = result.replace('\n', '\n\n')
    
    return result
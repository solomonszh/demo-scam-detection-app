import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.prompt import get_prompt_by_country

# Load environment variables from .env file
load_dotenv()

def generate_result(chat: dict, country: str, sea_lion_api_key: str) -> str:
    prompt_country = get_prompt_by_country(chat=chat, country=country)

    client = OpenAI(
        api_key=sea_lion_api_key,
        base_url="https://api.sea-lion.ai/v1",
    )
    completion = client.chat.completions.create(
        model="aisingapore/Llama-SEA-LION-v3-70B-IT",
        messages=prompt_country
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
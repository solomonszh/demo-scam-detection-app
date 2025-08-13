import random

def generate_result(chat: dict):
    answers = ["🚨 scam", "✅ not scam"]
    return random.sample(answers, k=1)[0]

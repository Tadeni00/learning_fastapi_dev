from pyexpat.errors import messages
from urllib import response
from openai import OpenAI, api_key
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("API_KEY")
client = Together(api_key=api_key)

text = "Machine learning is a field of artificial intelligence that enables computers to learn from data and make predictions."

prompt = f"""Explain the key concept of the text delimited by triple backticks in simpple terms. ```{text}```"""

sys_prompt = "You are a machine learning expert who explains concepts in simple terms."

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages= [
        {
            "role": "user",
            "content": prompt
        },
        {
            "role": "system",
            "content": "Explain the key concept of the text delimited by triple backticks in simple terms. The explanation should be concise and easy to understand."
        },
        {
            "role": "assistant",
            "content": sys_prompt
        }
    ]
)

print(response.choices[0].message.content) # type: ignore
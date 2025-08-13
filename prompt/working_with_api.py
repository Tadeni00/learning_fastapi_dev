from urllib import response
from openai import OpenAI, api_key
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("API_KEY")
client = Together(api_key=api_key)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=[
        {
            "role": "user",
            "content": "What are some fun things in Abeokuta?"
        },
        {
            "role": "system",
            "content": "You are a helpful assistant that provides information about places and activities in Abeokuta that are budget friendly."
            "The prices should be in Nigerian Naira (NGN) and should not exceed 5000 NGN."
        },
        {
            "role": "assistant",
            "content": "You are a travel expert"
        }
    ]
)

print(response.choices[0].message.content) # type: ignore
from pyexpat.errors import messages
from urllib import response
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("API_KEY")
client = Together(api_key=api_key)

text = "Artificial intelligence is transforming industries like healthcare, finance, and" \
" transportation by enabling machines to perform tasks that typically require human intelligence."

prompt = f"""Format the response in a  list:
-- List the key benefits of artificial intelligence in various industries.
-- Provide examples of how AI is being used in healthcare, finance, and transportation.
-- Use bullet points for clarity.
```{text}```"""

sys_prompt = "You are a machine learning expert who explains concepts in simple terms."
assistant_content = "You are a helpful assistant that provides information about the benefits of artificial intelligence in various industries."

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages= [
        {
            "role": "user",
            "content": prompt
        },
        {
            "role": "system",
            "content": sys_prompt
        },
        {
            "role": "assistant",
            "content": assistant_content
        }
    ]
)

print(response.choices[0].message.content) # type: ignore
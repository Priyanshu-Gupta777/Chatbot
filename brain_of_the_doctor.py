#step1 --> setup api key
import os
from dotenv import load_dotenv


load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
#print(GROQ_API_KEY)
#step2 --> converting image to required format
import base64

#image_path = "acne.jpg"
def encoded_image(image_path):
   image_file = open(image_path, 'rb')
   return base64.b64encode(image_file.read()).decode('utf-8')

#step3 --> setup multimodal LLM.

from groq import Groq

model="llama-3.2-11b-vision-preview"
query = "Is there something wrong with my face?"

def analyze_user_problem(query, encoded_image, model):

   client = Groq()

   message = [
    {
        "role" : "user",
        "content" : [
            {
                "type" : "text",
                "text" : query,
            },
            {
                "type" : "image_url",
                "image_url" : {
                    "url" : f'data:image/jpeg;base64,{encoded_image}',
                },
            },
        ],
    }
   ]


   completion = client.chat.completions.create(
    model=model,
    messages=message,
   )

   return completion.choices[0].message.content
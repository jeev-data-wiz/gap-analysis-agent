from openai import OpenAI
import numpy as np
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()  # <-- THIS WAS MISSING

print("Key loaded:", bool(os.getenv("GROQ_API_KEY")))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print([m.id for m in client.models.list().data])

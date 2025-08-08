from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()
model = ChatGroq(model='meta-llama/llama-4-scout-17b-16e-instruct')

print(model.invoke('what can you do'))
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph

from prompt import SYSTEM_PROMPT, REVIEW_PROMPT
from state import State, Response

load_dotenv()
model = ChatGroq(model='meta-llama/llama-4-scout-17b-16e-instruct')


def optimize_prompt(state: State):
    prompt = SYSTEM_PROMPT.format(input_prompt=state['input_prompt'])
    resp = model.with_structured_output(Response).invoke(prompt)
    return {'output_prompt': resp.optimized_prompt}

def review_prompt(state: State):
    prompt = REVIEW_PROMPT.format(prompt=state['input_prompt'])
    resp = model.invoke(prompt)
    return {'comments': resp.content}

builder = StateGraph(State)
builder.add_sequence([optimize_prompt, review_prompt])
builder.set_entry_point('optimize_prompt')
graph = builder.compile()


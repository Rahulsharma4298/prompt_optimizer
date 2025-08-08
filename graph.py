from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph

from prompt import SYSTEM_PROMPT, REVIEW_PROMPT, OPTIMIZE_BY_REVIEW_PROMPT
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

def optimize_prompt_by_review(state: State):
    prompt = OPTIMIZE_BY_REVIEW_PROMPT.format(prompt=state['input_prompt'],
                                              review_comments=state['comments'])
    resp = model.with_structured_output(Response).invoke(prompt)
    return {'output_prompt': resp.optimized_prompt}


builder = StateGraph(State)
builder.add_sequence([review_prompt, optimize_prompt_by_review])
builder.set_entry_point('review_prompt')
graph = builder.compile()


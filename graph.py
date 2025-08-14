from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langgraph.types import Send

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
    # print(resp)
    return {'comments': resp.content, 'iterations': state['iterations']-1}

def optimize_prompt_by_review(state: State):
    prompt = OPTIMIZE_BY_REVIEW_PROMPT.format(prompt=state['input_prompt'],
                                              review_comments=state['comments'])
    resp = model.with_structured_output(Response).invoke(prompt)
    print(state.get('output_prompt'))
    return {'output_prompt': resp.optimized_prompt}

def check_iteration(state: State):
    print("Inside conditional check")
    print(state['iterations'])
    if state['iterations'] > 0:
        return 'review_prompt'
    else:
        return END


builder = StateGraph(State)
builder.add_node('review_prompt', review_prompt)
builder.add_node('optimize_prompt_by_review', optimize_prompt_by_review)

builder.add_edge('review_prompt', 'optimize_prompt_by_review')
builder.add_conditional_edges('optimize_prompt_by_review', check_iteration)

builder.set_entry_point('review_prompt')

graph = builder.compile()


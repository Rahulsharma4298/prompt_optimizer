from pydantic import BaseModel
from typing_extensions import TypedDict


class State(TypedDict):
    input_prompt: str
    output_prompt: str
    comments: str

class Response(BaseModel):
    optimized_prompt: str

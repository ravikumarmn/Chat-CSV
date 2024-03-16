from llama_index.llms.openai import OpenAI

# Local imports
from .constants import *
from .log import logger

def init_model(model: str = DEFAULT_OPENAI_MODEL):
    logger.info("Model LLM set to {}".format(model))    
    llm = OpenAI(
        model=model,
        temperature=DEFAULT_TEMPERATURE,
        
    )
    return llm



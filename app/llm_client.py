from openai import OpenAI
import os
import random
from fastapi import Depends
from dotenv import load_dotenv


load_dotenv(override=True)

# Initialize OpenAI client with API key and base URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") 
LLM_MODEL = os.getenv("LLM_MODEL")
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

def generate(system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
    """
    Generate text using OpenAI's chat completions API.
    
    Args:
        system_prompt (str): Initial prompt that sets the behavior and context for the AI
        user_prompt (str): The actual input/question to be processed by the AI
        json_mode (bool, optional): If True, forces response to be valid JSON. Defaults to False.
        
    Returns:
        str: The generated text response from the AI model. If json_mode is True, 
             returns a valid JSON string.
    """
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"} if json_mode else None
    )
    return response.choices[0].message.content




def mock_generate(system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
    """
    Mock implementation of the generate function.
    
    Args:
        system_prompt (str): Initial prompt that sets the behavior and context for the AI
        user_prompt (str): The actual input/question to be processed by the AI
        json_mode (bool, optional): If True, forces response to be valid JSON. Defaults to False.
        
    Returns:
        str: The generated text response from the AI model. If json_mode is True, 
             returns a valid JSON string.
    """
    # check if the user prompt contains any of the types of analysis and return the response accordingly
    if "summary" in user_prompt:
        return "This is a summary of the text"
    elif "sentiment" in user_prompt:
        return '{"positive": 0.74, "negative": 0, "neutral": 0.26, "dominant": "positive"}'
    elif "keywords" in user_prompt:
        return '{"keywords": [{"keyword": "keyword1", "relevance": 0.74}, {"keyword": "keyword2", "relevance": 0.26}]}'
    elif "entities" in user_prompt:
        return '{"entities": [{"text": "entity1", "type": "entity1", "confidence": 0.74}, {"text": "entity2", "type": "entity2", "confidence": 0.26}]}'
    elif "classification" in user_prompt:
        return '{"classifications": [{"classification": "classification1", "confidence": 0.74}, {"classification": "classification2", "confidence": 0.26}]}'
    else:
        return "This is a mock response"




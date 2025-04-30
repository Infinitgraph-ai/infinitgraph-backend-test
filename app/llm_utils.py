"""
LLM utilities for Infinitgraph.ai Backend Developer Technical Test.

This file contains functions related to LLM processing that need to be implemented
by the candidate. For simplicity, you can use a mock implementation that returns
realistic-looking responses instead of actually calling an LLM API.

Key tasks:
1. Create a function to analyze text based on the analysis type
2. Implement proper error handling
3. Format responses according to the defined models
"""

from typing import Dict, List, Optional, Any
import datetime
import random
import json
import os

import google.generativeai as genai

from app.models import (
    AnalysisType,
    TextAnalysisResult,
    SentimentResult,
    KeywordResult,
    EntityResult
)

# Set up Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')


def analyze_text(text: str, analysis_type: AnalysisType) -> TextAnalysisResult:
    """
    Analyze text using LLM techniques based on the specified analysis type.
    
    For this test, you can implement mock responses that simulate LLM outputs.
    However, your implementation should demonstrate how you would structure this
    for a real LLM integration (error handling, response parsing, etc.)
    
    In a real-world scenario, this would call an external API like OpenAI.
    
    Args:
        text: The text to analyze
        analysis_type: Type of analysis to perform
        
    Returns:
        TextAnalysisResult object with analysis results
        
    Raises:
        ValueError: If text is empty or analysis type is invalid
        RuntimeError: If the mock LLM processing fails
    """
    if not text:
        raise ValueError("Text input cannot be empty")
    
    if analysis_type not in AnalysisType:
        raise ValueError(f"Invalid analysis type: {analysis_type}")
    
    summary = None
    sentiment = None
    keywords = None
    entities = None
    classification = None
    
    # Mock LLM processing
    match analysis_type:
        case AnalysisType.SUMMARY:
            result = _generate_summary(text)
            summary = result
        case AnalysisType.SENTIMENT:
            result = _analyze_sentiment(text)
            sentiment = result
        case AnalysisType.KEYWORDS:
            result = _extract_keywords(text)
            keywords = result
        case AnalysisType.ENTITIES:
            result = _extract_entities(text)
            entities = result
        case AnalysisType.CLASSIFICATION:
            result = _classify_text(text)
            classification = result
        case _:
            raise ValueError(f"Unsupported analysis type: {analysis_type}")

    # Format response
    response = TextAnalysisResult(
        analysis_type=analysis_type,
        summary=summary,
        sentiment=sentiment,
        keywords=keywords,
        entities=entities,
        classification=classification,
        timestamp=datetime.datetime.now().isoformat()
    )

    return response

def _generate_summary(text: str) -> str:
    prompt = f"Summarize the following text:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

def _analyze_sentiment(text: str) -> SentimentResult:
    prompt = (
        "Analyze the sentiment of the following text.\n"
        "Respond ONLY with a raw JSON object (no markdown, no backticks, no explanation).\n"
        "Format:\n"
        '{ "positive": float (0 to 1), "negative": float (0 to 1), "neutral": float (0 to 1), "dominant": "positive" | "neutral" | "negative" }\n\n'
        "Do not use any surrounding formatting. Do not return a list. Do not wrap the response in triple quotes or backticks.\n"
        f"{text}"
    )
    response = model.generate_content(prompt)
    try:
        parsed = eval(response.text.strip())
        return SentimentResult(
            positive=parsed["positive"],
            negative=parsed["negative"],
            neutral=parsed["neutral"],
            dominant=parsed["dominant"]
        )
    except Exception:
        raise RuntimeError("Failed to parse sentiment response")

def _extract_keywords(text: str) -> List[KeywordResult]:
    prompt = (
        "Extract up to 5 important keywords from the following text.\n"
        "Respond **only** with a raw JSON array (no markdown, no backticks, no explanation).\n"
        "Do not use any surrounding formatting. Do not return a list. Do not wrap the response in triple quotes or backticks.\n"
        "Format: [{\"keyword\": \"example\", \"relevance\": 0.85}, ...]\n\n"
        f"{text}"
    )
    response = model.generate_content(prompt)
    try:
        parsed = json.loads(response.text.strip())
        return [KeywordResult(keyword=k["keyword"], relevance=k["relevance"]) for k in parsed]
    except Exception:
        raise RuntimeError("Failed to parse keywords response")

def _extract_entities(text: str) -> List[EntityResult]:
    prompt = (
        "Extract entities from the following text.\n"
        "Respond **only** with a raw JSON array (no markdown, no backticks, no explanation).\n"
        "Do not use any surrounding formatting. Do not return a list. Do not wrap the response in triple quotes or backticks.\n"
        "Format: [{\"text\": \"example\", \"type\": \"example\", \"confidence\": 0.85}, ...]\n\n"
        f"{text}"
    )
    response = model.generate_content(prompt)
    try:
        parsed = eval(response.text.strip())
        return [EntityResult(text=e["text"], type=e["type"], confidence=e["confidence"]) for e in parsed]
    except Exception:
        raise RuntimeError("Failed to parse entities response")

def _classify_text(text: str) -> Dict[str, float]:
    prompt = (
        "Classify the following text into categories.\n"
        "Respond with **only** a raw JSON object (no Markdown, no triple backticks, no arrays, no explanation).\n"
        "Do not use any surrounding formatting. Do not return a list. Do not wrap the response in triple quotes or backticks.\n"
        "Return format example: {\"category1\": 0.85, \"category2\": 0.75}\n"
        "IMPORTANT: Output must be a single valid JSON object, not a list of objects.\n\n"
        f"{text}"
    )
    response = model.generate_content(prompt)
    try:
        print(response.text.strip())
        return eval(response.text.strip())
    except Exception as e:
        raise RuntimeError(f"Failed to parse classification response: {str(e)}")
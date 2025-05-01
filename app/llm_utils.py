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

import app.llm_client as llm_client
from typing import Callable
from app.models import (
    AnalysisType,
    TextAnalysisResult,
    SentimentResult,
    KeywordResult,
    EntityResult,
    ClassificationResult
)

# TODO: Implement analyze_text function
def analyze_text(text: str, analysis_type: AnalysisType, llm_function: Callable) -> TextAnalysisResult:
    """
    Analyze text using LLM techniques based on the specified analysis type.
    
    For this test, you can implement mock responses that simulate LLM outputs.
    However, your implementation should demonstrate how you would structure this
    for a real LLM integration (error handling, response parsing, etc.)
    
    In a real-world scenario, this would call an external API like OpenAI.
    
    Args:
        text: The text to analyze
        analysis_type: Type of analysis to perform
        llm_function: The LLM function to use

    Returns:
        TextAnalysisResult object with analysis results
        
    Raises:
        ValueError: If text is empty or analysis type is invalid
        RuntimeError: If the mock LLM processing fails
    """
    # TODO: Implement text analysis based on analysis_type
    # 1. Validate input
    if not text:
        raise ValueError("Text cannot be empty")
    if analysis_type not in AnalysisType:
        raise ValueError(f"Invalid analysis type: {analysis_type}")
    # Additional validation for the text can be made such as token count based on the used model.
    # 2. Perform analysis based on type 
    analysis_functions = {
        AnalysisType.SUMMARY: _generate_summary,
        AnalysisType.SENTIMENT: _analyze_sentiment, 
        AnalysisType.KEYWORDS: _extract_keywords,
        AnalysisType.ENTITIES: _extract_entities,
        AnalysisType.CLASSIFICATION: _classify_text
    }

    # Get the appropriate analysis function
    analysis_func = analysis_functions.get(analysis_type)

    # Execute the analysis
    result = analysis_func(text, llm_function)

    # 3. Format response according to TextAnalysisResult model
    return TextAnalysisResult(
        **result,
        processed_at=datetime.datetime.now()
    )


# TODO: Implement helper functions for each analysis type
def _generate_summary(text: str, llm_function: Callable) -> str:
    """
    Generate a summary of the text.
    
    Args:
        text: The text to summarize
        llm_function: The LLM function to use
    Returns:
        A summary of the text
    """
    # TODO: Implement summary generation 
    system_prompt = f"Generate a summary of the following text"
    user_prompt = f"Text: {text}"
    summary = llm_function(system_prompt=system_prompt, user_prompt=user_prompt)
    return {
        "summary": summary,
        "analysis_type" : AnalysisType.SUMMARY
    }


def _analyze_sentiment(text: str, llm_function: Callable) -> SentimentResult:
    """
    Analyze the sentiment of the text.
    
    Args:
        text: The text to analyze
        
    Returns:
        SentimentResult object with sentiment scores
    """
    # TODO: Implement sentiment analysis 
    system_prompt = """Analyze the sentiment of the following text and return the sentiment scores in a JSON format in the following format: 
        {{'positive': 0.0, 'negative': 0.0, 'neutral': 0.0, 'dominant': 'neutral'}}.
        The dominant sentiment should be the one with the highest score.
        Do not include any other text in your response or markdown formatting.
        Just return the JSON object.        
    """
    user_prompt = f"Text: {text}"
    result = llm_function(system_prompt=system_prompt, user_prompt=user_prompt ,json_mode=True)
    result = json.loads(result)
    # Create a SentimentResult object with the parsed values
    sentiment_result = SentimentResult(
        positive=result.get('positive'),
        negative=result.get('negative'),
        neutral=result.get('neutral'),
        dominant=result.get('dominant')
    )
    return {
        "sentiment": sentiment_result,
        "analysis_type" : AnalysisType.SENTIMENT
    }


def _extract_keywords(text: str, llm_function: Callable) -> List[KeywordResult]:
    """
    Extract keywords from the text.
    
    Args:
        text: The text to analyze
        
    Returns:
        List of KeywordResult objects
    """
    # TODO: Implement keyword extraction 
    system_prompt = """Extract keywords from the following text and return them in a JSON format in the following format: 
        [{{'keyword': 'keyword1', 'relevance': 0.0}}, {{'keyword': 'keyword2', 'relevance': 0.0}}, {{'keyword': 'keyword3', 'relevance': 0.0}}]
        Do not include any other text in your response or markdown formatting.
        Just return the JSON object.
    """
    user_prompt = f"Text: {text}"
    result = llm_function(system_prompt=system_prompt, user_prompt=user_prompt ,json_mode=True)
    result = json.loads(result)
    print(result)
    keyword_results = [
        KeywordResult(
            keyword=keyword['keyword'],
            relevance=keyword['relevance']
        )
        for keyword in result.get('keywords')
    ]
    return{
        "keywords": keyword_results,
        "analysis_type" : AnalysisType.KEYWORDS
    }


def _extract_entities(text: str, llm_function: Callable) -> List[EntityResult]:
    """
    Extract entities from the text.
    
    Args:
        text: The text to analyze
        
    Returns:
        List of EntityResult objects
    """
    # TODO: Implement entity extraction 
    system_prompt = """Extract entities from the following text and return them in a JSON format in the following format: 
        [{{'text': 'entity1', 'type': 'type1', 'confidence': 0.0}}, {{'text': 'entity2', 'type': 'type2', 'confidence': 0.0}}, {{'text': 'entity3', 'type': 'type3', 'confidence': 0.0}}]
        Do not include any other text in your response or markdown formatting.
        Just return the JSON object.
    """
    user_prompt = f"Text: {text}"
    result = llm_function(system_prompt=system_prompt, user_prompt=user_prompt ,json_mode=True)
    result = json.loads(result)
    entity_results = [
        EntityResult(
            text=entity['text'],
            type=entity['type'],
            confidence=entity['confidence']
        )
        for entity in result.get('entities')
    ]
    return{
        "entities": entity_results,
        "analysis_type" : AnalysisType.ENTITIES
    }


def _classify_text(text: str, llm_function: Callable) -> Dict[str, float]:
    """
    Classify the text into categories.
    
    Args:
        text: The text to classify
        
    Returns:
        Dictionary mapping category names to confidence scores
    """
    # TODO: Implement text classification 
    system_prompt = """Classify the following text into categories and return the category in a JSON format in the following format: 
        {'classifications': [{'classification': 'category1', 'confidence': 0.0}, {'classification': 'category2', 'confidence': 0.0}, {'classification': 'category3', 'confidence': 0.0}]}
        Do not include any other text in your response or markdown formatting.
        Just return the JSON object.
    """
    user_prompt = f"Text: {text}"
    result = llm_function(system_prompt=system_prompt, user_prompt=user_prompt ,json_mode=True)
    result = json.loads(result)
    classification_results = [
        ClassificationResult(
            classification=c['classification'],
            confidence=c['confidence']
        )
        for c in result.get('classifications', [])
    ]
    return {
        "classification": classification_results,
        "analysis_type" : AnalysisType.CLASSIFICATION
    }
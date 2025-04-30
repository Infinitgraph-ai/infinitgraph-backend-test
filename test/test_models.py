"""
Tests for the Pydantic models in the Infinitgraph.ai application.
"""

import pytest
from pydantic import ValidationError
import datetime

from app.models import (
    TextInput,
    TextAnalysisResult,
    SentimentResult,
    KeywordResult,
    EntityResult,
    AnalysisType
)


def test_text_input_validation():
    """Test validation rules for TextInput model"""
    # Valid input
    valid_input = TextInput(text="This is a test text that is longer than 10 characters.")
    assert valid_input.text == "This is a test text that is longer than 10 characters."
    assert valid_input.analysis_type == AnalysisType.SUMMARY
    
    # Test min length validation
    with pytest.raises(ValidationError):
        TextInput(text="Too short")
        
    # Test empty text validation
    with pytest.raises(ValidationError):
        TextInput(text="   ")

def test_sentiment_result_validation():
    """Test validation rules for SentimentResult model"""
    # Valid sentiment
    valid_sentiment = SentimentResult(positive=0.7, negative=0.1, neutral=0.2, dominant="positive")
    assert valid_sentiment.positive == 0.7
    assert valid_sentiment.dominant == "positive"
    
    # Test score range validation
    with pytest.raises(ValidationError):
        SentimentResult(positive=1.2, negative=0.1, neutral=0.2, dominant="positive")
        
    # Test negative values
    with pytest.raises(ValidationError):
        SentimentResult(positive=-0.1, negative=0.1, neutral=0.2, dominant="negative")
        

def test_text_analysis_result_validation():
    """Test validation rules for TextAnalysisResult model"""
    # Test summary analysis
    summary_result = TextAnalysisResult(
        analysis_type=AnalysisType.SUMMARY,
        summary="This is a summary of the text."
    )
    assert summary_result.analysis_type == AnalysisType.SUMMARY
    assert summary_result.summary == "This is a summary of the text."
    
    # Test sentiment analysis
    sentiment_result = TextAnalysisResult(
        analysis_type=AnalysisType.SENTIMENT,
        sentiment=SentimentResult(positive=0.6, negative=0.2, neutral=0.2, dominant="positive")
    )
    assert sentiment_result.analysis_type == AnalysisType.SENTIMENT
    assert sentiment_result.sentiment.dominant == "positive"
    
    # Test validation for missing required field based on analysis type
    with pytest.raises(ValueError):
        TextAnalysisResult(
            analysis_type=AnalysisType.SUMMARY,
            summary=None
        )
        
    # Test keywords analysis
    keywords_result = TextAnalysisResult(
        analysis_type=AnalysisType.KEYWORDS,
        keywords=[
            KeywordResult(keyword="test", relevance=0.9),
            KeywordResult(keyword="example", relevance=0.8)
        ]
    )
    assert keywords_result.analysis_type == AnalysisType.KEYWORDS
    assert len(keywords_result.keywords) == 2
    assert keywords_result.keywords[0].keyword == "test"


def test_keyword_result_validation():
    """Test validation rules for KeywordResult model"""
    # Valid keyword result
    valid_keyword = KeywordResult(keyword="example", relevance=0.9)
    assert valid_keyword.keyword == "example"
    assert valid_keyword.relevance == 0.9

    # Test relevance out of range
    with pytest.raises(ValidationError):
        KeywordResult(keyword="example", relevance=1.1)

    with pytest.raises(ValidationError):
        KeywordResult(keyword="example", relevance=-0.1)

def test_entity_result_validation():
    """Test validation rules for EntityResult model"""
    # Valid entity result
    valid_entity = EntityResult(text="example", type="organization", confidence=0.85)
    assert valid_entity.text == "example"
    assert valid_entity.type == "organization"
    assert valid_entity.confidence == 0.85

    # Test confidence out of range
    with pytest.raises(ValidationError):
        EntityResult(text="example", type="organization", confidence=1.1)

    with pytest.raises(ValidationError):
        EntityResult(text="example", type="organization", confidence=-0.1)
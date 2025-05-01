"""
Pydantic models for the Infinitgraph.ai technical test.
These models define the data structures used throughout the application.
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional, Dict, Any
from enum import Enum
import datetime

class AnalysisType(str, Enum):
    """Types of text analysis that can be performed"""
    SUMMARY = "summary"
    SENTIMENT = "sentiment"
    KEYWORDS = "keywords"
    ENTITIES = "entities"
    CLASSIFICATION = "classification"
    

class TokenResponse(BaseModel):
    """JWT token response model"""
    access_token: str
    token_type: str


class UserRole(str, Enum):
    """User roles for authorization"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class TextInput(BaseModel):
    """Input model for text analysis"""
    text: str = Field(..., min_length=10, max_length=10000)
    analysis_type: AnalysisType = Field(default=AnalysisType.SUMMARY)
    options: Optional[Dict[str, Any]] = Field(default=None)
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or only whitespace')
        return v


class SentimentResult(BaseModel):
    """Result model for sentiment analysis"""
    positive: float = Field(..., ge=0.0, le=1.0)
    negative: float = Field(..., ge=0.0, le=1.0)
    neutral: float = Field(..., ge=0.0, le=1.0)
    dominant: str


class KeywordResult(BaseModel):
    """Result model for keyword extraction"""
    keyword: str
    relevance: float = Field(..., ge=0.0, le=1.0)


class EntityResult(BaseModel):
    """Result model for entity recognition"""
    text: str
    type: str
    confidence: float = Field(..., ge=0.0, le=1.0)

class ClassificationResult(BaseModel):
    """Result model for text classification"""
    classification: str
    confidence: float = Field(..., ge=0.0, le=1.0)

class TextAnalysisResult(BaseModel):
    """Result model for text analysis"""
    analysis_type: AnalysisType
    summary: Optional[str] = None
    sentiment: Optional[SentimentResult] = None
    keywords: Optional[List[KeywordResult]] = None
    entities: Optional[List[EntityResult]] = None
    classification: Optional[List[ClassificationResult]] = None
    processed_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    @validator('*')
    def ensure_result_for_type(cls, v, values):
        if 'analysis_type' in values:
            analysis_type = values['analysis_type']
            if analysis_type == AnalysisType.SUMMARY and 'summary' in values and not values['summary']:
                raise ValueError('Summary analysis requires summary field')
            if analysis_type == AnalysisType.SENTIMENT and 'sentiment' in values and not values['sentiment']:
                raise ValueError('Sentiment analysis requires sentiment field')
            if analysis_type == AnalysisType.KEYWORDS and 'keywords' in values and not values['keywords']:
                raise ValueError('Keyword analysis requires keywords field')
            if analysis_type == AnalysisType.ENTITIES and 'entities' in values and not values['entities']:
                raise ValueError('Entity analysis requires entities field')
            if analysis_type == AnalysisType.CLASSIFICATION and 'classification' in values and not values['classification']:
                raise ValueError('Classification analysis requires classification field')
        return v


class UserOut(BaseModel):
    """User model for API responses"""
    id: int = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    role: UserRole = Field(...)
    is_active: bool = Field(...)
    created_at: datetime.datetime = Field(...)


class AnalysisHistoryOut(BaseModel):
    """Analysis history model for API responses"""
    id: Optional[int] = Field(default=None)
    user_id: int = Field(...)
    text_sample: str = Field(...)
    analysis_type: AnalysisType = Field(...)
    status: str = Field(...)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

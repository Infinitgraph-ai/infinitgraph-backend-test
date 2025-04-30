from fastapi import FastAPI, Depends, HTTPException, Header, Body, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from fastapi_pagination import Page, add_pagination, paginate
from typing import List, Optional, Dict, Any
import json
import time

from app.models import (
    TextInput, 
    TextAnalysisResult, 
    UserOut, 
    AnalysisHistoryOut,
    TokenResponse
)
from app.data_generator import DataGenerator
from app.auth import authenticate_user, create_access_token, get_current_user  # Candidate must implement
from app.llm_utils import analyze_text  # Candidate must implement
from app.core.exceptions import backend_exception_handler, BackendError

app = FastAPI(
    title="Infinitgraph Document Analyzer",
    description="An API for analyzing text using LLMs",
    version="1.0.0",
    docs_url=None,
)

app.add_exception_handler(BackendError, backend_exception_handler)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Middleware to track API response time"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def docs_redirect():
    """Redirect root to API documentation"""
    return RedirectResponse(url="/docs")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    """Custom Swagger UI documentation"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Infinitgraph Document Analyzer",
        swagger_favicon_url="https://example.com/favicon.png",
    )


# Initialize fake data
data_size = 100
generator = DataGenerator(data_size)
users, history = generator.generate_data()


@app.post("/api/token", response_model=TokenResponse, tags=["Authentication"])
async def login_for_access_token(username: str = Body(...), password: str = Body(...)):
    """
    Get an access token for API authentication
    
    This endpoint authenticates a user and provides a JWT token for accessing protected endpoints.
    """
    # TODO: Candidate should implement this in auth.py
    user = authenticate_user(username, password)
    
    if not user:
        raise BackendError(status=401, message="Invalid credentials")
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/analyze", response_model=TextAnalysisResult, tags=["Text Analysis"])
async def analyze_text_endpoint(
    text_input: TextInput,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Analyze text using LLM
    
    This endpoint processes the provided text and returns analysis results.
    """
    # TODO: Candidate should implement this using LLM integration
    try:
        # Call the analyze_text function that candidate will implement
        result = analyze_text(text_input.text, text_input.analysis_type)
        
        # Record this analysis in history (simplified)
        new_history = AnalysisHistoryOut(
            user_id=current_user.id,
            text_sample=text_input.text[:100] + "..." if len(text_input.text) > 100 else text_input.text,
            analysis_type=text_input.analysis_type,
            status="completed"
        )
        history.append(new_history)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/users", response_model=Page[UserOut], tags=["User Management"])
async def get_users(
    current_user: UserOut = Depends(get_current_user)
):
    """Get list of users (admin only)"""
    # TODO: Candidate should implement role-based access control
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    
    return paginate(users)


@app.get("/api/history", response_model=Page[AnalysisHistoryOut], tags=["Analysis History"])
async def get_analysis_history(
    current_user: UserOut = Depends(get_current_user)
):
    """Get analysis history for the current user"""
    # Filter history by user_id
    user_history = [h for h in history if h.user_id == current_user.id]
    return paginate(user_history)


@app.get("/api/health", tags=["System"])
async def health_check():
    """API health check endpoint"""
    return {"status": "healthy", "api_version": "1.0.0"}


add_pagination(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
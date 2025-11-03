import os
import logging
import uuid
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from .chatbot import CHATBOT

# Load environment variables from .env file
load_dotenv()

# Configure logging for the FastAPI app
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NovaPay Customer Support Chatbot API",
    description="REST API для взаимодействия с чат-ботом поддержки клиентов NovaPay",
    version="1.0.0"
)

# ============================================================================
# Pydantic Models for Request/Response Validation
# ============================================================================

class QueryRequest(BaseModel):
    """Model for incoming query requests."""
    query: str = Field(..., min_length=1, max_length=1000, description="User's question or query")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation continuity")
    user_id: Optional[str] = Field(None, description="Optional user ID for tracking")
    metadata: Optional[dict] = Field(None, description="Optional metadata about the user or query")

class QueryResponse(BaseModel):
    """Model for outgoing query responses."""
    query_id: str = Field(..., description="Unique identifier for this query")
    session_id: str = Field(..., description="Session ID for conversation continuity")
    query: str = Field(..., description="The original query")
    response: str = Field(..., description="The chatbot's response")
    confidence: Optional[float] = Field(None, description="Confidence score of the response (0-1)")
    source_documents: Optional[List[str]] = Field(None, description="Source documents used for the response")
    timestamp: str = Field(..., description="Timestamp of the response")
    processing_time_ms: float = Field(..., description="Time taken to process the query in milliseconds")

class HealthCheckResponse(BaseModel):
    """Model for health check response."""
    status: str = Field(..., description="Health status: 'ok' or 'degraded'")
    service: str = Field(..., description="Service name")
    timestamp: str = Field(..., description="Timestamp of the health check")

class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    timestamp: str = Field(..., description="Timestamp of the error")

# ============================================================================
# In-Memory Session Storage (For MVP; use Redis/DB in production)
# ============================================================================

sessions = {}

def create_session(user_id: Optional[str] = None) -> str:
    """Create a new session and return session ID."""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "user_id": user_id,
        "created_at": datetime.utcnow(),
        "conversation_history": []
    }
    logger.info(f"Created session: {session_id}")
    return session_id

def get_session(session_id: str) -> Optional[dict]:
    """Retrieve session data."""
    return sessions.get(session_id)

def save_to_conversation_history(session_id: str, query: str, response: str):
    """Save query and response to session's conversation history."""
    if session_id in sessions:
        sessions[session_id]["conversation_history"].append({
            "query": query,
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        })

# ============================================================================
# API Endpoints
# ============================================================================

@app.post("/api/v1/query", response_model=QueryResponse, tags=["Query"])
async def query_chatbot(request: QueryRequest, background_tasks: BackgroundTasks):
    """
    Query the customer support chatbot.
    
    - **query**: The user's question or query
    - **session_id**: Optional session ID for conversation continuity
    - **user_id**: Optional user ID for tracking
    - **metadata**: Optional metadata (e.g., user location, language)
    
    Returns a response with the chatbot's answer and metadata.
    """
    if CHATBOT is None:
        logger.error("Chatbot service is unavailable.")
        raise HTTPException(
            status_code=503,
            detail="Chatbot service is unavailable."
        )

    # Generate or retrieve session
    session_id = request.session_id or create_session(request.user_id)
    session = get_session(session_id)
    
    if session is None:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid session ID: {request.session_id}"
        )

    # Generate unique query ID
    query_id = str(uuid.uuid4())
    
    # Log query
    logger.info(f"Query ID: {query_id}, Session ID: {session_id}, Query: {request.query}")
    
    try:
        # Measure processing time
        import time
        start_time = time.time()
        
        # Get response from chatbot
        response_text = CHATBOT.get_response(request.query)
        
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Save to conversation history
        background_tasks.add_task(save_to_conversation_history, session_id, request.query, response_text)
        
        return QueryResponse(
            query_id=query_id,
            session_id=session_id,
            query=request.query,
            response=response_text,
            confidence=None,  # Can be enhanced with confidence scoring
            source_documents=None,  # Can be enhanced with source document extraction
            timestamp=datetime.utcnow().isoformat(),
            processing_time_ms=processing_time
        )
    
    except Exception as e:
        logger.error(f"Error processing query {query_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.get("/api/v1/session/{session_id}", tags=["Session"])
async def get_session_history(session_id: str):
    """
    Retrieve conversation history for a given session.
    
    - **session_id**: The session ID
    
    Returns the session metadata and conversation history.
    """
    session = get_session(session_id)
    
    if session is None:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {session_id}"
        )
    
    return {
        "session_id": session_id,
        "user_id": session.get("user_id"),
        "created_at": session.get("created_at").isoformat(),
        "conversation_history": session.get("conversation_history", [])
    }

@app.post("/api/v1/session", tags=["Session"])
async def create_new_session(user_id: Optional[str] = None):
    """
    Create a new session for conversation.
    
    - **user_id**: Optional user ID for tracking
    
    Returns the new session ID.
    """
    session_id = create_session(user_id)
    return {
        "session_id": session_id,
        "created_at": datetime.utcnow().isoformat()
    }

@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    status = "ok" if CHATBOT is not None else "degraded"
    logger.info(f"Health check status: {status}")
    return HealthCheckResponse(
        status=status,
        service="NovaPay Chatbot API",
        timestamp=datetime.utcnow().isoformat()
    )

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information."""
    return {
        "service": "NovaPay Customer Support Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return {
        "error": exc.detail,
        "error_code": str(exc.status_code),
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# Startup and Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Log startup event."""
    logger.info("FastAPI application started.")

@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown event."""
    logger.info("FastAPI application shut down.")

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("FASTAPI_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

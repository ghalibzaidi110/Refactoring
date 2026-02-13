from pydantic import BaseModel, Field
from typing import Optional


class RefactorRequest(BaseModel):
    """Request model for code refactoring"""
    code: str = Field(..., description="Python code to refactor", min_length=1)
    language: Optional[str] = Field(default="python", description="Programming language")
    use_llm: Optional[bool] = Field(default=True, description="Use LLM for intelligent refactoring")


class RefactorResponse(BaseModel):
    """Response model for refactored code"""
    summary: str = Field(..., description="Summary of changes made")
    refactored_code: str = Field(..., description="The refactored code")
    improvements: Optional[list[str]] = Field(default=None, description="List of improvements made")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(default="healthy", description="Service status")
    version: Optional[str] = Field(default="1.0.0", description="API version")

from fastapi import APIRouter, HTTPException
from app.schemas import RefactorRequest, RefactorResponse
from app.services.refactor import refactor_code

router = APIRouter()


@router.post("/refactor", response_model=RefactorResponse)
async def refactor(request: RefactorRequest):
    """
    Refactor Python code using formatting and optional LLM enhancement
    """
    try:
        result = refactor_code(
            code=request.code,
            use_llm=request.use_llm if request.use_llm is not None else True,
            llm_provider="openai"  # Can be made configurable
        )
        return RefactorResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

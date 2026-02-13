from typing import Dict, Any
from app.services.formatter import format_code, analyze_code_quality
from app.services.llm import refactor_with_llm


def refactor_code(code: str, use_llm: bool = True, llm_provider: str = "openai") -> Dict[str, Any]:
    """
    Main refactoring orchestration function
    
    Args:
        code: Python code to refactor
        use_llm: Whether to use LLM for intelligent refactoring
        llm_provider: LLM provider to use ('openai' or 'google')
    
    Returns:
        Dictionary with refactored code, summary, and improvements
    """
    all_improvements = []
    
    # Step 1: Format code
    formatted, format_improvements = format_code(code, formatter="black")
    all_improvements.extend(format_improvements)
    
    # Step 2: Analyze code quality
    quality_suggestions = analyze_code_quality(code)
    if quality_suggestions:
        all_improvements.extend(quality_suggestions)
    
    # Step 3: Apply LLM refactoring if enabled
    if use_llm:
        refactored, llm_improvements = refactor_with_llm(formatted, provider=llm_provider)
        all_improvements.extend(llm_improvements)
    else:
        refactored = formatted
        all_improvements.append("Basic formatting applied (LLM refactoring disabled)")
    
    # Generate summary
    summary = f"Code refactored with {len(all_improvements)} improvements"
    
    return {
        "refactored_code": refactored,
        "summary": summary,
        "improvements": all_improvements
    }

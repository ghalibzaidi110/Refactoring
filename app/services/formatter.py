import black
import autopep8
from typing import Tuple


def format_code(code: str, formatter: str = "black") -> Tuple[str, list[str]]:
    """
    Format Python code using black or autopep8
    
    Args:
        code: Python code to format
        formatter: Formatter to use ('black' or 'autopep8')
    
    Returns:
        Tuple of (formatted_code, list_of_improvements)
    """
    improvements = []
    
    try:
        if formatter.lower() == "black":
            formatted = black.format_str(code, mode=black.Mode())
            improvements.append("Applied Black formatting for consistent style")
        elif formatter.lower() == "autopep8":
            formatted = autopep8.fix_code(code)
            improvements.append("Applied autopep8 PEP 8 formatting")
        else:
            # Default to black
            formatted = black.format_str(code, mode=black.Mode())
            improvements.append("Applied Black formatting (default)")
        
        # Check if any changes were made
        if formatted != code:
            improvements.append("Fixed indentation and spacing")
            improvements.append("Normalized quotes and line breaks")
        else:
            improvements.append("Code already follows formatting standards")
            
        return formatted, improvements
        
    except Exception as e:
        # If formatting fails, return original code
        return code, [f"Formatting error: {str(e)}"]


def analyze_code_quality(code: str) -> list[str]:
    """
    Analyze code for potential improvements
    
    Args:
        code: Python code to analyze
    
    Returns:
        List of improvement suggestions
    """
    suggestions = []
    
    # Simple heuristics
    if "var " in code:
        suggestions.append("Replace 'var' with proper Python variable declaration")
    
    if code.count("\n") > 100:
        suggestions.append("Consider breaking large files into smaller modules")
    
    if "TODO" in code or "FIXME" in code:
        suggestions.append("Address TODO/FIXME comments")
    
    return suggestions

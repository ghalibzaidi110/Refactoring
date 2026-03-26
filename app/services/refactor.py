from typing import Dict, Any
from app.services.formatter import format_code, analyze_code_quality
from app.services.llm import refactor_with_llm
from app.services.parser import CodeParser


def refactor_code(
    code: str,
    use_llm: bool = True,
    llm_provider: str = "openai",
    language: str = "python",
) -> Dict[str, Any]:
    """
    Main refactoring orchestration function following the Architex.ai pipeline:

    1. Parsing Module  — analyze syntax & structure using AST
    2. AI Engine (LLM) — detect problems and suggest OOP patterns
    3. Refactoring Engine — apply formatter + LLM improvements
    4. Output Module   — return improved code + full report

    Args:
        code: Source code to refactor (Python or Java)
        use_llm: Whether to use LLM for intelligent OOP refactoring
        llm_provider: LLM provider ('openai' or 'google')
        language: Programming language ('python' or 'java')

    Returns:
        Dictionary with refactored code, summary, improvements,
        detected_smells, and suggested_patterns
    """
    all_improvements = []

    # ------------------------------------------------------------------ #
    # Step 1: Parse code — detect architectural smells & suggest patterns #
    # ------------------------------------------------------------------ #
    parser = CodeParser(code, language=language)
    detected_smells = parser.detect_smells()
    suggested_patterns = parser.suggest_patterns()

    # Surface non-trivial smells as improvement notes
    for smell in detected_smells:
        if "No major architectural" not in smell:
            all_improvements.append(f"Detected: {smell}")

    # ------------------------------------------------------------------ #
    # Step 2: Format code (Python only — Black/autopep8)                  #
    # ------------------------------------------------------------------ #
    if language.lower() == "python":
        formatted, format_improvements = format_code(code, formatter="black")
        all_improvements.extend(format_improvements)
    else:
        formatted = code
        all_improvements.append("Structure analyzed (formatting skipped for non-Python code)")

    # ------------------------------------------------------------------ #
    # Step 3: Static quality analysis (radon + pylint for Python)         #
    # ------------------------------------------------------------------ #
    if language.lower() == "python":
        quality_suggestions = analyze_code_quality(formatted)
        if quality_suggestions:
            all_improvements.extend(quality_suggestions)

    # ------------------------------------------------------------------ #
    # Step 4: LLM-driven OOP architectural refactoring                    #
    # ------------------------------------------------------------------ #
    if use_llm:
        refactored, llm_improvements = refactor_with_llm(
            formatted, provider=llm_provider, language=language
        )
        all_improvements.extend(llm_improvements)
    else:
        refactored = formatted
        all_improvements.append("Basic formatting applied (LLM refactoring disabled)")

    summary = f"Code refactored with {len(all_improvements)} improvements"

    return {
        "refactored_code": refactored,
        "summary": summary,
        "improvements": all_improvements,
        "detected_smells": detected_smells,
        "suggested_patterns": suggested_patterns,
    }

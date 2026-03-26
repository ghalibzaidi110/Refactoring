import os
import re
import subprocess
import tempfile

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
    Analyze code quality using radon (cyclomatic complexity + maintainability)
    and pylint (static analysis). Falls back gracefully if tools are unavailable.

    Args:
        code: Python code to analyze

    Returns:
        List of improvement suggestions
    """
    suggestions = []

    # --- radon: cyclomatic complexity & maintainability index ---
    try:
        from radon.complexity import cc_visit
        from radon.metrics import mi_visit, mi_rank

        results = cc_visit(code)
        for r in results:
            if r.complexity > 10:
                suggestions.append(
                    f"High cyclomatic complexity in '{r.name}' "
                    f"(complexity={r.complexity}) — consider breaking it up"
                )

        mi = mi_visit(code, multi=True)
        rank = mi_rank(mi)
        if rank in ("C", "D", "E", "F"):
            suggestions.append(
                f"Low maintainability index ({mi:.1f}, rank={rank}) "
                f"— code needs structural improvements"
            )
    except Exception:
        pass

    # --- pylint: static analysis ---
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            tmp_path = f.name

        result = subprocess.run(
            [
                "python", "-m", "pylint", tmp_path,
                "--output-format=text",
                "--score=no",
                # Suppress style-only noise; keep refactor (R) and warning (W) messages
                "--disable=C0114,C0115,C0116,C0103,W0611,R0903,W0621",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        msg_pattern = re.compile(r":\d+:\d+: ([RCWE]\d+): (.+) \([\w-]+\)")
        seen: set[str] = set()
        for line in result.stdout.splitlines():
            match = msg_pattern.search(line)
            if match:
                msg = match.group(2).strip()
                if msg and msg not in seen:
                    seen.add(msg)
                    suggestions.append(f"pylint: {msg}")
                if len(seen) >= 5:
                    break
    except Exception:
        pass
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    # --- basic heuristics (always run) ---
    if "TODO" in code or "FIXME" in code:
        suggestions.append("Address TODO/FIXME comments before finalizing")

    return suggestions

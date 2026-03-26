import ast
import re
from collections import Counter
from typing import Any, Dict, List


class CodeParser:
    """
    AST-based code parser for detecting architectural issues and OOP opportunities.
    Supports Python (full AST analysis) and Java (regex-based analysis).
    """

    def __init__(self, code: str, language: str = "python"):
        self.code = code
        self.language = language.lower()
        self.tree = None
        if self.language == "python":
            try:
                self.tree = ast.parse(code)
            except SyntaxError:
                self.tree = None

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def parse(self) -> Dict[str, Any]:
        """Parse code and return structural analysis"""
        if self.language == "python":
            return self._parse_python()
        elif self.language == "java":
            return self._parse_java()
        return {"error": "Unsupported language"}

    def _parse_python(self) -> Dict[str, Any]:
        if not self.tree:
            return {"error": "Could not parse Python code — check for syntax errors"}

        classes = []
        functions = []
        imports = []
        global_vars = []

        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = [
                    n for n in ast.iter_child_nodes(node)
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "methods": [m.name for m in methods],
                    "method_count": len(methods),
                    "has_docstring": (
                        bool(node.body)
                        and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Constant)
                    ),
                })
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append({"name": node.name, "line": node.lineno})
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        global_vars.append(target.id)

        return {
            "classes": classes,
            "functions": functions,
            "imports": imports,
            "global_vars": global_vars,
            "total_lines": len(self.code.splitlines()),
        }

    def _parse_java(self) -> Dict[str, Any]:
        """Regex-based Java code structure analysis"""
        class_names = re.findall(r'\bclass\s+(\w+)', self.code)
        method_names = re.findall(
            r'(?:public|private|protected)\s+(?:static\s+)?[\w<>\[\]]+\s+(\w+)\s*\(', self.code
        )
        imports = re.findall(r'import\s+([\w.]+);', self.code)

        classes = []
        for name in class_names:
            # Find methods inside this class (rough heuristic)
            pattern = rf'class\s+{re.escape(name)}.*?\{{(.*?)(?=\bclass\b|\Z)'
            match = re.search(pattern, self.code, re.DOTALL)
            body = match.group(1) if match else ""
            methods = re.findall(
                r'(?:public|private|protected)\s+(?:static\s+)?[\w<>\[\]]+\s+(\w+)\s*\(',
                body
            )
            classes.append({
                "name": name,
                "methods": methods,
                "method_count": len(methods),
                "has_docstring": "/**" in body,
            })

        return {
            "classes": classes,
            "functions": [{"name": m} for m in method_names],
            "imports": imports,
            "global_vars": [],
            "total_lines": len(self.code.splitlines()),
        }

    # ------------------------------------------------------------------
    # Code smell detection
    # ------------------------------------------------------------------

    def detect_smells(self) -> List[str]:
        """Detect code smells and architectural issues"""
        smells = []
        structure = self.parse()

        if "error" in structure:
            return [structure["error"]]

        classes = structure.get("classes", [])
        functions = structure.get("functions", [])
        imports = structure.get("imports", [])
        total_lines = structure.get("total_lines", 0)

        # Large class (God Object)
        for cls in classes:
            if cls.get("method_count", 0) > 10:
                smells.append(
                    f"Large class (God Object): '{cls['name']}' has {cls['method_count']} methods "
                    f"— consider splitting into smaller, focused classes"
                )

        # No OOP structure
        if not classes and total_lines > 30:
            smells.append(
                "No classes found — consider applying OOP structure "
                "(Encapsulation, Abstraction) to organize the code"
            )

        # Too many standalone functions
        if len(functions) > 8:
            smells.append(
                f"Feature envy / procedural code: {len(functions)} standalone functions detected "
                f"— consider grouping related ones into classes"
            )

        # Tight coupling (repeated imports from the same module)
        import_counts = Counter(imp for imp in imports if imp)
        for module, count in import_counts.items():
            if count > 3:
                smells.append(
                    f"Tight coupling: module '{module}' is referenced {count} times "
                    f"— consider dependency injection or a service locator"
                )

        # Large file
        if total_lines > 200:
            smells.append(
                f"Large file ({total_lines} lines) — consider breaking into "
                f"smaller, single-responsibility modules"
            )

        # Duplicate code (simple heuristic: repeated non-trivial lines)
        lines = [
            line.strip() for line in self.code.splitlines()
            if line.strip() and not line.strip().startswith(("#", "//", "/*", "*"))
        ]
        dup_counts = Counter(lines)
        duplicates = [line for line, count in dup_counts.items() if count > 2 and len(line) > 10]
        if duplicates:
            smells.append(
                f"Duplicate code: {len(duplicates)} repeated statement(s) found "
                f"— extract into shared methods or a base class"
            )

        # Missing docstrings (Python only)
        if self.language == "python" and self.tree:
            missing = 0
            for node in ast.walk(self.tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if not (
                        node.body
                        and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Constant)
                    ):
                        missing += 1
            if missing:
                smells.append(
                    f"{missing} function(s)/class(es) missing docstrings "
                    f"— add documentation for maintainability"
                )

        # Global variables (bad practice in OOP)
        global_vars = structure.get("global_vars", [])
        if global_vars:
            smells.append(
                f"Global variables detected: {global_vars} "
                f"— encapsulate inside classes to improve maintainability"
            )

        return smells if smells else ["No major architectural issues detected"]

    # ------------------------------------------------------------------
    # OOP design pattern suggestions
    # ------------------------------------------------------------------

    def suggest_patterns(self) -> List[str]:
        """Suggest applicable OOP design patterns based on code structure"""
        suggestions = []
        structure = self.parse()

        if "error" in structure:
            return suggestions

        classes = structure.get("classes", [])
        total_lines = structure.get("total_lines", 0)

        # Singleton — for resource managers, connections, config
        for cls in classes:
            methods = cls.get("methods", [])
            if any(
                m in methods
                for m in ["connect", "get_instance", "getInstance", "open", "load_config"]
            ):
                suggestions.append(
                    f"Singleton pattern: '{cls['name']}' manages a shared resource "
                    f"— ensure only one instance exists using the Singleton pattern"
                )

        # Factory — when multiple similar classes exist
        if len(classes) > 2:
            suggestions.append(
                "Factory pattern: multiple classes detected — use a Factory class to "
                "centralize and abstract object creation"
            )

        # Observer — for event-driven or notification logic
        for cls in classes:
            methods = cls.get("methods", [])
            if any(
                m in methods
                for m in ["notify", "update", "subscribe", "emit", "dispatch", "on_event", "handle"]
            ):
                suggestions.append(
                    f"Observer pattern: '{cls['name']}' has event-like methods "
                    f"— formalize with a Subject/Observer interface for loose coupling"
                )

        # MVC — large files mixing UI and logic with no class structure
        if total_lines > 80 and not classes:
            suggestions.append(
                "MVC pattern: code mixes data, logic, and output "
                "— separate into Model (data), View (presentation), Controller (logic)"
            )

        # Strategy pattern — multiple if/elif blocks suggesting swappable algorithms
        elif_count = len(re.findall(r'\belif\b', self.code))
        if elif_count > 4:
            suggestions.append(
                f"Strategy pattern: {elif_count} elif branches detected — consider replacing "
                f"with a Strategy pattern to make algorithms interchangeable"
            )

        return suggestions if suggestions else ["No specific design pattern changes detected"]

import os
from typing import Optional, Tuple
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMRefactorer:
    """LLM-based code refactoring using OpenAI or Google AI"""
    
    def __init__(self, provider: str = "openai"):
        """
        Initialize LLM refactorer
        
        Args:
            provider: 'openai' or 'google'
        """
        self.provider = provider.lower()
        
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                self.client = None
                
        elif self.provider == "google":
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
            else:
                self.model = None
    
    def _create_prompt(self, code: str, language: str = "python") -> str:
        """Create OOP-focused architectural refactoring prompt for LLM"""
        lang_display = language.capitalize()
        return f"""You are an expert software architect and {lang_display} developer specializing in OOP design patterns and clean architecture.

Refactor the following {lang_display} code by applying the appropriate OOP principles and design patterns listed below.

OOP Principles to enforce:
- Encapsulation: bundle data with its methods; restrict direct field access
- Inheritance: extract common behavior into base/abstract classes
- Polymorphism: use method overriding and interfaces/abstract methods
- Abstraction: hide implementation details behind clean interfaces

Design Patterns to apply where relevant:
- Singleton: for classes representing a single shared resource (DB connection, config, logger)
- Factory: centralize object creation; avoid direct instantiation of concrete classes
- Observer: decouple event producers from consumers using Subject/Observer interfaces
- MVC: separate data (Model), business logic (Controller), and presentation (View)

Also fix these architectural smells:
- Duplicate code — extract into shared methods or a base class
- Large classes (God Objects) — split into smaller, single-responsibility classes
- Tight coupling — use dependency injection or interfaces
- Global variables — encapsulate inside classes
- Missing docstrings — add clear documentation

Original {lang_display} code:
```{language}
{code}
```

Provide ONLY the refactored code without any explanations or commentary.
Return only valid {lang_display} code."""

    def refactor_with_openai(self, code: str, language: str = "python") -> Tuple[str, list[str]]:
        """Refactor code using OpenAI GPT with OOP-focused architectural improvements"""
        if not self.client:
            return code, ["OpenAI API key not configured"]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are an expert {language.capitalize()} software architect "
                            f"specializing in OOP design patterns (Singleton, Factory, Observer, MVC) "
                            f"and clean code principles."
                        ),
                    },
                    {"role": "user", "content": self._create_prompt(code, language)},
                ],
                temperature=0.3,
                max_tokens=3000,
            )

            refactored = response.choices[0].message.content.strip()

            # Strip markdown code fences if present
            refactored = self._strip_code_fences(refactored, language)

            improvements = [
                "Applied OOP principles (Encapsulation, Inheritance, Polymorphism, Abstraction)",
                "Applied relevant design patterns (Singleton / Factory / Observer / MVC)",
                "Eliminated code smells and improved architecture",
            ]

            return refactored, improvements

        except Exception as e:
            return code, [f"OpenAI refactoring error: {str(e)}"]
    
    @staticmethod
    def _strip_code_fences(text: str, language: str = "python") -> str:
        """Remove markdown code fences from LLM output"""
        fence_lang = f"```{language}"
        if text.startswith(fence_lang):
            text = text[len(fence_lang):].split("```")[0].strip()
        elif text.startswith("```"):
            text = text[3:].split("```")[0].strip()
        return text

    def refactor_with_google(self, code: str, language: str = "python") -> Tuple[str, list[str]]:
        """Refactor code using Google Gemini with OOP-focused architectural improvements"""
        if not self.model:
            return code, ["Google API key not configured"]

        try:
            response = self.model.generate_content(self._create_prompt(code, language))
            refactored = self._strip_code_fences(response.text.strip(), language)

            improvements = [
                "Applied OOP principles via Gemini (Encapsulation, Inheritance, Polymorphism, Abstraction)",
                "Applied relevant design patterns (Singleton / Factory / Observer / MVC)",
                "Eliminated code smells and improved architecture",
            ]

            return refactored, improvements

        except Exception as e:
            return code, [f"Google AI refactoring error: {str(e)}"]
    
    def refactor(self, code: str, language: str = "python") -> Tuple[str, list[str]]:
        """
        Refactor code using the configured LLM provider.

        Args:
            code: Source code to refactor
            language: Programming language ('python' or 'java')

        Returns:
            Tuple of (refactored_code, improvements_list)
        """
        if self.provider == "openai":
            return self.refactor_with_openai(code, language)
        elif self.provider == "google":
            return self.refactor_with_google(code, language)
        else:
            return code, ["Unknown LLM provider"]


# Singleton instance
_refactorer: Optional[LLMRefactorer] = None


def get_refactorer(provider: str = "openai") -> LLMRefactorer:
    """Get or create LLM refactorer instance"""
    global _refactorer
    if _refactorer is None or _refactorer.provider != provider:
        _refactorer = LLMRefactorer(provider)
    return _refactorer


def refactor_with_llm(
    code: str, provider: str = "openai", language: str = "python"
) -> Tuple[str, list[str]]:
    """
    Convenience function to refactor code with LLM using OOP-focused prompting.

    Args:
        code: Source code to refactor
        provider: LLM provider ('openai' or 'google')
        language: Programming language ('python' or 'java')

    Returns:
        Tuple of (refactored_code, improvements_list)
    """
    refactorer = get_refactorer(provider)
    return refactorer.refactor(code, language)

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
    
    def _create_prompt(self, code: str) -> str:
        """Create refactoring prompt for LLM"""
        return f"""You are an expert Python developer. Refactor the following Python code to improve:
- Code readability and clarity
- Performance and efficiency
- Following Python best practices (PEP 8)
- Adding helpful docstrings and comments where needed
- Removing code smells and anti-patterns

Original code:
```python
{code}
```

Provide ONLY the refactored code without any explanations. Return only valid Python code."""

    def refactor_with_openai(self, code: str) -> Tuple[str, list[str]]:
        """Refactor code using OpenAI GPT"""
        if not self.client:
            return code, ["OpenAI API key not configured"]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert Python refactoring assistant."},
                    {"role": "user", "content": self._create_prompt(code)}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            refactored = response.choices[0].message.content.strip()
            
            # Clean up markdown code blocks if present
            if refactored.startswith("```python"):
                refactored = refactored.split("```python")[1].split("```")[0].strip()
            elif refactored.startswith("```"):
                refactored = refactored.split("```")[1].split("```")[0].strip()
            
            improvements = [
                "Applied AI-powered refactoring",
                "Improved code structure and readability",
                "Enhanced with best practices"
            ]
            
            return refactored, improvements
            
        except Exception as e:
            return code, [f"OpenAI refactoring error: {str(e)}"]
    
    def refactor_with_google(self, code: str) -> Tuple[str, list[str]]:
        """Refactor code using Google Gemini"""
        if not self.model:
            return code, ["Google API key not configured"]
        
        try:
            response = self.model.generate_content(self._create_prompt(code))
            refactored = response.text.strip()
            
            # Clean up markdown code blocks if present
            if refactored.startswith("```python"):
                refactored = refactored.split("```python")[1].split("```")[0].strip()
            elif refactored.startswith("```"):
                refactored = refactored.split("```")[1].split("```")[0].strip()
            
            improvements = [
                "Applied AI-powered refactoring with Gemini",
                "Improved code structure and readability",
                "Enhanced with best practices"
            ]
            
            return refactored, improvements
            
        except Exception as e:
            return code, [f"Google AI refactoring error: {str(e)}"]
    
    def refactor(self, code: str) -> Tuple[str, list[str]]:
        """
        Refactor code using configured LLM provider
        
        Args:
            code: Python code to refactor
        
        Returns:
            Tuple of (refactored_code, improvements_list)
        """
        if self.provider == "openai":
            return self.refactor_with_openai(code)
        elif self.provider == "google":
            return self.refactor_with_google(code)
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


def refactor_with_llm(code: str, provider: str = "openai") -> Tuple[str, list[str]]:
    """
    Convenience function to refactor code with LLM
    
    Args:
        code: Python code to refactor
        provider: LLM provider ('openai' or 'google')
    
    Returns:
        Tuple of (refactored_code, improvements_list)
    """
    refactorer = get_refactorer(provider)
    return refactorer.refactor(code)

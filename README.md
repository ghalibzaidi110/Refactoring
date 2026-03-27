
# Architex.ai

Automated Architectural Refactoring for Python & Java

---

**Architex.ai** is an AI-powered tool that analyzes and refactors your Python or Java code, applying OOP principles, design patterns, and fixing architectural smells. It features a modern web UI and a REST API for programmatic access.

## Features

- **Web UI**: Modern, dark-themed, with syntax highlighting and side-by-side editors
- **Language Support**: Python and Java
- **OOP & Design Patterns**: Detects and applies Singleton, Factory, Observer, MVC, and more
- **Architectural Smell Detection**: Finds large classes, duplicate code, tight coupling, missing docstrings, and more
- **AI-Powered Refactoring**: Uses OpenAI GPT or Google Gemini to rewrite code with OOP best practices
- **Static Analysis**: Integrates Black, autopep8, pylint, and radon for formatting and quality
- **Full Report**: Returns detected smells, suggested patterns, and all improvements
- **REST API**: FastAPI backend for automation and integration

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/refactorgpt.git
cd refactorgpt
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

**Activate the virtual environment:**

- **Windows (PowerShell):**
  ```bash
  venv\Scripts\activate
  ```
- **Windows (CMD):**
  ```bash
  venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

> **Troubleshooting:** If you get an error like `Unable to copy venvlauncher.exe` (common with Python 3.14), try:
> ```bash
> python -m venv venv --without-pip
> ```
> Then activate the venv and install pip manually:
> ```bash
> venv\Scripts\activate
> python -m ensurepip --upgrade
> ```
> Alternatively, use `virtualenv`:
> ```bash
> pip install virtualenv
> virtualenv venv
> ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example env file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

Get API keys from:
- **OpenAI:** https://platform.openai.com/api-keys
- **Google AI:** https://makersuite.google.com/app/apikey

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The app will start at **http://127.0.0.1:8000**.

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000 | Web UI |
| http://127.0.0.1:8000/docs | API Documentation (Swagger) |
| http://127.0.0.1:8000/health | Health Check |

---

## How It Works

1. **Parsing** - Analyzes code structure (AST for Python, regex for Java)
2. **Smell Detection** - Finds large classes, duplicate code, tight coupling, missing OOP, etc.
3. **Static Analysis** - Runs Black, autopep8, pylint, and radon (Python only)
4. **OOP Refactoring** - LLM rewrites code to apply OOP principles and design patterns
5. **Full Report** - Returns refactored code, detected smells, suggested patterns, and all improvements

---

## API Usage

### Refactor Code Endpoint

**POST** `/api/refactor`

Request body:
```json
{
  "code": "public class Hello { public static void main(String[] args) { System.out.println(\"Hello, World!\"); } }",
  "language": "java",
  "use_llm": true
}
```

Response:
```json
{
  "summary": "Code refactored with 7 improvements",
  "refactored_code": "...refactored code...",
  "improvements": [
    "Applied OOP principles (Encapsulation, Inheritance, ...)",
    "Applied Singleton pattern",
    "Eliminated duplicate code"
  ],
  "detected_smells": [
    "Large class (God Object): ...",
    "Duplicate code: ..."
  ],
  "suggested_patterns": [
    "Factory pattern: ...",
    "Observer pattern: ..."
  ]
}
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/api/refactor" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "public class Hello { ... }",
    "language": "java",
    "use_llm": true
  }'
```

### Python Example

```python
import requests

response = requests.post(
    "http://localhost:8000/api/refactor",
    json={
        "code": "def add(x,y):\n  return x+y",
        "use_llm": True
    }
)

result = response.json()
print(result["refactored_code"])
```

---

## Project Structure

```
refactorgpt/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── schemas.py           # Pydantic models for request/response
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API route handlers
│   └── services/
│       ├── __init__.py
│       ├── formatter.py     # Code formatting with Black/autopep8
│       ├── llm.py           # LLM integration (OpenAI/Google)
│       ├── parser.py        # Code parsing and AST analysis
│       └── refactor.py      # Main refactoring orchestration
├── static/
│   ├── css/
│   │   └── style.css        # Application styles
│   └── js/
│       └── script.js        # Frontend logic
├── templates/
│   └── index.html           # Web UI template
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

---

## Configuration Options

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | Yes (if using OpenAI) |
| `GOOGLE_API_KEY` | Google AI API key for Gemini models | Optional |
| `DEFAULT_LLM_PROVIDER` | Default LLM provider (`openai` or `google`) | Optional |
| `DEBUG` | Enable debug mode (`True`/`False`) | Optional |

### LLM Providers

The application supports two LLM providers:

1. **OpenAI** (default) - Uses GPT-4-mini for refactoring
2. **Google Gemini** - Uses gemini-pro model

You can configure the provider in the request or set a default in `.env`.

---

## Development

### Running Tests

```bash
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

### Code Quality

```bash
# Format code
black app/

# Lint code
pylint app/

# Type checking
mypy app/
```

---

## Deployment

### Deploying to Render

1. Push your code to GitHub/GitLab
2. Create a new Web Service on [Render Dashboard](https://dashboard.render.com/)
3. Configure:
   - **Build Command:** `./build.sh`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Python Version:** 3.11.0
4. Set environment variables (`OPENAI_API_KEY`, `GOOGLE_API_KEY`)
5. Deploy

### Using Docker

```bash
docker build -t refactorgpt .
docker run -p 8000:8000 --env-file .env refactorgpt
```

### Using Heroku

```bash
heroku login
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set GOOGLE_API_KEY=your_key_here
git push heroku main
```

---

## Tech Stack

- **Backend**: FastAPI, Python 3.10+
- **LLM SDKs**: OpenAI, Google Generative AI
- **Code Formatting**: Black, autopep8
- **Static Analysis**: pylint, radon
- **Data Validation**: Pydantic
- **Frontend**: HTML, CSS, JavaScript with Highlight.js

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

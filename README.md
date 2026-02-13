# RefactorGPT

AI-powered Python code refactoring tool with web UI and REST API. Automatically improves code quality using Black formatting and LLM-based intelligent refactoring.

## Features

- **Web UI**: Beautiful dark-themed interface with syntax highlighting
- **REST API**: FastAPI-based API for programmatic access
- **AI-Powered**: Uses OpenAI GPT or Google Gemini for intelligent refactoring
- **Code Formatting**: Automatic formatting with Black or autopep8
- **Quality Analysis**: Built-in code quality suggestions
- **Dual Editors**: Side-by-side editable input and read-only output

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd refactorgpt

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

Get API keys from:
- OpenAI: https://platform.openai.com/api-keys
- Google AI: https://makersuite.google.com/app/apikey

### 3. Run the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the application:
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API Usage

### Refactor Code Endpoint

**POST** `/api/refactor`

Request body:
```json
{
  "code": "def hello():\n    print('Hello, World!')",
  "language": "python",
  "use_llm": true
}
```

Response:
```json
{
  "summary": "Code refactored with 5 improvements",
  "refactored_code": "def hello():\n    \"\"\"Print a greeting message.\"\"\"\n    print(\"Hello, World!\")",
  "improvements": [
    "Applied Black formatting for consistent style",
    "Fixed indentation and spacing",
    "Applied AI-powered refactoring",
    "Improved code structure and readability",
    "Enhanced with best practices"
  ]
}
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/api/refactor" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(x,y):\n  return x+y",
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
│       ├── llm.py          # LLM integration (OpenAI/Google)
│       └── refactor.py     # Main refactoring orchestration
├── static/                  # Static assets (CSS, JS)
├── templates/               # HTML templates
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Configuration Options

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for GPT models
- `GOOGLE_API_KEY`: Google AI API key for Gemini models
- `DEFAULT_LLM_PROVIDER`: Default LLM provider (openai/google)
- `DEBUG`: Enable debug mode (True/False)

### LLM Providers

The application supports two LLM providers:

1. **OpenAI** (default): Uses GPT-4-mini for refactoring
2. **Google Gemini**: Uses gemini-pro model

You can configure the provider in the request or set a default in `.env`.

## Development

### Running Tests

```bash
# Install test dependencies
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

## Deployment

### Deploying to Render

1. **Push your code to GitHub/GitLab**

2. **Create a new Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" and select "Web Service"
   - Connect your repository

3. **Configure the service**
   - **Name**: refactorgpt (or your preferred name)
   - **Environment**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Python Version**: 3.11.0 (specified in runtime.txt)

4. **Set environment variables**
   - Add `OPENAI_API_KEY` with your OpenAI API key
   - Add `GOOGLE_API_KEY` with your Google AI API key (optional)
   
5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app

**Note**: The app uses `render.yaml` for automatic configuration. You can also use the Render Blueprint feature by committing this file.

### Using uvicorn (Manual Deployment)

```bash
# For production with multiple workers
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4
```

### Using Docker

```bash
# Build image
docker build -t refactorgpt .

# Run container
docker run -p 8000:8000 --env-file .env refactorgpt
```

### Using Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set GOOGLE_API_KEY=your_key_here

# Deploy
git push heroku main
```

### Environment Variables for Production

Make sure to set these in your deployment platform:
- `OPENAI_API_KEY` - Required for OpenAI GPT refactoring
- `GOOGLE_API_KEY` - Optional, for Google Gemini refactoring
- `PORT` - Automatically set by most platforms (Render, Heroku, etc.)

## Tech Stack

- **Backend**: FastAPI, Python 3.10+
- **LLM SDKs**: OpenAI, Google Generative AI
- **Code Formatting**: Black, autopep8
- **Data Validation**: Pydantic
- **Frontend**: HTML, CSS, JavaScript with Highlight.js

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

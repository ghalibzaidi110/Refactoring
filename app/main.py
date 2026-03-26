from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api.routes import router
from app.schemas import HealthResponse, RefactorRequest, RefactorResponse
from app.services.refactor import refactor_code
from pathlib import Path

# Get base directory
BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="RefactorGPT",
    description="AI-powered Python code refactoring API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Include API routes
app.include_router(router, prefix="/api", tags=["refactor"])


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the web UI"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/refactor", response_model=RefactorResponse)
async def refactor_endpoint(request: RefactorRequest):
    """
    Legacy refactor endpoint for the web UI (mirrors /api/refactor)
    """
    import traceback
    try:
        result = refactor_code(
            code=request.code,
            use_llm=request.use_llm if request.use_llm is not None else True,
            llm_provider="openai",
            language=request.language or "python",
        )
        return RefactorResponse(**result)
    except Exception as e:
        print(f"Error in refactor_endpoint: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(status="healthy", version="1.0.0")

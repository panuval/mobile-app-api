# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Run Commands
- **Run development server:** `python run.py` or `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- **Run with Gunicorn:** `gunicorn -c gunicorn_conf.py app.main:app`
- **Build Docker container:** `docker build -t panuval-api .`
- **Run Docker container:** `docker run -p 8000:8000 panuval-api`

## Code Style Guidelines
- **Imports:** Group imports by standard library, third-party packages, then local modules
- **Typing:** Use Python type hints with Pydantic models for request/response validation
- **Error Handling:** Use FastAPI `HTTPException` with appropriate status codes
- **Naming:** Use snake_case for variables/functions, CamelCase for classes, UPPERCASE for constants
- **API Design:** Follow RESTful principles with consistent endpoint structure
- **DB Models:** SQLAlchemy ORM models in `/app/models`, Pydantic schemas in `/app/schemas`
- **Route Organization:** Keep endpoint logic in `/app/api/endpoints` categorized by resource
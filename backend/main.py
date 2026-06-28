from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="CLauseIQ Query System")

# CORS — allow frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Lock to your frontend URL in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
# Run: uvicorn main:app --reload --port 8000

# Health check — Render pings this to verify deploy success
@app.get("/health")
def health():
    return {"status": "ok", "app": "ClauseIQ"}
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import init_db
from routers import (
    user_router,
    candidate_router,
    recruiter_router,
    job_router,
    cv_router,
    application_router,
    match_router,
    system_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    print("✓ Database initialized")
    yield
    # Shutdown
    print("✓ Shutdown complete")


app = FastAPI(
    title="Job Matcher API",
    description="Backend API for Mastodon Job Matcher Extension",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(user_router.router)
app.include_router(candidate_router.router)
app.include_router(recruiter_router.router)
app.include_router(job_router.router)
app.include_router(cv_router.router)
app.include_router(application_router.router)
app.include_router(match_router.router)
app.include_router(system_router.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Job Matcher API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
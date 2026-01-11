from fastapi import FastAPI

from app.database import engine, Base
from app.routers import cats, missions, targets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spy Cat Agency API",
    description="Management system for spy cats, missions, and targets",
    version="1.0"
)

app.include_router(cats.router)
app.include_router(missions.router)
app.include_router(targets.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Spy Cat Agency API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


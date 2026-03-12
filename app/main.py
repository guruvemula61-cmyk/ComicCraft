from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router


app = FastAPI(
    title="ComicCraft AI Generator",
    description="AI powered comic generator using Gemini and Stable Diffusion",
    version="1.0"
)


# Static files (images, exports, fonts)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Include application routes
app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ComicCraft API running"}
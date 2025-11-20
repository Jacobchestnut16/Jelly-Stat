from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, media, user, sync, api_keys

def create_app():
    app = FastAPI(title="Film Finder", version="0.1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # include routes
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(media.router, prefix="/media", tags=["Media"])
    app.include_router(sync.router, prefix="/sync", tags=["Sync"])
    app.include_router(api_keys.router, prefix="/keys", tags=["Keys"])

    app.include_router(user.router, prefix="/user", tags=["User"])

    @app.get("/health")
    def health():
        return {"ok": True}

    return app

app = create_app()

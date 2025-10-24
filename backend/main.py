from fastapi import FastAPI
from backend.db import init_db
from backend.routers import auth, post, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Aghype API - Backend version 0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(post.router)


init_db(app)


@app.get('/')
async def root():
    return {"msg": "Hello - FastAPI TikTok starter"}
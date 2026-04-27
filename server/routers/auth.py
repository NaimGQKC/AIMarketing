"""VisiMind -- Auth Router (JWT + bcrypt)"""
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
import aiosqlite

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import SECRET_KEY
from database import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

BLOCKED_DOMAINS = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "icloud.com", "protonmail.com", "aol.com", "live.com",
    "mail.com", "yandex.com", "zoho.com", "gmx.com",
}

class SignupRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)
    company_name: str = Field(min_length=1)
    company_url: str = ""

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    token: str
    user: dict

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=30),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def validate_work_email(email: str) -> None:
    domain = email.split("@")[-1].lower()
    if domain in BLOCKED_DOMAINS:
        raise HTTPException(
            status_code=422,
            detail="Please use your work email to access the pilot. Generic email providers are not accepted.",
        )

async def require_user(request: Request, db: aiosqlite.Connection = Depends(get_db)) -> dict:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")
    token = auth_header.split(" ", 1)[1]
    user_id = decode_token(token)
    cursor = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = await cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return dict(user)

@router.post("/signup", response_model=AuthResponse)
async def signup(req: SignupRequest, db: aiosqlite.Connection = Depends(get_db)):
    validate_work_email(req.email)
    cursor = await db.execute("SELECT id FROM users WHERE email = ?", (req.email.lower(),))
    if await cursor.fetchone():
        raise HTTPException(status_code=409, detail="Email already registered")
    user_id = str(uuid.uuid4())
    pw_hash = hash_password(req.password)
    await db.execute(
        "INSERT INTO users (id, email, password_hash, company_name, company_url) VALUES (?, ?, ?, ?, ?)",
        (user_id, req.email.lower(), pw_hash, req.company_name, req.company_url),
    )
    await db.commit()
    token = create_token(user_id)
    return AuthResponse(
        token=token,
        user={"id": user_id, "email": req.email.lower(), "company_name": req.company_name, "company_url": req.company_url, "has_brand": False},
    )

@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM users WHERE email = ?", (req.email.lower(),))
    user = await cursor.fetchone()
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    cursor = await db.execute("SELECT id FROM brand_profiles WHERE user_id = ?", (user["id"],))
    has_brand = await cursor.fetchone() is not None
    token = create_token(user["id"])
    return AuthResponse(
        token=token,
        user={"id": user["id"], "email": user["email"], "company_name": user["company_name"], "company_url": user["company_url"], "has_brand": has_brand},
    )

@router.get("/me")
async def get_me(user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id FROM brand_profiles WHERE user_id = ?", (user["id"],))
    has_brand = await cursor.fetchone() is not None
    return {
        "id": user["id"],
        "email": user["email"],
        "company_name": user["company_name"],
        "company_url": user["company_url"],
        "has_brand": has_brand,
    }

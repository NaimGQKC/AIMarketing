"""VisiMind -- Auth Router (JWT + bcrypt + email verification + rate limiting)"""
import uuid
import random
import string
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
import aiosqlite

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import SECRET_KEY, DEBUG
from database import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

BLOCKED_DOMAINS = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "icloud.com", "protonmail.com", "aol.com", "live.com",
    "mail.com", "yandex.com", "zoho.com", "gmx.com",
}

# --- IP rate limiting (in-memory, resets on restart) ---
_signup_attempts: dict[str, list[datetime]] = defaultdict(list)
SIGNUP_LIMIT_PER_IP = 5  # max signups per IP per day


def _check_ip_rate_limit(ip: str):
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)
    _signup_attempts[ip] = [t for t in _signup_attempts[ip] if t > cutoff]
    if len(_signup_attempts[ip]) >= SIGNUP_LIMIT_PER_IP:
        raise HTTPException(
            status_code=429,
            detail="Too many signup attempts from this address. Try again in 24 hours.",
        )
    _signup_attempts[ip].append(now)


# --- Models ---
class SignupRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)
    company_name: str = Field(min_length=1)
    company_url: str = ""

class LoginRequest(BaseModel):
    email: str
    password: str

class VerifyEmailRequest(BaseModel):
    code: str

class AuthResponse(BaseModel):
    token: str
    user: dict


# --- Helpers ---
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

def _generate_verification_code() -> str:
    return "".join(random.choices(string.digits, k=6))


# --- Dependency ---
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


# --- Endpoints ---
@router.post("/signup", response_model=AuthResponse)
async def signup(req: SignupRequest, request: Request, db: aiosqlite.Connection = Depends(get_db)):
    # Rate limit by IP
    client_ip = request.client.host if request.client else "unknown"
    _check_ip_rate_limit(client_ip)

    validate_work_email(req.email)
    cursor = await db.execute("SELECT id FROM users WHERE email = ?", (req.email.lower(),))
    if await cursor.fetchone():
        raise HTTPException(status_code=409, detail="Email already registered")

    user_id = str(uuid.uuid4())
    pw_hash = hash_password(req.password)
    code = _generate_verification_code()
    expires = (datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat()

    await db.execute(
        """INSERT INTO users (id, email, password_hash, company_name, company_url,
           email_verified, verification_code, verification_expires)
           VALUES (?, ?, ?, ?, ?, 0, ?, ?)""",
        (user_id, req.email.lower(), pw_hash, req.company_name, req.company_url, code, expires),
    )
    await db.commit()

    # Log verification code (in production, send via email)
    print(f"\n{'='*50}")
    print(f"  VERIFICATION CODE for {req.email.lower()}: {code}")
    print(f"  Expires in 30 minutes")
    print(f"{'='*50}\n")

    token = create_token(user_id)
    user_data = {
        "id": user_id,
        "email": req.email.lower(),
        "company_name": req.company_name,
        "company_url": req.company_url,
        "has_brand": False,
        "email_verified": False,
    }

    # In debug mode, include code in response so frontend can show it for testing
    if DEBUG:
        user_data["_dev_verification_code"] = code

    return AuthResponse(token=token, user=user_data)


@router.post("/verify-email")
async def verify_email(req: VerifyEmailRequest, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Verify email with 6-digit code."""
    if user.get("email_verified"):
        return {"verified": True, "message": "Email already verified"}

    stored_code = user.get("verification_code")
    expires_str = user.get("verification_expires")

    if not stored_code:
        raise HTTPException(status_code=400, detail="No verification code found. Request a new one.")

    # Check expiry
    if expires_str:
        expires = datetime.fromisoformat(expires_str)
        if datetime.now(timezone.utc) > expires:
            raise HTTPException(status_code=400, detail="Verification code expired. Request a new one.")

    if req.code.strip() != stored_code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    await db.execute(
        "UPDATE users SET email_verified = 1, verification_code = NULL, verification_expires = NULL WHERE id = ?",
        (user["id"],),
    )
    await db.commit()
    return {"verified": True, "message": "Email verified successfully"}


@router.post("/resend-code")
async def resend_code(user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Generate and log a new verification code."""
    if user.get("email_verified"):
        return {"message": "Email already verified"}

    code = _generate_verification_code()
    expires = (datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat()

    await db.execute(
        "UPDATE users SET verification_code = ?, verification_expires = ? WHERE id = ?",
        (code, expires, user["id"]),
    )
    await db.commit()

    print(f"\n{'='*50}")
    print(f"  NEW VERIFICATION CODE for {user['email']}: {code}")
    print(f"  Expires in 30 minutes")
    print(f"{'='*50}\n")

    result = {"message": "New verification code sent"}
    if DEBUG:
        result["_dev_verification_code"] = code
    return result


@router.post("/guest", response_model=AuthResponse)
async def create_guest(db: aiosqlite.Connection = Depends(get_db)):
    """Create a guest user for the free audit flow. No email or password needed."""
    user_id = str(uuid.uuid4())
    guest_email = f"guest-{user_id[:8]}@visimind.local"

    await db.execute(
        """INSERT INTO users (id, email, password_hash, company_name, email_verified)
           VALUES (?, ?, ?, ?, 1)""",
        (user_id, guest_email, "guest", "Guest"),
    )
    await db.commit()

    token = create_token(user_id)
    return AuthResponse(
        token=token,
        user={
            "id": user_id,
            "email": guest_email,
            "company_name": "Guest",
            "company_url": "",
            "has_brand": False,
            "email_verified": True,
        },
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
        user={
            "id": user["id"],
            "email": user["email"],
            "company_name": user["company_name"],
            "company_url": user["company_url"],
            "has_brand": has_brand,
            "email_verified": bool(user["email_verified"]),
        },
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
        "email_verified": bool(user.get("email_verified", 0)),
    }

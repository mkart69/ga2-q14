
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import jwt, JWTError
from cryptography.hazmat.primitives import serialization

app = FastAPI()

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-g69cipc5.apps.exam.local"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
PASTE_THE_COMPLETE_PUBLIC_KEY_FROM_THE_QUESTION_HERE
-----END PUBLIC KEY-----"""


class TokenRequest(BaseModel):
    token: str


@app.post("/verify")
def verify_token(request: TokenRequest):
    try:
        claims = jwt.decode(
            request.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iss": True,
                "verify_aud": True,
            },
        )

        return {
            "valid": True,
            "email": claims.get("email"),
            "sub": claims.get("sub"),
            "aud": claims.get("aud"),
        }

    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail={"valid": False},
        )


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import jwt, JWTError
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-g69cipc5.apps.exam.local"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
PASTE_YOUR_COMPLETE_RSA_PUBLIC_KEY_HERE
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
        )

        return {
            "valid": True,
            "email": claims.get("email"),
            "sub": claims.get("sub"),
            "aud": claims.get("aud"),
        }

    except JWTError as e:
        logging.warning("JWT validation failed: %s", e)
        raise HTTPException(status_code=401, detail={"valid": False})

    except Exception:
        logging.exception("Unexpected verification error")
        raise HTTPException(status_code=500, detail={"valid": False})

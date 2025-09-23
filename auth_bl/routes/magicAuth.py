# main.py (FastAPI) - Fixed Version
import os
from urllib.parse import urlencode, quote
import logging

from auth_bl.services.magic_link_auth.magic_link_auth import create_magic_token, verify_magic_token, send_magic_link
from fastapi import HTTPException, Query, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
FRONTEND_BASE = os.getenv("FRONTEND_BASE", "https://frontendcou-smoky.vercel.app/")
# Public URL of your FastAPI service
BASE_URL = os.getenv("BASE_URL", "https://backendcou-3.onrender.com")
ROUTER_PREFIX = os.getenv("ROUTER_PREFIX", "/api/v1/magic-auth")
# Default verified page path on the frontend (configurable)
MAGIC_VERIFIED_PATH = os.getenv("MAGIC_VERIFIED_PATH", "auth/verified")

@router.get("/")
def health():
    return {"ok": True, "service": "magic-link"}

@router.post("/request-magic-link")
def request_magic_link(
    email_form: str | None = Form(default=None),
    email_query: str | None = Query(default=None, alias="email"),
    next: str | None = Form(default=None),  # Accept both form and query
    next_query: str | None = Query(default=None, alias="next"),
    request: Request = None
):
    """Request a magic link to be sent via email"""
    email = email_form or email_query
    next_url = next or next_query
    
    if not email:
        logger.error("No email provided in request")
        raise HTTPException(
            status_code=422,
            detail="Provide email as form field 'email_form' or query param 'email'",
        )

    logger.info(f"Creating magic link for email: {email}")
    
    try:
        token = create_magic_token(email)
        logger.info(f"Token created successfully for {email}")
    except Exception as e:
        logger.error(f"Failed to create token: {e}")
        raise HTTPException(status_code=500, detail="Failed to create magic token")

    # Ensure we have a default next URL that is mobile-friendly (frontend verified page)
    if not next_url:
        frontend_base = FRONTEND_BASE if FRONTEND_BASE.endswith("/") else f"{FRONTEND_BASE}/"
        next_url = f"{frontend_base}{MAGIC_VERIFIED_PATH}"

    # Build the verification URL with proper parameters
    verify_params = {
        "token": token,
        "redirect": "true",  # Always redirect to next_url for better mobile UX
        "next": next_url,
    }

    # Properly encode the query parameters
    query_string = urlencode(verify_params, safe=':/?&=')
    magic_link = f"{BASE_URL}{ROUTER_PREFIX}/verify-magic-link?{query_string}"
    
    logger.info(f"Magic link created: {magic_link}")

    try:
        send_magic_link(email, magic_link)
        logger.info(f"Magic link sent successfully to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    return JSONResponse({
        "message": f"Magic link sent to {email}",
        "success": True
    })

@router.get("/verify-magic-link")
def verify_magic_link(
    token: str,
    redirect: bool = Query(default=False),
    next: str | None = Query(default=None)
):
    """Verify the magic link token and optionally redirect"""
    logger.info(f"Verifying magic link with token: {token[:10]}...")
    
    try:
        email = verify_magic_token(token)
        logger.info(f"Token verified successfully for email: {email}")
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid or expired magic link")

    # If redirect is requested, redirect to provided next or default verified page
    if redirect:
        try:
            redirect_target = next
            if not redirect_target:
                frontend_base = FRONTEND_BASE if FRONTEND_BASE.endswith("/") else f"{FRONTEND_BASE}/"
                redirect_target = f"{frontend_base}{MAGIC_VERIFIED_PATH}"
            # Construct redirect URL with email parameter
            separator = "&" if "?" in redirect_target else "?"
            redirect_url = f"{redirect_target}{separator}email={quote(email)}&verified=true"
            logger.info(f"Redirecting to: {redirect_url}")
            return RedirectResponse(url=redirect_url, status_code=302)
        except Exception as e:
            logger.error(f"Redirect failed: {e}")
            return JSONResponse({
                "message": "Login verified but redirect failed",
                "email": email,
                "error": str(e)
            }, status_code=200)

    return JSONResponse({
        "message": "Login verified",
        "email": email,
        "success": True
    })
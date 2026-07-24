"""
Weblytic Solutions — Marketing Website
========================================
A production-ready FastAPI + Jinja2 + Tailwind CSS website.

Run locally:
    pip install -r requirements.txt
    uvicorn main:app --reload

Then visit http://127.0.0.1:8000
"""

import json
import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Weblytic Solutions",
    description="Official website of Weblytic Solutions — Web Design, Development & Digital Support.",
    version="1.0.0",
)

# Mount static files (CSS, images, JS)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Where submitted contact form data will be stored (simple JSON file "DB")
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
CONTACTS_FILE = DATA_DIR / "contacts.json"


def save_contact_submission(data: dict) -> None:
    """Append a contact form submission to a local JSON file.

    This is intentionally simple (no database) as requested — it stores
    submissions so they can be reviewed later, and also prints them to the
    server console/log for immediate visibility.
    """
    data["submitted_at"] = datetime.utcnow().isoformat() + "Z"

    # Print to console/log so it's visible during local dev or on host logs
    print("=" * 60)
    print("NEW CONTACT FORM SUBMISSION")
    print(json.dumps(data, indent=2))
    print("=" * 60)

    # Load existing submissions (if any), append, and save back
    existing = []
    if CONTACTS_FILE.exists():
        try:
            existing = json.loads(CONTACTS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            existing = []

    existing.append(data)
    CONTACTS_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Shared context (available to every template via base.html)
# ---------------------------------------------------------------------------

COMPANY = {
    "name": "Weblytic Solutions",
    "tagline": "Modern Websites. Real Business Results.",
    "email": "hello@weblyticsolutions.com",
    "phone": "+91 98765 43210",
    "address": "Ahmedabad, Gujarat, India",
    "year": datetime.now().year,
}


def get_base_context(request: Request, active_page: str) -> dict:
    """Helper to build the common context dict every page needs."""
    return {
        "request": request,
        "company": COMPANY,
        "active_page": active_page,
    }


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=None)
async def home(request: Request):
    """Home page — hero, services overview, why us, testimonials, CTA."""
    context = get_base_context(request, "home")
    return templates.TemplateResponse("index.html", context)


@app.get("/about")
async def about(request: Request):
    """About Us — story, mission, vision, team, values."""
    context = get_base_context(request, "about")
    return templates.TemplateResponse("about.html", context)


@app.get("/services")
async def services(request: Request):
    """Services — detailed breakdown of all offerings."""
    context = get_base_context(request, "services")
    return templates.TemplateResponse("services.html", context)


@app.get("/portfolio")
async def portfolio(request: Request):
    """Portfolio / Work — grid of past project case studies."""
    context = get_base_context(request, "portfolio")
    return templates.TemplateResponse("portfolio.html", context)


@app.get("/pricing")
async def pricing(request: Request):
    """Pricing — Starter, Professional, Enterprise packages."""
    context = get_base_context(request, "pricing")
    return templates.TemplateResponse("pricing.html", context)


@app.get("/contact")
async def contact(request: Request):
    """Contact — form + company details + map placeholder."""
    context = get_base_context(request, "contact")
    return templates.TemplateResponse("contact.html", context)


@app.post("/contact")
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    company_name: str = Form(""),
    service_interested: str = Form(""),
    message: str = Form(...),
):
    """Handle contact form submission.

    Saves the submission locally (JSON file + console log) and redirects
    the visitor to a friendly success page.
    """
    save_contact_submission(
        {
            "name": name,
            "email": email,
            "phone": phone,
            "company_name": company_name,
            "service_interested": service_interested,
            "message": message,
        }
    )
    # Redirect (Post/Redirect/Get pattern) to avoid re-submission on refresh
    return RedirectResponse(url="/contact/success", status_code=303)


@app.get("/contact/success")
async def contact_success(request: Request):
    """Simple success page shown after a contact form submission."""
    context = get_base_context(request, "contact")
    return templates.TemplateResponse("contact_success.html", context)


# ---------------------------------------------------------------------------
# Simple 404 handler (kept minimal, styled to match site)
# ---------------------------------------------------------------------------

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    context = get_base_context(request, "")
    return templates.TemplateResponse("404.html", context, status_code=404)


# ---------------------------------------------------------------------------
# Local dev entrypoint (optional — `uvicorn main:app --reload` is preferred)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

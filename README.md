# Weblytic Solutions — Website

A complete, production-ready marketing website for **Weblytic Solutions**, built with:

- **Backend:** FastAPI (Python)
- **Templating:** Jinja2
- **Styling:** Tailwind CSS (via CDN) — navy + white + soft blue palette
- **No React / Next.js / Node.js** — pure Python + HTML

---

## 1. Folder Structure

```
weblytic-solutions/
├── main.py                     # FastAPI app + all routes
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/
│   └── contacts.json           # Auto-created — stores contact form submissions
├── static/
│   ├── css/
│   │   └── style.css           # Small custom CSS on top of Tailwind
│   └── images/                 # (empty — add real images here if desired)
└── templates/
    ├── base.html                # Shared layout: header, nav, footer
    ├── index.html                # Home page
    ├── about.html                # About Us page
    ├── services.html             # Services page
    ├── portfolio.html            # Portfolio / Work page
    ├── pricing.html               # Pricing page
    ├── contact.html               # Contact page (form)
    ├── contact_success.html       # Success page after form submit
    └── 404.html                   # Custom 404 page
```

---

## 2. Run Locally

**Requirements:** Python 3.9+

```bash
# 1. Navigate into the project folder
cd weblytic-solutions

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server
uvicorn main:app --reload

# 5. Open your browser at:
http://127.0.0.1:8000
```

That's it — all 7 pages, shared header/footer, and the working contact form are live locally.

### Where contact form submissions go
When someone submits the contact form, Weblytic Solutions:
1. Prints the submission to your terminal/console (visible immediately during local dev).
2. Appends it as JSON to `data/contacts.json` (auto-created on first submission).
3. Redirects the visitor to a friendly `/contact/success` page.

This is intentionally simple (no external database needed) — perfect for getting started, and easy to swap for a real database or email service later (see "Next steps" below).

---

## 3. Deploy to Render.com (Free Tier) — Step by Step

Render is the simplest option for a FastAPI app like this one.

### Step 1 — Push your code to GitHub
1. Create a new GitHub repository (e.g. `weblytic-solutions`).
2. Push this entire `weblytic-solutions/` folder to that repo:
   ```bash
   cd weblytic-solutions
   git init
   git add .
   git commit -m "Initial commit — Weblytic Solutions website"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/weblytic-solutions.git
   git push -u origin main
   ```

### Step 2 — Create a new Web Service on Render
1. Go to [https://render.com](https://render.com) and sign up / log in (you can sign in with GitHub).
2. Click **New +** → **Web Service**.
3. Connect your GitHub account and select the `weblytic-solutions` repository.
4. Fill in the settings:
   - **Name:** `weblytic-solutions` (or any name you like)
   - **Region:** choose the one closest to your target users
   - **Branch:** `main`
   - **Root Directory:** leave blank (unless you nested the folder)
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type:** `Free`
5. Click **Create Web Service**.

### Step 3 — Wait for deployment
Render will install dependencies and start your app. Once you see **"Live"** at the top, your site is online at a URL like:

```
https://weblytic-solutions.onrender.com
```

> **Note on the free tier:** Render's free web services "spin down" after periods of inactivity and take ~30–60 seconds to wake up on the next visit. This is fine for a small business site; upgrade to a paid instance later if you want zero cold-start delay.

### Step 4 (Optional) — Persisting contact form data
Render's free tier has an **ephemeral filesystem** — meaning `data/contacts.json` will reset whenever the service restarts or redeploys. For a production business site, we recommend either:
- Connecting a free tier database (e.g. Render's free PostgreSQL, or a service like Supabase), or
- Sending form submissions via email (e.g. using an SMTP service or an API like Resend/SendGrid) instead of / in addition to saving to a file.

Both are straightforward additions to the `contact_submit()` function in `main.py` whenever you're ready.

---

## 4. Alternative: Deploy to Railway.app

If you prefer Railway instead of Render:

1. Push your code to GitHub (same as Step 1 above).
2. Go to [https://railway.app](https://railway.app) and log in with GitHub.
3. Click **New Project** → **Deploy from GitHub repo** → select your repository.
4. Railway auto-detects Python. Under the service **Settings**:
   - **Start Command:**
     ```
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
5. Click **Deploy**. Railway will build and give you a live URL such as:
   ```
   https://weblytic-solutions-production.up.railway.app
   ```

Railway's free tier includes a small monthly usage credit rather than the "sleep on inactivity" model — pick whichever platform's free-tier trade-offs suit you better.

---

## 5. Connecting Your Own Domain (e.g. weblyticsolutions.com)

Once deployed on Render or Railway:

### On Render:
1. Open your Web Service → **Settings** → **Custom Domains**.
2. Click **Add Custom Domain** and enter your domain (e.g. `www.weblyticsolutions.com`).
3. Render will show you a CNAME (or A) record to add at your domain registrar (GoDaddy, Namecheap, Google Domains, etc.):
   - Type: `CNAME`
   - Name: `www`
   - Value: `weblytic-solutions.onrender.com` (your Render URL)
4. If you also want the bare domain (`weblyticsolutions.com` without `www`), Render will give you an **A record** pointing to their IP — add that too at your registrar.
5. Wait for DNS propagation (a few minutes up to 24–48 hours). Render automatically issues a free SSL certificate (HTTPS) once the domain is verified.

### On Railway:
1. Open your project → the service → **Settings** → **Networking** → **Custom Domain**.
2. Enter your domain and Railway will show you the CNAME record to add at your registrar.
3. Add the record, wait for DNS propagation, and Railway will auto-provision SSL.

### Buying a domain
If you don't already own `weblyticsolutions.com` (or similar), you can register one through:
- Namecheap, GoDaddy, Google Domains, or Cloudflare Registrar — typically $10–15/year for a `.com`.

---

## 6. Customizing Content Later

- **Company details** (email, phone, address, year) are centralized in the `COMPANY` dictionary at the top of `main.py` — update once, and it reflects everywhere (footer, contact page, etc.).
- **Page copy** lives directly in each template under `templates/` — all plain HTML with Jinja2, easy to edit.
- **Colors** are defined in the `tailwind.config` script block inside `templates/base.html` under `navy` and `skyblue` — adjust hex values there to re-theme the whole site instantly.
- **Real project images**: replace the gradient placeholder blocks in `portfolio.html` with `<img>` tags pointing to files placed in `static/images/`.
- **Map embed**: replace the map placeholder block in `contact.html` with a real Google Maps iframe embed once you have your exact business address indexed on Google Maps.

---

## 7. Tech Notes

- Tailwind is loaded via CDN (`<script src="https://cdn.tailwindcss.com">`) — no build step needed, works out of the box. For a heavier-traffic production site later, you could migrate to a compiled Tailwind build for slightly faster load times, but the CDN approach is perfectly fine for this use case.
- The site is fully responsive (mobile-first) using Tailwind's `sm:`, `lg:` breakpoints throughout.
- Basic SEO meta tags (title, description, Open Graph) are set per-page via Jinja2 `{% block %}` overrides in each template.
- Contact form uses the POST → Redirect → GET pattern, so refreshing the success page never re-submits the form.

---

Built for **Weblytic Solutions** — Ahmedabad, India.

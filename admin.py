"""Admin + academy dashboards. Reachable by URL only (no links anywhere on the site).

/admin                 -> create academy accounts (gated by ADMIN_PASSWORD in .env)
/admin/<ACRONYM>       -> create student accounts (gated by that academy's email + password,
                          or by an admin session)
"""
import hmac
import os
import re
from collections import Counter
from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from supabase_client import get_supabase

bp = Blueprint("admin", __name__, url_prefix="/admin")

ACRONYM_RE = re.compile(r"^[A-Za-z0-9]{2,10}$")
RESERVED = {"LOGIN", "LOGOUT", "ACADEMIES"}  # clash with fixed /admin/... routes
MIN_PW = 6


def db():
    client = get_supabase()
    if client is None:
        abort(503, "Supabase is not configured. Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env.")
    return client


def is_admin():
    return session.get("admin") is True


def has_access(acronym):
    return is_admin() or session.get("academy") == acronym


def admin_required(view):
    @wraps(view)
    def wrapped(*a, **kw):
        if not is_admin():
            return redirect(url_for("admin.dashboard"))
        return view(*a, **kw)
    return wrapped


def load_academy(acr):
    rows = db().table("academies").select("*").eq("acronym", acr.upper()).limit(1).execute().data
    if not rows:
        abort(404)
    return rows[0]


def friendly(err):
    text = str(err)
    if "23505" in text or "duplicate" in text.lower():
        return "That acronym or email is already registered."
    return f"Could not save: {text}"


# ------------------------------------------------------------------ /admin
@bp.route("/", strict_slashes=False)
def dashboard():
    if not is_admin():
        return render_template("admin_login.html", heading="Admin sign-in", label="Admin password",
                               action=url_for("admin.login"), email_field=False)
    c = db()
    academies = (c.table("academies").select("id,name,acronym,email,created_at")
                 .order("created_at", desc=True).execute().data)
    counts = Counter(r["academy_id"] for r in c.table("students").select("academy_id").execute().data)
    for a in academies:
        a["students"] = counts.get(a["id"], 0)
    return render_template("admin_dashboard.html", academy=None, rows=academies,
                           total_academies=len(academies), total_students=sum(counts.values()))


@bp.post("/login")
def login():
    expected = os.environ.get("ADMIN_PASSWORD", "")
    given = request.form.get("password", "")
    if expected and hmac.compare_digest(given.encode(), expected.encode()):
        session["admin"] = True
    else:
        flash("Incorrect admin password." if expected else "ADMIN_PASSWORD is not set in .env.", "error")
    return redirect(url_for("admin.dashboard"))


@bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


@bp.post("/academies")
@admin_required
def create_academy():
    name = request.form.get("name", "").strip()
    acronym = request.form.get("acronym", "").strip().upper()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    if not name or not email:
        flash("Academy name and email are required.", "error")
    elif not ACRONYM_RE.match(acronym) or acronym in RESERVED:
        flash("Acronym must be 2-10 letters or numbers (and not a reserved word).", "error")
    elif len(password) < MIN_PW:
        flash(f"Password must be at least {MIN_PW} characters.", "error")
    else:
        c = db()
        try:
            c.table("academies").insert({"name": name, "acronym": acronym, "email": email,
                                         "password_hash": generate_password_hash(password)}).execute()
            flash(f"Academy {name} ({acronym}) created.", "success")
        except Exception as e:
            flash(friendly(e), "error")
    return redirect(url_for("admin.dashboard"))


@bp.post("/academies/<academy_id>/delete")
@admin_required
def delete_academy(academy_id):
    c = db()
    try:
        c.table("academies").delete().eq("id", academy_id).execute()  # students cascade
        flash("Academy and its students deleted.", "success")
    except Exception as e:
        flash(friendly(e), "error")
    return redirect(url_for("admin.dashboard"))


# ------------------------------------------------------- /admin/<acronym>
@bp.route("/<acr>", strict_slashes=False)
def academy(acr):
    a = load_academy(acr)
    if not has_access(a["acronym"]):
        return render_template("admin_login.html", heading=f"{a['name']} sign-in", label="Academy password",
                               action=url_for("admin.academy_login", acr=a["acronym"]), email_field=True)
    a.pop("password_hash", None)
    students = (db().table("students").select("id,name,email,created_at").eq("academy_id", a["id"])
                .order("created_at", desc=True).execute().data)
    return render_template("admin_dashboard.html", academy=a, rows=students)


@bp.post("/<acr>/login")
def academy_login(acr):
    a = load_academy(acr)
    email = request.form.get("email", "").strip().lower()
    if email == a["email"] and check_password_hash(a["password_hash"], request.form.get("password", "")):
        session["academy"] = a["acronym"]
    else:
        flash("Incorrect academy email or password.", "error")
    return redirect(url_for("admin.academy", acr=a["acronym"]))


@bp.route("/<acr>/logout")
def academy_logout(acr):
    session.pop("academy", None)
    return redirect(url_for("admin.academy", acr=acr.upper()))


@bp.post("/<acr>/students")
def create_student(acr):
    a = load_academy(acr)
    if not has_access(a["acronym"]):
        abort(403)
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    if not name or not email:
        flash("Student name and email are required.", "error")
    elif len(password) < MIN_PW:
        flash(f"Password must be at least {MIN_PW} characters.", "error")
    else:
        c = db()
        try:
            c.table("students").insert({"academy_id": a["id"], "name": name, "email": email,
                                        "password_hash": generate_password_hash(password)}).execute()
            flash(f"Student account created for {name}.", "success")
        except Exception as e:
            flash("That student email is already registered." if "23505" in str(e) or "duplicate" in str(e).lower()
                  else friendly(e), "error")
    return redirect(url_for("admin.academy", acr=a["acronym"]))


@bp.post("/<acr>/students/<student_id>/delete")
def delete_student(acr, student_id):
    a = load_academy(acr)
    if not has_access(a["acronym"]):
        abort(403)
    c = db()
    try:
        c.table("students").delete().eq("id", student_id).eq("academy_id", a["id"]).execute()
        flash("Student account deleted.", "success")
    except Exception as e:
        flash(friendly(e), "error")
    return redirect(url_for("admin.academy", acr=a["acronym"]))
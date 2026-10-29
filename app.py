import copy
import os
import re
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from markupsafe import Markup, escape
from lesson_content import LESSON_CONTENT, get_module_videos
from supabase_client import get_supabase, get_supabase_video_url

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "nma-secret-key-australia-2026")

STATS = [("users", "12,000+", "Students taught"), ("award", "25+ yrs", "Teaching excellence"),
         ("star", "4.9/5", "Average rating"), ("clock", "98%", "Complete their course")]
WHY = [("piano", "Personalised One-on-One Lessons", "Live video lessons tailored to your pace, goals, and musical taste — never generic."),
       ("heart", "Patient, World-Class Instructors", "Learn from ARIA-nominated pianists and conservatorium graduates who specialise in learners of all levels."),
       ("trophy", "Structured Progress & Grading", "Follow the AMEB & ABRSM syllabus with optional exams, or learn purely for joy."),
       ("calendar", "Flexible Scheduling", "Book lessons around your life. Reschedule anytime with 24 hours’ notice — no lock-in contracts.")]
STEPS = [("pointer", "01", "Enrol in 60 seconds", "Complete the form and a course advisor calls you within 24 hours to understand your goals."),
         ("calcheck", "02", "Get matched & schedule", "We pair you with the ideal instructor and book your first live lesson at a time that suits you."),
         ("music", "03", "Play from your first lesson", "Your instructor builds a personalised roadmap. You’ll play a real piece in session one.")]
TESTIMONIALS = [("I started as a complete beginner at 52. Eighteen months later I performed at the Academy’s recital. National Music Academy gave me a part of myself back.", "Margaret D.", "Adult learner · Foundation → Conservatoire"),
                ("My daughter went from reluctant practiser to begging for more lessons. She passed her AMEB Grade 4 with Honours.", "David & Mei L.", "Parents of student · Conservatoire level"),
                ("After years of self-teaching and hitting a wall, the Virtuoso course broke me through. I’m now preparing for my Associate Diploma.", "Thomas R.", "Virtuoso level · AMEB Associate candidate")]
PLANS = [dict(name="Single Lesson", blurb="Perfect for trying us out or occasional guidance.", price="$65", unit="per lesson", cta="Book a Lesson", featured=False,
              features=["1 × 45-minute live lesson", "Personalised feedback notes", "Reschedule up to 24 hrs prior", "No ongoing commitment"]),
         dict(name="Term enrolment", blurb="Our most popular path — consistent progress, best value.", price="$49", unit="per lesson (billed termly)", cta="Enrol This Term", featured=True,
              features=["10 × 45-minute live lessons per term", "Personalised practice roadmap", "Optional AMEB/ABRSM exam entry", "Free recital participation", "Save 25% vs single lessons"]),
         dict(name="Accelerator", blurb="Two lessons weekly for rapid, focused advancement.", price="$89", unit="per lesson (billed weekly)", cta="Start Accelerating", featured=False,
              features=["2 × live lessons per week", "Priority instructor matching", "Personalised practice roadmap", "Exam & recital preparation", "Direct messaging with instructor"])]
FAQS = [("Do I need any prior experience or a piano at home?", "No experience is needed — we welcome complete beginners through to advanced players."),
        ("Are lessons suitable for both children and adults?", "Yes. Lessons are suitable for ages 7+ and adults, tailored to each learner."),
        ("How do online lessons actually work?", "Lessons are live one-on-one video sessions with your instructor — never pre-recorded."),
        ("Can I prepare for AMEB or ABRSM exams through this course?", "Yes. Our structured curriculum follows both syllabi, with optional exam entry."),
        ("What if I need to reschedule a lesson?", "You can reschedule anytime with 24 hours’ notice."),
        ("Is there a lock-in contract?", "No. Cancel anytime — no contracts, no hidden fees.")]

DEFAULT_STUDENT = {
    "name": "Eleanor Whitfield",
    "first": "Eleanor",
    "initials": "EW",
    "level": "Conservatoire Level",
    "enrolled": "March 2026",
    "email": "eleanor@example.com"
}
ACTIVE_LESSONS = {1, 5, 10}

_L = [
    (1, "Introduction to the Piano", "Getting Started with Keys, Fingers & Rhythm", "Learn finger numbers, navigate the black and white notes, name the musical alphabet, and play your first rhythms.", 18, "Dr. Margaret Holloway", "done"),
    (2, "Foundations of Technique", "Reading the Treble Clef", "Learn to identify notes on the treble staff, understand ledger lines, and sight-read simple melodies.", 22, "Dr. Margaret Holloway", "done"),
    (3, "Foundations of Technique", "Reading the Bass Clef", "Master the bass clef staff, recognise intervals, and coordinate both hands reading simultaneously.", 20, "Dr. Margaret Holloway", "done"),
    (4, "Scales & Arpeggios", "C Major Scale — One Octave", "Learn the C major scale with correct fingering, thumb-under technique, and even tone production.", 25, "James Chen", "done"),
    (5, "Scales & Arpeggios", "G Major Scale & The Fingering Principle", "Apply the fingering principle to G major, understand the F# requirement, and build muscle memory.", 27, "James Chen", "current"),
    (6, "Scales & Arpeggios", "Two-Octave Scales & Tempo", "Extend scales to two octaves, introduce metronome practice at 60–80 BPM, and develop hand coordination.", 30, "James Chen", "todo"),
    (7, "Scales & Arpeggios", "Broken Chords & Arpeggio Form", "Transition from solid chords to broken chord patterns and introductory arpeggio exercises.", 24, "James Chen", "todo"),
    (8, "Repertoire: Debussy", "Clair de Lune — Section A", "Begin Debussy’s masterpiece. Focus on the opening theme, rubato phrasing, and delicate touch.", 35, "Sophia Laurent", "todo"),
    (9, "Repertoire: Debussy", "Clair de Lune — Section B & Voicing", "Tackle the middle section with its rolling arpeggios, melodic voicing, and dynamic control.", 38, "Sophia Laurent", "todo"),
    (10, "Repertoire: Debussy", "Pedalling Technique for Debussy", "Master half-pedalling, flutter pedalling, and sustain techniques that give Debussy’s works resonance.", 29, "Sophia Laurent", "todo"),
]
LESSONS = [dict(zip(("num", "topic", "title", "desc", "minutes", "instructor", "status"), l)) for l in _L]
MODULES = []
for l in LESSONS:
    if not MODULES or MODULES[-1]["title"] != l["topic"]:
        MODULES.append(dict(n=len(MODULES) + 1, title=l["topic"], total=0, done=0))
    MODULES[-1]["total"] += 1
    MODULES[-1]["done"] += l["status"] == "done"
for m in MODULES:
    m["pct"] = round(100 * m["done"] / m["total"])

WEEK = [("Mon", 30), ("Tue", 25), ("Wed", 45), ("Thu", 0), ("Fri", 30), ("Sat", 15), ("Sun", 0)]
SKILLS = [("Technique", 82), ("Sight-Reading", 64), ("Repertoire", 38), ("Aural Skills", 55), ("Theory", 71)]
NOTIFICATIONS = [
    dict(id="n1", title="Live lesson on Thursday", text="Your session with Sophia Laurent starts at 7:00 AM.", time="Today"),
    dict(id="n2", title="New feedback from James Chen", text="Notes for G Major Scale are ready.", time="Yesterday"),
    dict(id="n3", title="35 minutes to your weekly goal", text="You’re at 145 of 180 practice minutes this week.", time="Yesterday"),
    dict(id="n4", title="Welcome to the NMA Portal", text="Explore your lessons and track your progress here.", time="3 days ago"),
]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def media_url(num, name, exts):
    """Fallback local static media if present."""
    for ext in exts:
        if os.path.exists(os.path.join(app.static_folder, "media", f"lesson{num}", name + ext)):
            return url_for("static", filename=f"media/lesson{num}/{name}{ext}")
    return ""


def with_media(num, content):
    """Resolves media URLs: Supabase public URLs first, then local static media fallback."""
    c = copy.deepcopy(content)
    if not c.get("sheet_music"):
        c["sheet_music"] = media_url(num, "sheet-music", (".pdf",))
    for part in c.get("parts", []):
        for sct in part.get("sections", []):
            name = slug(sct["heading"])
            if sct.get("video") is not None and not sct["video"].get("url"):
                # Check Supabase Storage first
                supabase_url = get_supabase_video_url(f"lesson{num}/{name}.mp4")
                if supabase_url:
                    sct["video"]["url"] = supabase_url
                else:
                    sct["video"]["url"] = media_url(num, name, (".mp4", ".webm", ".mov"))
            if sct.get("audio") is not None and not sct["audio"].get("url"):
                sct["audio"]["url"] = media_url(num, name, (".mp3", ".wav", ".m4a", ".ogg"))
            if sct.get("download") is not None and not sct["download"].get("url"):
                sct["download"]["url"] = media_url(num, slug(sct["download"]["label"]), (".pdf", ".zip"))
    return c


def get_current_student():
    user = session.get("user")
    if isinstance(user, dict):
        full_name = user.get("name") or "Student"
        first = user.get("first") or full_name.split()[0]
        initials = user.get("initials") or "".join(part[0].upper() for part in full_name.split()[:2]) or "ST"
        return {
            "name": full_name,
            "first": first,
            "initials": initials,
            "level": user.get("level", "Conservatoire Level"),
            "enrolled": user.get("enrolled", "October 2026"),
            "email": user.get("email", ""),
        }
    return DEFAULT_STUDENT


@app.template_filter("md")
def md(text):
    t = str(escape(text))
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r'<code class="rounded bg-[var(--secondary)] px-1.5 py-0.5 text-[13px]">\1</code>', t)
    return Markup(t)


@app.context_processor
def inject_notifications():
    return dict(notifications=NOTIFICATIONS)


def login_required(view):
    @wraps(view)
    def wrapped(*a, **kw):
        if not session.get("user"):
            return redirect(url_for("login"))
        return view(*a, **kw)
    return wrapped


@app.route("/")
def index():
    return render_template("index.html", stats=STATS, why=WHY, steps=STEPS,
                           testimonials=TESTIMONIALS, plans=PLANS, faqs=FAQS)


@app.post("/enroll")
def enroll():
    flash("Thanks! A course advisor will contact you within 24 hours.", "success")
    return redirect(url_for("index") + "#enroll")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user"):
        return redirect(url_for("portal_dashboard"))

    if request.method == "POST":
        full_name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return render_template("register.html")

        client = get_supabase()
        if client:
            try:
                res = client.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {"full_name": full_name or email.split("@")[0].capitalize()}
                    }
                })
                if res.user:
                    user_name = full_name or email.split("@")[0].capitalize()
                    session["user"] = {
                        "id": res.user.id,
                        "email": res.user.email,
                        "name": user_name,
                        "first": user_name.split()[0],
                        "initials": "".join(p[0].upper() for p in user_name.split()[:2]),
                        "level": "Conservatoire Level",
                        "enrolled": "October 2026"
                    }
                    flash(f"Welcome to National Music Academy, {user_name.split()[0]}!", "success")
                    return redirect(url_for("portal_dashboard"))
                else:
                    flash("Registration submitted! Please sign in.", "success")
                    return redirect(url_for("login"))
            except Exception as e:
                flash(f"Supabase Sign-Up Error: {e}", "error")
                return render_template("register.html")
        else:
            # Fallback local demo registration when keys are not yet configured
            user_name = full_name or email.split("@")[0].capitalize()
            session["user"] = {
                "id": "demo-local-id",
                "email": email,
                "name": user_name,
                "first": user_name.split()[0],
                "initials": "".join(p[0].upper() for p in user_name.split()[:2]),
                "level": "Conservatoire Level",
                "enrolled": "October 2026"
            }
            flash(f"Demo Mode: Account created for {user_name} (Connect Supabase in .env for production auth)", "info")
            return redirect(url_for("portal_dashboard"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("portal_dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        client = get_supabase()
        if client:
            try:
                res = client.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                if res.user:
                    meta = getattr(res.user, "user_metadata", {}) or {}
                    full_name = meta.get("full_name") or email.split("@")[0].capitalize()
                    session["user"] = {
                        "id": res.user.id,
                        "email": res.user.email,
                        "name": full_name,
                        "first": full_name.split()[0],
                        "initials": "".join(p[0].upper() for p in full_name.split()[:2]),
                        "level": "Conservatoire Level",
                        "enrolled": "October 2026"
                    }
                    flash(f"Welcome back, {full_name.split()[0]}!", "success")
                    return redirect(url_for("portal_dashboard"))
                else:
                    flash("Invalid credentials. Please try again.", "error")
            except Exception as e:
                flash(f"Sign In Error: {e}", "error")
        else:
            # Demo fallback when Supabase keys are not yet provided
            user_name = email.split("@")[0].capitalize() if "@" in email else "Eleanor Whitfield"
            session["user"] = {
                "id": "demo-id",
                "email": email or "eleanor@example.com",
                "name": user_name,
                "first": user_name.split()[0],
                "initials": "".join(p[0].upper() for p in user_name.split()[:2]),
                "level": "Conservatoire Level",
                "enrolled": "March 2026"
            }
            flash("Signed in using demo fallback mode. Configure Supabase in .env to use live cloud auth.", "info")
            return redirect(url_for("portal_dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    client = get_supabase()
    if client:
        try:
            client.auth.sign_out()
        except Exception:
            pass
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("index"))


@app.route("/portal/dashboard")
@login_required
def portal_dashboard():
    student = get_current_student()
    current = next(l for l in LESSONS if l["status"] == "current")
    done = sum(l["status"] == "done" for l in LESSONS)
    return render_template("dashboard.html", student=student, modules=MODULES, current=current,
                           done=done, total=len(LESSONS), pct=round(100 * done / len(LESSONS)))


@app.route("/portal/lessons")
@login_required
def portal_lessons():
    student = get_current_student()
    done = sum(l["status"] == "done" for l in LESSONS)
    return render_template("lessons.html", student=student, lessons=LESSONS, active=ACTIVE_LESSONS, done=done)


@app.route("/portal/lessons/<int:num>")
@login_required
def portal_lesson(num):
    lesson = next((l for l in LESSONS if l["num"] == num), None)
    if lesson is None:
        abort(404)
    if num not in ACTIVE_LESSONS:
        return redirect(url_for("portal_lessons"))
    student = get_current_student()
    content = with_media(num, LESSON_CONTENT.get(num, {}))
    module_videos = get_module_videos(num)
    return render_template("lesson.html", student=student, lesson=lesson, content=content, module_videos=module_videos)


@app.route("/portal/progress")
@login_required
def portal_progress():
    student = get_current_student()
    done = sum(l["status"] == "done" for l in LESSONS)
    return render_template("progress.html", student=student, lessons=LESSONS, week=WEEK, skills=SKILLS,
                           done=done, total=len(LESSONS), pct=round(100 * done / len(LESSONS)),
                           week_total=sum(m for _, m in WEEK))


if __name__ == "__main__":
    app.run(debug=True)
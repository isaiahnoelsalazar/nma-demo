import os
import re
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from markupsafe import Markup, escape
from lesson_content import LESSON_CONTENT

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")

STATS = [("users", "12,000+", "Students taught"), ("award", "25+ yrs", "Teaching excellence"),
         ("star", "4.9/5", "Average rating"), ("clock", "98%", "Complete their course")]
WHY = [("piano", "Personalised One-on-One Lessons", "Live video lessons tailored to your pace, goals, and musical taste — never pre-recorded, never generic."),
       ("heart", "Patient, World-Class Instructors", "Learn from ARIA-nominated pianists and conservatorium graduates who specialise in adult and child learners alike."),
       ("trophy", "Structured Progress & Grading", "Follow the AMEB & ABRSM syllabus with optional exams, or learn purely for joy. You set the destination."),
       ("calendar", "Flexible Scheduling", "Book lessons around your life. Reschedule anytime with 24 hours’ notice — no lock-in contracts.")]
STEPS = [("pointer", "01", "Enrol in 60 seconds", "Complete the form and a course advisor calls you within 24 hours to understand your goals."),
         ("calcheck", "02", "Get matched & schedule", "We pair you with the ideal instructor and book your first live lesson at a time that suits you."),
         ("music", "03", "Play from your first lesson", "Your instructor builds a personalised roadmap. You’ll play a real piece in session one — guaranteed.")]
TESTIMONIALS = [("I started as a complete beginner at 52. Eighteen months later I performed at the Academy’s recital. National Music Academy didn’t just teach me piano — they gave me a part of myself back.", "Margaret D.", "Adult learner · Foundation → Conservatoire"),
                ("My daughter went from reluctant practiser to begging for more lessons. The instructor’s patience and structure made all the difference. She passed her AMEB Grade 4 with Honours.", "David & Mei L.", "Parents of student · Conservatoire level"),
                ("After years of self-teaching and hitting a wall, the Virtuoso course broke me through. I’m now preparing for my Associate Diploma and couldn’t be more grateful.", "Thomas R.", "Virtuoso level · AMEB Associate candidate")]
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


@app.route("/")
def index():
    return render_template("index.html", stats=STATS, why=WHY, steps=STEPS,
                           testimonials=TESTIMONIALS, plans=PLANS, faqs=FAQS)


@app.post("/enroll")
def enroll():
    # TODO: save request.form (firstName, lastName, email, phone, level) to your database / CRM
    flash("Thanks! A course advisor will contact you within 24 hours.", "success")
    return redirect(url_for("index") + "#enroll")


STUDENT = dict(name="Eleanor Whitfield", first="Eleanor", initials="EW", level="Conservatoire Level", enrolled="March 2026")
ACTIVE_LESSONS = {1, 5, 10}  # all other lessons are greyed out as "Coming soon"
_L = [  # (number, topic, title, description, minutes, instructor, status)
    (1, "Introduction to the Piano", "Getting Started with Keys, Fingers & Rhythm", "Learn finger numbers, navigate the black and white notes, name the musical alphabet, and play your first rhythms with crotchets and minims.", 18, "Dr. Margaret Holloway", "done"),
    (2, "Foundations of Technique", "Reading the Treble Clef", "Learn to identify notes on the treble staff, understand ledger lines, and sight-read simple melodies with confidence.", 22, "Dr. Margaret Holloway", "done"),
    (3, "Foundations of Technique", "Reading the Bass Clef", "Master the bass clef staff, recognise intervals, and coordinate both hands reading simultaneously.", 20, "Dr. Margaret Holloway", "done"),
    (4, "Scales & Arpeggios", "C Major Scale — One Octave", "Learn the C major scale with correct fingering, thumb-under technique, and even tone production across one octave.", 25, "James Chen", "done"),
    (5, "Scales & Arpeggios", "G Major Scale & The Fingering Principle", "Apply the fingering principle to G major, understand the F# requirement, and build muscle memory for sharp-key scales.", 27, "James Chen", "current"),
    (6, "Scales & Arpeggios", "Two-Octave Scales & Tempo", "Extend scales to two octaves, introduce metronome practice at 60–80 BPM, and develop hand coordination.", 30, "James Chen", "todo"),
    (7, "Scales & Arpeggios", "Broken Chords & Arpeggio Form", "Transition from solid chords to broken chord patterns and introductory arpeggio exercises.", 24, "James Chen", "todo"),
    (8, "Repertoire: Debussy", "Clair de Lune — Section A", "Begin Debussy’s masterpiece. Focus on the opening theme, rubato phrasing, and the delicate touch required for Impressionist repertoire.", 35, "Sophia Laurent", "todo"),
    (9, "Repertoire: Debussy", "Clair de Lune — Section B & Voicing", "Tackle the middle section with its rolling arpeggios, melodic voicing, and dynamic control across overlapping harmonies.", 38, "Sophia Laurent", "todo"),
    (10, "Repertoire: Debussy", "Pedalling Technique for Debussy", "Master half-pedalling, flutter pedalling, and the sustain techniques that give Debussy’s works their characteristic resonance.", 29, "Sophia Laurent", "todo"),
]
LESSONS = [dict(zip(("num", "topic", "title", "desc", "minutes", "instructor", "status"), l)) for l in _L]
MODULES = []  # dashboard "Your Curriculum": lessons grouped by topic
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
    dict(id="n2", title="New feedback from James Chen", text="Notes for G Major Scale & The Fingering Principle are ready.", time="Yesterday"),
    dict(id="n3", title="35 minutes to your weekly goal", text="You’re at 145 of 180 practice minutes this week.", time="Yesterday"),
    dict(id="n4", title="Welcome to the NMA Portal", text="Explore your lessons and track your progress here.", time="3 days ago"),
]


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("portal_dashboard"))
    if request.method == "POST":
        # TODO: replace with real authentication (check request.form["email"] / ["password"]).
        # For now ANY credentials sign in as the demo student below.
        session["user"] = STUDENT["name"]
        return redirect(url_for("portal_dashboard"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/portal/dashboard")
@login_required
def portal_dashboard():
    current = next(l for l in LESSONS if l["status"] == "current")
    done = sum(l["status"] == "done" for l in LESSONS)
    return render_template("dashboard.html", student=STUDENT, modules=MODULES, current=current,
                           done=done, total=len(LESSONS), pct=round(100 * done / len(LESSONS)))


@app.route("/portal/lessons")
@login_required
def portal_lessons():
    done = sum(l["status"] == "done" for l in LESSONS)
    return render_template("lessons.html", student=STUDENT, lessons=LESSONS, active=ACTIVE_LESSONS, done=done)


@app.route("/portal/lessons/<int:num>")
@login_required
def portal_lesson(num):
    lesson = next((l for l in LESSONS if l["num"] == num), None)
    if lesson is None:
        abort(404)
    if num not in ACTIVE_LESSONS:
        return redirect(url_for("portal_lessons"))
    return render_template("lesson.html", student=STUDENT, lesson=lesson, content=LESSON_CONTENT.get(num, {}))


@app.route("/portal/progress")
@login_required
def portal_progress():
    done = sum(l["status"] == "done" for l in LESSONS)
    return render_template("progress.html", student=STUDENT, lessons=LESSONS, week=WEEK, skills=SKILLS,
                           done=done, total=len(LESSONS), pct=round(100 * done / len(LESSONS)),
                           week_total=sum(m for _, m in WEEK))


if __name__ == "__main__":
    app.run(debug=True)

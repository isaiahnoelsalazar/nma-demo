import os
from flask import Flask, render_template, request, redirect, url_for, flash

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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO: authenticate request.form["email"] / ["password"], then redirect to the dashboard
        flash("Student portal coming soon.", "info")
        return redirect(url_for("login"))
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)

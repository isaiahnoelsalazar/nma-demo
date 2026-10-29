import os
from supabase_client import get_supabase_video_url

# ==============================================================================
# SUPABASE VIDEO CATALOG BY MODULE
# Format: Lesson <Num>: <Title> - [video link from supabase]
# ==============================================================================

MODULE_VIDEOS = {
    1: [
        {
            "name": "Right Hand - Kangaroo Hop",
            "file": "lesson1/right-hand-kangaroo-hop.mp4",
            "title": "Lesson 1: Right Hand - Kangaroo Hop",
        },
        {
            "name": "Left Hand - Kangaroo Hop",
            "file": "lesson1/left-hand-kangaroo-hop.mp4",
            "title": "Lesson 1: Left Hand - Kangaroo Hop",
        },
        {
            "name": "Right Hand - Three-Legged Kangaroo",
            "file": "lesson1/right-hand-three-legged-kangaroo.mp4",
            "title": "Lesson 1: Right Hand - Three-Legged Kangaroo",
        },
        {
            "name": "Left Hand - Three-Legged Kangaroo",
            "file": "lesson1/left-hand-three-legged-kangaroo.mp4",
            "title": "Lesson 1: Left Hand - Three-Legged Kangaroo",
        },
        {
            "name": "Finding Middle C",
            "file": "lesson1/finding-middle-c.mp4",
            "title": "Lesson 1: Finding Middle C",
        },
        {
            "name": "Introducing \"The Crotchet\"",
            "file": "lesson1/introducing-the-crotchet.mp4",
            "title": "Lesson 1: Introducing \"The Crotchet\"",
        },
        {
            "name": "Introducing \"The Minim\"",
            "file": "lesson1/introducing-the-minim.mp4",
            "title": "Lesson 1: Introducing \"The Minim\"",
        },
        {
            "name": "Reading Different Note Values",
            "file": "lesson1/reading-different-note-values.mp4",
            "title": "Lesson 1: Reading Different Note Values",
        },
        {
            "name": "Rhythm Song",
            "file": "lesson1/rhythm-song.mp4",
            "title": "Lesson 1: Rhythm Song",
        },
        {
            "name": "Song Performance: \"We Will Rock You\"",
            "file": "lesson1/song-performance-we-will-rock-you.mp4",
            "title": "Lesson 1: Song Performance: \"We Will Rock You\"",
        },
    ],
    5: [
        {
            "name": "Middle C and Middle B Song",
            "file": "lesson5/middle-c-and-middle-b-song.mp4",
            "title": "Lesson 5: Middle C and Middle B Song",
        },
        {
            "name": "The Crotchet Rest",
            "file": "lesson5/the-crotchet-rest.mp4",
            "title": "Lesson 5: The Crotchet Rest",
        },
        {
            "name": "Song Performance: Jaws",
            "file": "lesson5/song-performance-jaws.mp4",
            "title": "Lesson 5: Song Performance: Jaws",
        },
    ],
    10: [
        {
            "name": "Lesson 10: Reading Treble Clef Notes",
            "file": "lesson10/lesson-10-reading-treble-clef-notes.mp4",
            "title": "Lesson 10: Reading Treble Clef Notes",
        },
        {
            "name": "Reading Treble Clef Notes (Space Notes & Middle Notes)",
            "file": "lesson10/reading-treble-clef-notes-space-notes-middle-notes.mp4",
            "title": "Lesson 10: Reading Treble Clef Notes (Space Notes & Middle Notes)",
        },
    ],
}


def get_module_videos(num: int):
    """Returns the list of videos for this module resolved with Supabase URLs."""
    entries = MODULE_VIDEOS.get(num, [])
    resolved = []
    for item in entries:
        url = get_supabase_video_url(item["file"])
        resolved.append({
            "title": item["title"],
            "file": item["file"],
            "url": url,
            "display": f"{item['title']} - [{url if url else 'Supabase URL Pending'}]"
        })
    return resolved


def sec(heading, text=(), **extra):
    return {"heading": heading, "text": list(text), **extra}


def video_sec(heading, text=(), desc="", file_path=""):
    return {
        "heading": heading,
        "text": list(text),
        "video": {"url": get_supabase_video_url(file_path), "desc": desc},
    }


LESSON_CONTENT = {
    1: {
        "sheet_music": "",
        "parts": [
            {"title": "Part 1: Finger Numbers & Technique", "sections": [
                sec("Finger Numbers", [
                    "Learn the fundamental finger numbering for both hands (1 = Thumb, 2 = Index, 3 = Middle, 4 = Ring, 5 = Pinky).",
                    "Practice the **Spider Fingers 12345 Drill** to build finger independence."], widget="hands"),
                sec("Practice & Resources", ["Practice matching and identifying finger numbers on both hands."],
                    download={"label": "Downloadable PDF Worksheets", "url": ""}),
            ]},
            {"title": "Part 2: Navigating the Keyboard (Black & White Notes)", "sections": [
                sec("Finding Groups of Black Notes", [
                    "Observe the layout of the piano keyboard.",
                    "Learn to recognize patterns: **Groups of 2 Black Notes** and **Groups of 3 Black Notes**."]),
                sec("Kangaroo Hop Drill", [
                    "**Objective:** Play the group of 2 black notes using **fingers 2 and 3**, starting from the low end of the keyboard and ascending higher.",
                    "Practice separately with Right Hand and Left Hand."]),
                video_sec("Right Hand - Kangaroo Hop", desc="Demonstrates Right Hand playing fingers 2 and 3 on groups of 2 black notes up the keyboard.", file_path="lesson1/right-hand-kangaroo-hop.mp4"),
                video_sec("Left Hand - Kangaroo Hop", desc="Demonstrates Left Hand playing fingers 2 and 3 on groups of 2 black notes up the keyboard.", file_path="lesson1/left-hand-kangaroo-hop.mp4"),
                sec("Three-Legged Kangaroo Drill", [
                    "**Objective:** Play the group of 3 black notes using **fingers 2, 3, and 4**, starting low and ascending higher.",
                    "Practice separately with Right Hand and Left Hand."]),
                video_sec("Right Hand - Three-Legged Kangaroo", desc="Demonstrates Right Hand playing fingers 2, 3, and 4 on groups of 3 black notes up the keyboard.", file_path="lesson1/right-hand-three-legged-kangaroo.mp4"),
                video_sec("Left Hand - Three-Legged Kangaroo", desc="Demonstrates Left Hand playing fingers 2, 3, and 4 on groups of 3 black notes up the keyboard.", file_path="lesson1/left-hand-three-legged-kangaroo.mp4"),
            ]},
            {"title": "Part 3: The Musical Alphabet & Finding Notes", "sections": [
                sec("The Musical Alphabet", [
                    "In music, we use the letters **A - B - C - D - E - F - G**.",
                    "Once you reach **G**, the letters repeat over and over again on the white keys across the keyboard."]),
                sec("Find the White Notes (A–G)", [
                    "Locate and name every white key from A to G using the black key groups as landmarks."],
                    widget="notegame"),
                video_sec("Finding Middle C", [
                    "**Rule:** Find any group of 2 black notes. The white key directly to the left of the 2 black notes is **C**.",
                    "**Exercise:** Find and play C's all over the piano using your **Right Hand Finger 1** (Thumb)."],
                    desc="Demonstrates locating C next to the 2 black notes and playing all C's up/down the keyboard with finger 1.",
                    file_path="lesson1/finding-middle-c.mp4"),
            ]},
            {"title": "Part 4: Rhythm Fundamentals", "sections": [
                video_sec("Introducing \"The Crotchet\"", [
                    "Symbols in music tell us how long to hold a sound.",
                    "**The Crotchet (♩)** = Hold a sound for **1 beat**.",
                    "**Clapping Drill:** Clap and say \"1\" out loud for every crotchet (`1 - 1 - 1 - 1 - 1`)."],
                    desc="Demonstration of clapping steady 1-beat crotchet rhythms.",
                    file_path="lesson1/introducing-the-crotchet.mp4"),
                video_sec("Introducing \"The Minim\"", [
                    "The **Minim (𝅗𝅥)** looks like a crotchet, but its center is white/hollow.",
                    "**The Minim (𝅗𝅥)** = Hold a sound for **2 beats**.",
                    "**Clapping Drill:** Clap, hold hands together, and count \"1 - 2\" out loud (`1-2 | 1-2 | 1-2 | 1-2`)."],
                    desc="Demonstration of clapping and holding for 2 beats.",
                    file_path="lesson1/introducing-the-minim.mp4"),
                video_sec("Reading Different Note Values", [
                    "Combine Crotchets and Minims into a rhythm sequence.",
                    "**Crotchet (♩):** Stomp feet for 1 beat (\"1\").",
                    "**Minim (𝅗𝅥):** Clap hands and hold for 2 beats (\"1-2\")."],
                    desc="Demo showing stomping on crotchets and clapping on minims.",
                    file_path="lesson1/reading-different-note-values.mp4"),
                video_sec("Rhythm Song", [
                    "Perform the full pattern combining feet (crotchets) and hands (minims):",
                    "**Pattern:** `1 - 1 - (1-2) | 1 - 1 - (1-2) | 1 - 1 - (1-2) | 1 - 1 - (1-2)`"],
                    desc="Full performance of the Rhythm Song exercise.",
                    file_path="lesson1/rhythm-song.mp4"),
                video_sec("Song Performance: \"We Will Rock You\"", [
                    "Play along with the real song using the rhythm pattern learned in the Rhythm Song (`Stomp - Stomp - Clap`)."],
                    desc="Real-hand play-along performance to \"We Will Rock You\".",
                    file_path="lesson1/song-performance-we-will-rock-you.mp4"),
            ]},
        ],
    },
    5: {
        "sheet_music": "",
        "parts": [
            {"title": "Part 1: Introducing Middle B & Reading Notes", "sections": [
                sec("Lesson 5: Middle B", [
                    "Middle B sits in the space just above the top line in the bass clef stave.",
                    "Unlike Middle C, Middle B does not have a line through the middle of the note."],
                    widget="staffgame", clef="bass"),
                video_sec("Middle C and Middle B Song", [
                    "Let's try playing this song with our Left Hand first on Middle C using finger 1 and finger 2 on Middle B.",
                    "Remember to hold the notes for the correct value."],
                    desc="Demonstrates Left Hand playing Middle C (Finger 1) and Middle B (Finger 2) following the sheet music.",
                    file_path="lesson5/middle-c-and-middle-b-song.mp4"),
            ]},
            {"title": "Part 2: Rhythm & Song Application", "sections": [
                video_sec("The Crotchet Rest", [
                    "This symbol is called a 'Crotchet Rest'.",
                    {"t": "Unlike a crotchet which tells us to play for one beat, a Crotchet Rest tells us to have one beat of silence.",
                     "sub": ["**Crotchet Rest (𝄽):** 1 beat of silence", "**Crotchet (♩):** 1 beat of sound"]}],
                    desc="Demonstrates counting steady beats while resting on the crotchet rest.",
                    file_path="lesson5/the-crotchet-rest.mp4"),
                video_sec("Song Performance: Jaws", [
                    "We are going to use the Crotchet Rest to help us play the famous movie song \"Jaws\".",
                    "Place your Left Hand Finger 1 on Middle C and your Finger 2 on Middle B.",
                    "Remember to hold the notes for the correct value and to count the rests as beats of silence."],
                    desc="Real-hand play-along demonstration with Left Hand Finger 1 (C) and Finger 2 (B) counting crotchet rests accurately.",
                    file_path="lesson5/song-performance-jaws.mp4"),
            ]},
        ],
    },
    10: {
        "sheet_music": "",
        "parts": [
            {"title": "Part 1: Treble Clef Line Notes", "sections": [
                video_sec("Lesson 10: Reading Treble Clef Notes", [
                    "A quick and easy way to read notes in the Treble Clef is to use a rhyme for the line notes and spell the word ‘FACE’ for the Space Notes.",
                    {"t": "**Line Notes Rhyme:** Assign one word for each line note:",
                     "sub": ["**E**very (1st line)", "**G**ood (2nd line)", "**B**oy (3rd line)", "**D**eserves (4th line)", "**F**ruit (5th line)"]}],
                    desc="Explains how to read line notes on the Treble Clef stave using the \"Every Good Boy Deserves Fruit\" memory technique.",
                    file_path="lesson10/lesson-10-reading-treble-clef-notes.mp4"),
            ]},
            {"title": "Part 2: Treble Clef Space Notes & Ledger Line Notes", "sections": [
                video_sec("Reading Treble Clef Notes (Space Notes & Middle Notes)", [
                    {"t": "**Space Notes:** For space notes, we spell the word **FACE**.",
                     "sub": ["**F** (1st space)", "**A** (2nd space)", "**C** (3rd space)", "**E** (4th space)"]},
                    {"t": "**Middle C and D Underneath the Treble Stave:**",
                     "sub": ["Middle C sits on the first line underneath the treble stave.",
                             "Middle D sits in the space underneath the Treble stave."]}],
                    desc="Explains space notes (FACE) and demonstrates how Middle C and Middle D sit below the Treble Clef stave.",
                    file_path="lesson10/reading-treble-clef-notes-space-notes-middle-notes.mp4"),
            ]},
            {"title": "Part 3: Cheat Sheet & Practice Game", "sections": [
                sec("Treble Clef Note Cheat Sheet", [
                    "Use this quick reference \"Cheat Sheet\" to review all Treble Clef Line Notes, Space Notes, and Middle C & D.",
                    "**Line Notes:** E - G - B - D - F (\"Every Good Boy Deserves Fruit\")",
                    "**Space Notes:** F - A - C - E (\"FACE\")",
                    "**Middle Notes:** Middle C (line below) and Middle D (space below)"],
                    widget="staffgame", clef="treble"),
            ]},
        ],
    },
}
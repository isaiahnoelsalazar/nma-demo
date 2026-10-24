"""
Lesson content + media.

EASIEST WAY TO ADD MEDIA (no code changes):
  Drop files into static/media/lessonN/ named after the section heading (lowercase, dashes).
  See static/media/README.txt for the exact file names of every video / audio / PDF slot.
  e.g.  static/media/lesson1/right-hand-kangaroo-hop.mp4

OR set a link here instead (a link below always wins over a dropped-in file):
  sheet_music  -> "Download Sheet Music" PDF link          (file name: sheet-music.pdf)
  video.url    -> demo video link (mp4 URL or YouTube/Vimeo embed URL)
  audio.url    -> backing track link
  download.url -> downloadable file link
  player.src   -> URL of an external interactive player (embedded as an iframe)

BUILT-IN INTERACTIVE PLAYERS (lesson 1) are configured on the section's "player":
  kind="keys"  -> practice keyboard; guide="black2" | "black3" | "allC", hand="R" | "L" shows the finger numbers.
                  Optional cues=[[start_sec, duration_sec, [midi, ...]], ...] lights keys in sync with the video.
  kind="beat"  -> rhythm trainer; pattern uses S = stomp crotchet, K = clap crotchet, M = clap minim; bpm sets the tempo.
"""

SYNC = "Synchronized virtual keyboard with light-up keys during video playback."
BEAT = "Synchronized rhythmic audio playback with visual beat indicators."


def media(video_desc, player_desc=SYNC, **player_extra):
    return {"video": {"url": "", "desc": video_desc}, "player": {"src": "", "desc": player_desc, **player_extra}}


def sec(heading, text=(), **extra):
    return {"heading": heading, "text": list(text), **extra}


LESSON_CONTENT = {
    1: {
        "sheet_music": "",    # TODO: lesson 1 sheet music PDF link
        "parts": [
            {"title": "Part 1: Finger Numbers & Technique", "sections": [
                sec("Finger Numbers", [
                    "Learn the fundamental finger numbering for both hands (1 = Thumb, 2 = Index, 3 = Middle, 4 = Ring, 5 = Pinky).",
                    "Practice the **Spider Fingers 12345 Drill** to build finger independence."], widget="hands"),
                sec("Practice & Resources", ["Practice matching and identifying finger numbers on both hands."],
                    download={"label": "Downloadable PDF Worksheets", "url": ""}),  # TODO: worksheets PDF link
            ]},
            {"title": "Part 2: Navigating the Keyboard (Black & White Notes)", "sections": [
                sec("Finding Groups of Black Notes", [
                    "Observe the layout of the piano keyboard.",
                    "Learn to recognize patterns: **Groups of 2 Black Notes** and **Groups of 3 Black Notes**."]),
                sec("Kangaroo Hop Drill", [
                    "**Objective:** Play the group of 2 black notes using **fingers 2 and 3**, starting from the low end of the keyboard and ascending higher.",
                    "Practice separately with Right Hand and Left Hand."]),
                sec("Right Hand - Kangaroo Hop", **media("Demonstrates Right Hand playing fingers 2 and 3 on groups of 2 black notes up the keyboard.", kind="keys", guide="black2", hand="R")),
                sec("Left Hand - Kangaroo Hop", **media("Demonstrates Left Hand playing fingers 2 and 3 on groups of 2 black notes up the keyboard.", kind="keys", guide="black2", hand="L")),
                sec("Three-Legged Kangaroo Drill", [
                    "**Objective:** Play the group of 3 black notes using **fingers 2, 3, and 4**, starting low and ascending higher.",
                    "Practice separately with Right Hand and Left Hand."]),
                sec("Right Hand - Three-Legged Kangaroo", **media("Demonstrates Right Hand playing fingers 2, 3, and 4 on groups of 3 black notes up the keyboard.", kind="keys", guide="black3", hand="R")),
                sec("Left Hand - Three-Legged Kangaroo", **media("Demonstrates Left Hand playing fingers 2, 3, and 4 on groups of 3 black notes up the keyboard.", kind="keys", guide="black3", hand="L")),
            ]},
            {"title": "Part 3: The Musical Alphabet & Finding Notes", "sections": [
                sec("The Musical Alphabet", [
                    "In music, we use the letters **A - B - C - D - E - F - G**.",
                    "Once you reach **G**, the letters repeat over and over again on the white keys across the keyboard."]),
                sec("Find the White Notes (A–G)", [
                    "Interactive mini-game teaching students how to locate and name every white key from A to G using the black key groups as landmarks."],
                    widget="notegame"),
                sec("Finding Middle C", [
                    "**Rule:** Find any group of 2 black notes. The white key directly to the left of the 2 black notes is **C**.",
                    "**Exercise:** Find and play C's all over the piano using your **Right Hand Finger 1** (Thumb)."],
                    **media("Demonstrates locating C next to the 2 black notes and playing all C's up/down the keyboard with finger 1.", kind="keys", guide="allC", hand="R")),
            ]},
            {"title": "Part 4: Rhythm Fundamentals", "sections": [
                sec("Introducing \"The Crotchet\"", [
                    "Symbols in music tell us how long to hold a sound.",
                    "**The Crotchet (♩)** = Hold a sound for **1 beat**.",
                    "**Clapping Drill:** Clap and say \"1\" out loud for every crotchet (`1 - 1 - 1 - 1 - 1`)."],
                    **media("Demonstration of clapping steady 1-beat crotchet rhythms.", BEAT, kind="beat", pattern="KKKKK", bpm=70)),
                sec("Introducing \"The Minim\"", [
                    "The **Minim (𝅗𝅥)** looks like a crotchet, but its center is white/hollow.",
                    "**The Minim (𝅗𝅥)** = Hold a sound for **2 beats**.",
                    "**Clapping Drill:** Clap, hold hands together, and count \"1 - 2\" out loud (`1-2 | 1-2 | 1-2 | 1-2`)."],
                    **media("Demonstration of clapping and holding for 2 beats.", BEAT, kind="beat", pattern="MMMM", bpm=70)),
                sec("Reading Different Note Values", [
                    "Combine Crotchets and Minims into a rhythm sequence.",
                    "**Crotchet (♩):** Stomp feet for 1 beat (\"1\").",
                    "**Minim (𝅗𝅥):** Clap hands and hold for 2 beats (\"1-2\")."],
                    **media("Demo showing stomping on crotchets and clapping on minims.", "Synchronized rhythmic audio playback.", kind="beat", pattern="SSMSSM", bpm=70)),
                sec("Rhythm Song", [
                    "Perform the full pattern combining feet (crotchets) and hands (minims):",
                    "**Pattern:** `1 - 1 - (1-2) | 1 - 1 - (1-2) | 1 - 1 - (1-2) | 1 - 1 - (1-2)`"],
                    **media("Full performance of the Rhythm Song exercise.", "Synchronized visual beat tracking with light-up key indicators.", kind="beat", pattern="SSMSSMSSMSSM", bpm=70)),
                sec("Song Performance: \"We Will Rock You\"", [
                    "Play along with the real song using the rhythm pattern learned in the Rhythm Song (`Stomp - Stomp - Clap`)."],
                    **media("Real-hand play-along performance to \"We Will Rock You\".", "Interactive backing track audio with light-up key playback.", kind="beat", pattern="SSMSSMSSMSSM", bpm=81)),
            ]},
        ],
    },
    5: {
        "sheet_music": "",    # TODO: lesson 5 sheet music PDF link
        "parts": [
            {"title": "Part 1: Introducing Middle B & Reading Notes", "sections": [
                sec("Lesson 5: Middle B", [
                    "Middle B sits in the space just above the top line in the bass clef stave.",
                    "Unlike Middle C, Middle B does not have a line through the middle of the note. This is how we tell the difference between Middle C and Middle B: Middle C is on the line and Middle B is in the space."],
                    widget="staffgame", clef="bass"),
                sec("Middle C and Middle B Song", [
                    "Let's try playing this song with our Left Hand first on Middle C using finger 1 and finger 2 on Middle B.",
                    "Remember to hold the notes for the correct value."],
                    **media("Demonstrates Left Hand playing Middle C (Finger 1) and Middle B (Finger 2) following the sheet music.",
                            "Synchronized virtual keyboard and stave playback with light-up keys.")),
            ]},
            {"title": "Part 2: Rhythm & Song Application", "sections": [
                sec("The Crotchet Rest", [
                    "This symbol is called a 'Crotchet Rest'.",
                    {"t": "Unlike a crotchet which tells us to play for one beat, a Crotchet Rest tells us to have one beat of silence or to \"rest\" for one beat.",
                     "sub": ["**Crotchet Rest (𝄽):** 1 beat of silence", "**Crotchet (♩):** 1 beat of sound"]}],
                    video={"url": "", "desc": "Demonstrates counting steady beats while resting (keeping silence) on the crotchet rest."}),
                sec("Song Performance: Jaws", [
                    "We are going to use the Crotchet Rest to help us play the famous movie song \"Jaws\".",
                    "This song depicts a scary scene of a shark circling a boat.",
                    "Place your Left Hand Finger 1 on Middle C and your Finger 2 on Middle B.",
                    "Remember to hold the notes for the correct value and to count the rests as beats of silence."],
                    audio={"url": "", "desc": "Play-along backing track for \"Jaws\"."},
                    **media("Real-hand play-along demonstration with Left Hand Finger 1 (C) and Finger 2 (B) counting crotchet rests accurately.",
                            "Interactive sheet music player with light-up key feedback synced to the backing track.")),
            ]},
        ],
    },
    10: {
        "sheet_music": "",    # TODO: lesson 10 sheet music PDF link
        "parts": [
            {"title": "Part 1: Treble Clef Line Notes", "sections": [
                sec("Lesson 10: Reading Treble Clef Notes", [
                    "A quick and easy way to read notes in the Treble Clef is to use a rhyme for the line notes and spell the word ‘FACE’ for the Space Notes.",
                    {"t": "**Line Notes Rhyme:** Assign one word for each line note:",
                     "sub": ["**E**very (1st line)", "**G**ood (2nd line)", "**B**oy (3rd line)", "**D**eserves (4th line)", "**F**ruit (5th line)"]},
                    "Use the first letter of each word to find your note: **E** for Every, **G** for Good, **B** for Boy, **D** for Deserves, and **F** for Fruit."],
                    **media("Explains how to read line notes on the Treble Clef stave using the \"Every Good Boy Deserves Fruit\" memory technique.",
                            "Visual stave displaying each line note with audio playback when clicked.")),
            ]},
            {"title": "Part 2: Treble Clef Space Notes & Ledger Line Notes", "sections": [
                sec("Reading Treble Clef Notes (Space Notes & Middle Notes)", [
                    {"t": "**Space Notes:** For space notes, we spell the word **FACE**.",
                     "sub": ["**F** (1st space)", "**A** (2nd space)", "**C** (3rd space)", "**E** (4th space)"]},
                    {"t": "**Middle C and D Underneath the Treble Stave:**",
                     "sub": ["Middle C and Middle D sit underneath the Treble stave.",
                             "Simply remember what they look like: Middle C sits on the first **line underneath** the treble stave, and Middle D sits in the **space underneath** the Treble stave."]}],
                    video={"url": "", "desc": "Explains space notes (FACE) and demonstrates how Middle C and Middle D sit below the Treble Clef stave."}),
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

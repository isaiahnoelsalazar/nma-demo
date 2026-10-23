"""
Lesson content + media placeholders.

HOW TO ADD MEDIA
  * Put files in static/media/lessonN/ and use a URL like "/static/media/lesson1/right-hand-kangaroo.mp4",
    or paste a YouTube / Vimeo embed URL (e.g. "https://www.youtube.com/embed/XXXX").
  * Every "" below is an empty slot. Empty slots show a visible "placeholder" box on the page.

SLOTS
  main_video   -> big player at the top of the lesson page
  sheet_music  -> "Download Sheet Music" button (PDF link)
  video.url    -> demo video inside a section
  player.src   -> URL of the interactive player for that section (embedded as an iframe)
  download.url -> downloadable file link (e.g. worksheets PDF)
"""

SYNC = "Synchronized virtual keyboard with light-up keys during video playback."
BEAT = "Synchronized rhythmic audio playback with visual beat indicators."


def media(video_desc, player_desc=SYNC):
    return {"video": {"url": "", "desc": video_desc}, "player": {"src": "", "desc": player_desc}}


def sec(heading, text=(), **extra):
    return {"heading": heading, "text": list(text), **extra}


LESSON_CONTENT = {
    1: {
        "main_video": "",     # TODO: lesson 1 main video link
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
                sec("Right Hand - Kangaroo Hop", **media("Demonstrates Right Hand playing fingers 2 and 3 on groups of 2 black notes up the keyboard.")),
                sec("Left Hand - Kangaroo Hop", **media("Demonstrates Left Hand playing fingers 2 and 3 on groups of 2 black notes up the keyboard.")),
                sec("Three-Legged Kangaroo Drill", [
                    "**Objective:** Play the group of 3 black notes using **fingers 2, 3, and 4**, starting low and ascending higher.",
                    "Practice separately with Right Hand and Left Hand."]),
                sec("Right Hand - Three-Legged Kangaroo", **media("Demonstrates Right Hand playing fingers 2, 3, and 4 on groups of 3 black notes up the keyboard.")),
                sec("Left Hand - Three-Legged Kangaroo", **media("Demonstrates Left Hand playing fingers 2, 3, and 4 on groups of 3 black notes up the keyboard.")),
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
                    **media("Demonstrates locating C next to the 2 black notes and playing all C's up/down the keyboard with finger 1.")),
            ]},
            {"title": "Part 4: Rhythm Fundamentals", "sections": [
                sec("Introducing \"The Crotchet\"", [
                    "Symbols in music tell us how long to hold a sound.",
                    "**The Crotchet (♩)** = Hold a sound for **1 beat**.",
                    "**Clapping Drill:** Clap and say \"1\" out loud for every crotchet (`1 - 1 - 1 - 1 - 1`)."],
                    **media("Demonstration of clapping steady 1-beat crotchet rhythms.", BEAT)),
                sec("Introducing \"The Minim\"", [
                    "The **Minim (𝅗𝅥)** looks like a crotchet, but its center is white/hollow.",
                    "**The Minim (𝅗𝅥)** = Hold a sound for **2 beats**.",
                    "**Clapping Drill:** Clap, hold hands together, and count \"1 - 2\" out loud (`1-2 | 1-2 | 1-2 | 1-2`)."],
                    **media("Demonstration of clapping and holding for 2 beats.", BEAT)),
                sec("Reading Different Note Values", [
                    "Combine Crotchets and Minims into a rhythm sequence.",
                    "**Crotchet (♩):** Stomp feet for 1 beat (\"1\").",
                    "**Minim (𝅗𝅥):** Clap hands and hold for 2 beats (\"1-2\")."],
                    **media("Demo showing stomping on crotchets and clapping on minims.", "Synchronized rhythmic audio playback.")),
                sec("Rhythm Song", [
                    "Perform the full pattern combining feet (crotchets) and hands (minims):",
                    "**Pattern:** `1 - 1 - (1-2) | 1 - 1 - (1-2) | 1 - 1 - (1-2) | 1 - 1 - (1-2)`"],
                    **media("Full performance of the Rhythm Song exercise.", "Synchronized visual beat tracking with light-up key indicators.")),
                sec("Song Performance: \"We Will Rock You\"", [
                    "Play along with the real song using the rhythm pattern learned in the Rhythm Song (`Stomp - Stomp - Clap`)."],
                    **media("Real-hand play-along performance to \"We Will Rock You\".", "Interactive backing track audio with light-up key playback.")),
            ]},
        ],
    },
    # Contents for lessons 5 and 10 will be provided — same structure as lesson 1.
    5: {"main_video": "", "sheet_music": "", "parts": []},
    10: {"main_video": "", "sheet_music": "", "parts": []},
}

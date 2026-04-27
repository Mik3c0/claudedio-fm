#!/usr/bin/env python3
"""
Claudedio FM — DJ Cara Voice Generator
Generates MP3 intros using ElevenLabs TTS.

Usage:
  python generate_cara.py

Requirements:
  pip install requests
"""

import os
import sys
import time
import json
import requests

# ── CONFIG — fill these in ───────────────────────────────────────────────────
API_KEY  = ""        # Paste your ElevenLabs API key here
VOICE_ID = "pFZP5JQG7iQjIQuC4Bku"   # Lily — Velvety Actress, British Female (premade, free tier)
MODEL_ID = "eleven_multilingual_v2"   # Best quality
OUTPUT_DIR = "audio"
# ─────────────────────────────────────────────────────────────────────────────

# Voice settings — tuned for a warm, clear radio host delivery
VOICE_SETTINGS = {
    "stability":        0.42,   # Lower = more expressive/natural
    "similarity_boost": 0.80,   # How closely to match the voice
    "style":            0.20,   # Adds character/expressiveness
    "use_speaker_boost": True
}

# ── ALL 58 DJ CARA SCRIPTS ───────────────────────────────────────────────────
SCRIPTS = [
    (1,  "90210",                        "Travis Scott",                         "Coming up — Travis Scott with 90210 from Rodeo, 2015. Five minutes and forty seconds of pure atmosphere. Travis Scott, whose real name is Jacques Webster the Second, started performing at sixteen in a church in Houston. Then he made 90210. Quite the career arc. Turn it up."),
    (2,  "L$D",                          "A$AP Rocky",                           "You're tuned in to Claudedio FM — I'm DJ Cara, and I do hope you're comfortable. Coming up, A$AP Rocky with L$D, from AT.LONG.LAST.A$AP, 2015. Rocky reportedly named the album during a mushroom trip. That is not a euphemism. That is just what happened."),
    (3,  "A$AP Forever",                 "A$AP Rocky ft. Moby",                  "A$AP Rocky sampling Moby — 2018. That's Rocky borrowing from Moby's Porcelain, which was everywhere in the year 2000. Moby himself said he was honoured. A$AP Forever, from Testing. Two artists, two eras, one rather beautiful result."),
    (4,  "Fashion Killa",                "A$AP Rocky",                           "Quick pop quiz — Rocky mentions how many fashion brands in Fashion Killa? The answer is over fifteen. Chanel, Alexander Wang, Yves Saint Laurent, Maison Margiela. The man turned a rap song into a spring collection. Fashion Killa, Long Live A$AP, 2013."),
    (5,  "Fukk Sleep",                   "A$AP Rocky ft. FKA twigs",             "FKA twigs is, without question, one of the most singular artists alive. And Rocky had the good sense to ring her up for Fukk Sleep, from Testing, 2018. An album so experimental it confused Rocky's own label. Claudedio FM, however, is not confused. We love it here."),
    (6,  "Kids Turned Out Fine",         "A$AP Rocky",                           "A$AP Rocky sampling eighties synth-pop for Kids Turned Out Fine. Testing, 2019. Is it genius or deeply chaotic? On Claudedio FM we have convened, deliberated, and ruled: it is genius. Here it is."),
    (7,  "Drugs N Hella Melodies",       "Don Toliver ft. Kali Uchis",           "Kali Uchis has the vocal range of someone who made a deal at a crossroads at midnight. Don Toliver floats on top like smoke off a warm engine. Together — Drugs N Hella Melodies, Life of a Don, 2021. It does exactly what it says on the tin."),
    (8,  "No Idea",                      "Don Toliver",                          "Don Toliver. No Idea, from Heaven or Hell, 2020. This is the track that properly put Toliver on the map — the algorithm caught it, the playlists caught it, and then the rest of us caught it. Celestial trap. That's the genre. I'm coining it now."),
    (9,  "No Pole",                      "Don Toliver",                          "More Don Toliver — Love Sick, 2023. No Pole. Toliver's whole catalogue sounds like being airborne in very good weather. I don't know how else to describe it. Here he is."),
    (10, "ATM",                          "Don Toliver",                          "Claudedio FM. DJ Cara. ATM — Don Toliver, OCTANE, 2023. This song makes driving feel like a film. Which, if you are in fact driving right now, is rather the point. Keep both hands on the wheel, and enjoy."),
    (11, "MY EYES",                      "Travis Scott",                         "Travis Scott. UTOPIA, 2023. One of the most anticipated albums in recent memory, and MY EYES is the kind of track that reminds you why. Four minutes of peak Cactus Jack. Eyes on the road, though. Not literally."),
    (12, "Trance",                       "Metro Boomin, Travis Scott & Young Thug","Metro Boomin — whose real name is Leland Tyler Wayne, which I find deeply charming — plus Travis Scott and Young Thug. Trance, from Heroes and Villains, 2022. Three very chaotic people making something very composed. Here it is."),
    (13, "Type Shit",                    "Future, Metro Boomin, Travis Scott & Playboi Carti","Four of the most chaotic men in music on a single track. Future, Metro Boomin, Travis Scott, Playboi Carti — We Don't Trust You, 2024. I genuinely don't know who approved this collaboration but I'd like to send them a fruit basket. Type Shit."),
    (14, "née-nah",                      "21 Savage, Travis Scott & Metro Boomin","21 Savage, Travis Scott, Metro Boomin. née-nah, 2023. Trivia — 21 Savage was born in London. Yes, London. Moved to Atlanta at twelve. The internet lost its mind when this became public in 2019. He seemed entirely unbothered. As one should be."),
    (15, "New Person, Same Old Mistakes","Tame Impala",                          "Tame Impala — technically one person. Kevin Parker, Perth, Australia, doing absolutely everything himself in a studio. New Person Same Old Mistakes, Currents, 2015. Rihanna covered this and called it Same Ol' Mistakes. Kevin Parker said he cried when he heard it. That's rather sweet."),
    (16, "Borderline",                   "Tame Impala",                          "More Kevin Parker. Borderline, from The Slow Rush, 2019. He wrote this album about the feeling of watching your own life from the outside. Either very deep or very Australian — possibly both. Here it is."),
    (17, "Dark Red",                     "Steve Lacy",                           "Steve Lacy wrote Dark Red on his phone. Using GarageBand. He was nineteen. On his phone. I'll just let that be what it is. Dark Red, 2017."),
    (18, "luther",                       "Kendrick Lamar & SZA",                 "Kendrick Lamar and SZA. luther — from GNX, 2024. The whole album dropped with no warning and the internet held its breath for a week. luther samples Luther Vandross, is genuinely a love song from Kendrick Lamar, and is frankly stunning. Here it is."),
    (19, "Chanel",                       "Frank Ocean",                          "Frank Ocean releases music at the frequency of a solar eclipse. Chanel, 2017 — about seeing both sides of everything. Love, identity, duality. Frank Ocean is operating at a level most artists can only theorise about. Here he is."),
    (20, "Raindance",                    "Dave & Tems",                          "Dave — Santan Dave, Streatham, South London — and Tems, from Lagos. Raindance, 2023. Dave went to law school, won the Mercury Prize, and writes some of the sharpest verse in British music. Tems is simply extraordinary. Together they made this. Here it is."),
    (21, "Sudno",                        "Molchat Doma",                         "Molchat Doma — Houses Are Silent — from Minsk, Belarus. Судно. Vessel. Post-punk, Soviet melancholy, bass so heavy it might be load-bearing. 2019. If you've never heard them before, welcome. If you have — you know exactly what's coming."),
    (22, "Detstvo",                      "Rauf & Faik",                          "Rauf and Faik are brothers from Azerbaijan. Detstvo means Childhood in Russian. 2018. The song became enormously popular online, people started slowing it down, adding reverb, making it float even more than it already did. The original is gorgeous. Here it is, as intended."),
    (23, "Meduza",                       "MATRANG",                              "MATRANG — Russian rapper, real name Artur Musokov. Медуза. Medusa. 2017. Produced himself, released independently, went viral across Russia and then internationally. Dark, hypnotic, smooth. Fits your rotation rather well, I think."),
    (24, "Sailor Song",                  "Gigi Perez",                           "Gigi Perez. Sailor Song, 2023. Existed quietly until the algorithm found it, at which point it became inescapable — and for very good reason. Gigi Perez has a voice built for rooms with low ceilings and good acoustics. This song takes you somewhere coastal and specific. Here it is."),
    (25, "Timeless",                     "The Weeknd & Playboi Carti",           "The Weeknd and Playboi Carti, 2024. Abel Tesfaye and Carti — whose commitment to sounding completely unhinged is a genuine artistic philosophy — made something quite otherworldly together. Timeless. The title is, for once, not an exaggeration."),
    (26, "Come As You Are",              "Nirvana",                              "1991. Nirvana. Come As You Are, from Nevermind. Kurt Cobain said the song was about hypocrisy, then said it was about acceptance, then said it was about nothing. It's been thirty-five years and it still sounds like it was recorded yesterday. Here it is."),
    (27, "Everything In Its Right Place","Radiohead",                            "Radiohead. Kid A, year 2000. Everything In Its Right Place — Thom Yorke wrote it in fifteen minutes. Critics called it the best album opener in modern music. The band had spent years as rock stars and then released this, which sounds like nothing that came before it. Quite the move."),
    (28, "XO Tour Llif3",               "Lil Uzi Vert",                         "Lil Uzi Vert. XO Tour Llif3 — Life, spelled backwards. Luv Is Rage 2, 2017. Recorded in one take after a breakup. Uzi has since embedded a twenty-four million dollar pink diamond in his forehead. He appears to be doing very well. Here's the song."),
    (29, "MUTT",                         "Leon Thomas",                          "Leon Thomas. MUTT, 2023. You may know Thomas from the television show Victorious — which I mention because it's gloriously unexpected context. He grew up, became one of the most interesting R&B voices working today, and MUTT is him at full power. Here it is."),
    (30, "back to friends",              "sombr",                                "sombr — no capital S, I've accepted it — are a Canadian duo. back to friends, 2022. This song exists at the exact frequency of sadness that doesn't register while you're listening. It catches you twenty minutes later. You have been warned. Here it is."),
    (31, "Fire for You",                 "Cannons",                              "Cannons. Los Angeles trio. Fire for You, 2020. They sound like they were assembled specifically to score films that haven't been made yet. This track, in particular, sounds like driving toward something important at dusk. Perfect Claudedio FM material."),
    (32, "Big Dawgs",                    "Hanumankind & Kalmi",                  "Hanumankind — from Kerala, trained in the States, came home and made something that went completely global. Big Dawgs, 2024, with Kalmi. The internet said where has this been and the answer is: India, patiently waiting for you to catch up."),
    (33, "MILLION DOLLAR BABY",          "Tommy Richman",                        "Tommy Richman. MILLION DOLLAR BABY, 2024. He was essentially unknown before this track and then suddenly he was on every playlist, every show, every speaker. It makes you feel like you're winning something. You're listening to Claudedio FM. You are, in fact, winning something."),
    (34, "Head In The Clouds",           "Hayd",                                 "Hayd — Irish-American singer-songwriter. Head In The Clouds, 2022. This is one of those songs that arrived quietly and built slowly into something you listen to on repeat without fully realising you're doing it. It's earned that."),
    (35, "One More Light",               "Linkin Park",                          "Linkin Park. One More Light, 2017. Chester Bennington passed away two months after this album released. This song, specifically, took on a weight it was already carrying. It is a beautiful, fragile thing. Here it is."),
    (36, "Love In Portofino",            "Dalida",                               "Right. A pivot. Dalida — born in Cairo, raised in Italy, became a French icon. Love In Portofino, 1958. This is the oldest track on the station today by a considerable margin, and it sounds like a film that exists in another dimension. Claudedio FM has range. Here it is."),
    (37, "PUFFIN ON ZOOTIEZ",           "Future",                               "Future. PUFFIN ON ZOOTIEZ, from I Never Liked You, 2022. Future has released more music than most artists have ideas. The remarkable thing is how consistently good it is. This track in particular has a weight to it. Here it is."),
    (38, "act iii: on god",              "4batz",                                "4batz. act iii — on god, she like. 2024. Another artist who came from relative obscurity and suddenly everyone knew the name. The R&B underground has been producing extraordinary music for years and the mainstream is slowly catching up. 4batz is a good reason why."),
    (39, "HONEST",                       "Baby Keem",                            "Baby Keem. HONEST, from DIE FOR MY BITCH, 2019. Keem is Kendrick Lamar's cousin — which is almost unfair in terms of musical genetics — and he has been making deeply interesting music since he was a teenager. HONEST is an early one that holds up completely."),
    (40, "If We Being Real",             "Yeat",                                 "Yeat. If We Being Real, from 2093, 2023. Yeat has created his own dialect at this point — the slurred, pitched, layered vocal style that either clicks immediately or confuses entirely. I suspect for you it clicks. Here it is."),
    (41, "Nonchalant",                   "6LACK",                                "6LACK — pronounced Black, not Six-Lack. I learned this the hard way. Nonchalant, from East Atlanta Love Letter, 2018. 6LACK makes R&B that sounds like a 3am conversation you weren't prepared for but needed. This is one of the good ones."),
    (42, "Superstar",                    "Lupe Fiasco ft. Matthew Santos",       "2007. Lupe Fiasco. Superstar, from Lupe Fiasco's The Cool. Lupe is one of the most lyrically gifted rappers of his generation — he's been underlisted in best-of conversations for fifteen years and I find it genuinely baffling. Matthew Santos on the hook. All of it perfect."),
    (43, "Headlines",                    "Drake",                                "Drake. Headlines, 2011. Before all the chapters that followed — this was just Drake deciding he was a star and being correct about it. The confidence was earned. Retrospectively — yes it was."),
    (44, "You & Me (Flume Remix)",       "Disclosure ft. Eliza Doolittle",       "Disclosure's You and Me, remixed by Flume, then slowed and reverbed by the internet. The slowed-reverb era is its own genre now and I've made peace with it. This version sounds like drifting through fog in a car that costs more than it should. Which may or may not describe your current situation."),
    (45, "Maps",                         "Yeah Yeah Yeahs",                      "Yeah Yeah Yeahs. Maps. 2003. Karen O wrote this about her then-boyfriend while he was late to the recording session. The tears in the music video are real. The song became one of the defining tracks of its era. Also — and primarily — it's just brilliant."),
    (46, "Ivy",                          "Frank Ocean",                          "DJ Cara pick. I'm selecting this personally. Frank Ocean — Ivy, from Blonde, 2016. Ocean went silent for four years and then delivered Blonde and made everyone agree it was worth the wait. Ivy is raw, honest, and slightly devastating. I think you'll find it fits."),
    (47, "The Less I Know The Better",   "Tame Impala",                          "DJ Cara pick. More Kevin Parker. The Less I Know The Better — possibly the Tame Impala song, if you had to pick one. Currents, 2015. The bass, the groove, the chorus that arrives like something you've been waiting for without knowing it. Here it is."),
    (48, "Evergreen",                    "Omar Apollo",                          "DJ Cara pick. Omar Apollo, from Indiana. Mexican-American. Grew up on Selena and Frank Ocean simultaneously. That combination produced something special — Evergreen, 2022, about a love that probably should have ended sooner. Heartbreaking. I think you'll love it."),
    (49, "Magnolia",                     "Playboi Carti",                        "DJ Cara pick. Playboi Carti. Magnolia, 2017. Pierre Bourne made that beat and it became one of the most referenced sounds of the decade. Carti says very little in his songs and means all of it. New York, summer, here it is."),
    (50, "Retrograde",                   "James Blake",                          "DJ Cara pick. James Blake — West London. He makes music that sits between electronic minimalism and the most exposed piano balladry you've ever heard. Retrograde, 2013, his best-known track. Given what else you've been listening to, I think this lands well."),
    (51, "From Eden",                    "Hozier",                               "DJ Cara pick. Hozier. From Eden, 2014. Andrew Hozier-Byrne, from Bray, County Wicklow. From Eden sounds like a hymn written by someone who stopped believing but couldn't stop singing. You've got his Unknown slash Nth in your regular rotation — I think this is the natural companion."),
    (52, "Bad Habit",                    "Steve Lacy",                           "DJ Cara pick. Steve Lacy — you've got Dark Red in the rotation, written on his phone at nineteen. Bad Habit, from Gemini Rights, 2022, is the one that went to number one. He played the guitar himself. He's been producing for Kendrick and Tyler the Creator since he was seventeen. The talent is slightly offensive."),
    (53, "BUS RIDE",                     "KAYTRANADA ft. Karriem Riggins & River Tiber","DJ Cara pick. KAYTRANADA — Haitian-Canadian producer, Montreal. Louis Kevin Celestin. BUS RIDE from 99.9%, 2016. Grammy-winning album. Karriem Riggins on drums, River Tiber on top. The whole thing is endlessly smooth. Trust me on this one."),
    (54, "Multi-Love",                   "Unknown Mortal Orchestra",             "DJ Cara pick. Unknown Mortal Orchestra. Multi-Love, 2015. Ruban Nielson wrote this about a relationship arrangement that didn't quite work out. Psychedelic, funky, and oddly sorrowful all at once. Given your Tame Impala consumption — you'll get along with this perfectly."),
    (55, "Snooze",                       "SZA",                                  "DJ Cara pick. SZA. Snooze, from SOS, 2022. Deceptively casual, technically immaculate. A song about staying in something you know isn't working. Extremely relatable. Extremely well-made. Here it is."),
    (56, "Money Trees",                  "Kendrick Lamar ft. Jay Rock",          "DJ Cara pick. Kendrick Lamar — you've got luther in the rotation, so I know you appreciate him. Money Trees, from Good Kid M.A.A.D City, 2012. Jay Rock's hook. That piano sample. Kendrick's storytelling about Compton. One of the best album cuts in hip-hop this century, I'd argue."),
    (57, "Space Song",                   "Beach House",                          "DJ Cara pick. Beach House. Space Song, from Depression Cherry, 2015. Victoria Legrand's voice was specifically engineered to make you feel weightless — I don't know how else to explain it. The band is called Beach House. The album is called Depression Cherry. It all makes sense when the song plays."),
    (58, "Tabletki (Pills)",             "IC3PEAK",                              "DJ Cara pick — and a bold one. IC3PEAK, from Moscow. Tabletki — Pills — 2018. Dark, industrial, Russian post-punk electronic. You've already got Molchat Doma in the rotation. I've taken that as permission. Their live shows were reportedly monitored by Russian authorities. That's how you know it's essential listening."),
]


# ── HELPERS ──────────────────────────────────────────────────────────────────

def get_headers():
    return {"xi-api-key": API_KEY, "Content-Type": "application/json"}

def list_voices():
    """Fetch and print all available voices."""
    print("\nFetching voices from ElevenLabs...\n")
    r = requests.get("https://api.elevenlabs.io/v1/voices", headers=get_headers())
    r.raise_for_status()
    voices = r.json()["voices"]

    print(f"{'#':<4} {'Name':<28} {'ID':<25} {'Labels'}")
    print("-" * 90)
    for i, v in enumerate(voices):
        labels = ", ".join(f"{k}: {val}" for k, val in v.get("labels", {}).items())
        print(f"{i:<4} {v['name']:<28} {v['voice_id']:<25} {labels}")
    return voices

def generate_mp3(voice_id, text, track_num):
    """Call ElevenLabs TTS and save the result as an MP3."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS
    }
    headers = {**get_headers(), "Accept": "audio/mpeg"}
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"cara_{track_num:03d}.mp3"
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "wb") as f:
        f.write(r.content)
    size_kb = len(r.content) / 1024
    print(f"  ✅  {filename}  ({size_kb:.0f} KB)")
    return path

def check_credits():
    """Show remaining character quota."""
    r = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers=get_headers())
    if r.status_code == 200:
        data = r.json()
        used      = data.get("character_count", 0)
        limit     = data.get("character_limit", 0)
        remaining = limit - used
        print(f"\n📊 Credits: {used:,} used / {limit:,} total — {remaining:,} remaining")
    else:
        print("  (Could not fetch credit info)")


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    global API_KEY, VOICE_ID

    print("🎙  Claudedio FM — DJ Cara Voice Generator")
    print("=" * 45)

    # API key
    if not API_KEY:
        API_KEY = input("\nEnter your ElevenLabs API key: ").strip()
    if not API_KEY:
        print("❌  No API key provided. Exiting.")
        sys.exit(1)

    # Show credits before we start
    check_credits()

    # Voice selection
    if not VOICE_ID:
        voices = list_voices()
        print()
        choice = input("Enter the # from the list above, or paste a voice ID directly: ").strip()
        if choice.isdigit():
            VOICE_ID = voices[int(choice)]["voice_id"]
            print(f"  Selected: {voices[int(choice)]['name']}  ({VOICE_ID})")
        else:
            VOICE_ID = choice
            print(f"  Using voice ID: {VOICE_ID}")

    # How many to generate?
    print()
    count_input = input("How many tracks to generate? (Enter 2 for test, or 'all' for all 58): ").strip().lower()
    if count_input == "all":
        scripts_to_run = SCRIPTS
    else:
        try:
            n = int(count_input)
            scripts_to_run = SCRIPTS[:n]
        except ValueError:
            print("❌  Invalid input. Exiting.")
            sys.exit(1)

    # Generate
    total_chars = sum(len(s[2]) for s in scripts_to_run)
    print(f"\nGenerating {len(scripts_to_run)} intro(s)  ({total_chars:,} characters)...\n")

    for track_num, title, artist, text in scripts_to_run:
        print(f"  Track {track_num:02d}: {title} — {artist}")
        try:
            generate_mp3(VOICE_ID, text, track_num)
        except requests.HTTPError as e:
            print(f"  ❌  Error: {e.response.status_code} {e.response.text}")
            break
        time.sleep(0.4)  # gentle rate limiting

    # Show credits after
    check_credits()

    print(f"\n✅  Done! MP3s saved to ./{OUTPUT_DIR}/")
    print("     Listen to them, then re-run and choose 'all' to generate the full set.")


if __name__ == "__main__":
    main()

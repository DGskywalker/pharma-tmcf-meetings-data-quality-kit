"""
60-Second Explainer Video Generator for Meridian BioPharma Global Operations
Renders an enterprise motion-graphic explainer video (720p HD, 60.0s, synchronized captions,
smooth animated progress bar, scene transitions, and synthesized corporate audio track).

[CONFIDENTIAL - FOR SIMULATION & DEMO PURPOSES ONLY - ALL DATA IS 100% SYNTHETIC]
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import subprocess

VIDEO_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(VIDEO_DIR)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

FPS = 20
DURATION_SEC = 60
TOTAL_FRAMES = FPS * DURATION_SEC
WIDTH = 1280
HEIGHT = 720

# Colors
NAVY = (15, 23, 42)
SLATE = (30, 41, 59)
TEAL = (13, 148, 136)
CYAN = (6, 182, 212)
RED = (225, 29, 72)
AMBER = (217, 119, 6)
WHITE = (255, 255, 255)
LIGHT_GRAY = (241, 245, 249)
MUTED = (148, 163, 184)

# 6 Structured Scenes (10 seconds each)
SCENES = [
    {
        "start": 0, "end": 10,
        "tag": "GLOBAL PHARMA COMPLIANCE",
        "title": "Why Meeting Data Quality Matters",
        "subtitle": "US Sunshine Act (42 CFR Part 403) & EFPIA Transparency",
        "bullets": [
            "• Medical meetings connect researchers with Key Opinion Leaders (HCPs)",
            "• Every meal, flight, and honorarium is statutory Transfer of Value (ToV)",
            "• Inaccurate or missing records trigger federal penalties up to $1,000,000"
        ],
        "stat": "TARGET: 100% DISCLOSURE ACCURACY",
        "stat_color": CYAN,
        "caption": "In global pharma, every medical meeting carries strict federal compliance mandates."
    },
    {
        "start": 10, "end": 20,
        "tag": "ENTERPRISE ARCHITECTURE",
        "title": "The End-to-End Meeting Lifecycle",
        "subtitle": "Connecting 6 Disparate Systems Across the Organization",
        "bullets": [
            "1. Intake & Requester: Business Need & WBS Budget Allocation",
            "2. Medical Compliance: Fair Market Value (FMV) & Cross-Border Check",
            "3. SMM & Travel: Cvent Registration, Amex GBT Flights & Fleet Shuttles",
            "4. Expense & ERP: Concur Folio Matching & Snowflake Spend Lake"
        ],
        "stat": "6 SWIMLANES • $224M AUDITED SPEND",
        "stat_color": TEAL,
        "caption": "Meetings travel through six distinct swimlanes from initiation to federal filing."
    },
    {
        "start": 20, "end": 30,
        "tag": "DATA LEAKAGE POINTS",
        "title": "Where Critical Data Goes Missing",
        "subtitle": "The 3 Most Severe Disconnects in the Enterprise Pipeline",
        "bullets": [
            "DLP-1: Rogue Booking - Direct hotel contracts bypass Cvent SMM intake",
            "DLP-2: Missing NPIs - Unverified physician tax IDs delay disclosure",
            "DLP-4: Virtual Card Orphans - Hotel folios lack Cvent Meeting ID reference"
        ],
        "stat": "329 FLAGGED EXCEPTIONS DETECTED",
        "stat_color": RED,
        "caption": "Data leakage points create invisible spend, unallocated balances, and audit fines."
    },
    {
        "start": 30, "end": 40,
        "tag": "CRITICAL RISK SPOTLIGHT",
        "title": "The 14-Day Roster Crisis & 'Ghost HCPs'",
        "subtitle": "Why Late Attendance Sign-In Sheets Are Our #1 Vulnerability",
        "bullets": [
            "• 184 meetings exceeded the mandatory 14-day post-event upload SLA",
            "• Preliminary invite lists mistakenly report no-show physicians to CMS",
            "• Physicians dispute false meal allocations during the 45-day review window",
            "• Result: Costly legal audits, physician friction, and compliance scrutiny"
        ],
        "stat": "$13.7M SUNSHINE SPEND EXPOSURE",
        "stat_color": RED,
        "caption": "When attendee rosters are late, non-attending physicians are falsely reported to CMS."
    },
    {
        "start": 40, "end": 50,
        "tag": "OPERATIONAL REMEDIATION",
        "title": "The Requester 4-Point Golden Rule",
        "subtitle": "Follow These 4 Steps to Guarantee Clean Compliance",
        "bullets": [
            "1. Cvent ID First: Never book a venue without an approved SMM Meeting ID",
            "2. Validate NPI: Use live CMS NPPES lookup for all US medical professionals",
            "3. Roster in 14 Days: Upload verified sign-in sheets immediately after event",
            "4. Concur WBS Sync: Attach the exact clinical trial WBS to your expense report"
        ],
        "stat": "PREVENTION AT SOURCE ELIMINATES 85% OF ERRORS",
        "stat_color": TEAL,
        "caption": "Remember the 4-point golden rule: Cvent ID first, check NPI, roster in 14 days, sync WBS."
    },
    {
        "start": 50, "end": 60,
        "tag": "STRATEGIC VISION",
        "title": "Target: 95% Data Quality Excellence",
        "subtitle": "Transforming Meetings Governance at Meridian BioPharma",
        "bullets": [
            "• Hard Stop Policy: 'No Cvent ID, No Payment' enforced in Concur & Cards",
            "• Automated Nudges: Day +7 and +14 alerts to meeting organizers and BU VPs",
            "• Continuous Audit: Real-time Snowflake Spend Lake anomaly surveillance",
            "• Visit the PharmaInsights Hub for interactive tools, scorecards, and templates"
        ],
        "stat": "OCTOBER MILESTONE: >= 95.0% PORTFOLIO ACCURACY",
        "stat_color": CYAN,
        "caption": "Explore the PharmaInsights Hub today to keep our meetings compliant, efficient, and clean."
    }
]


def generate_audio_track(wav_path):
    """Synthesizes a pleasant corporate background melody with audio cues."""
    sample_rate = 44100
    total_samples = sample_rate * DURATION_SEC
    t = np.linspace(0, DURATION_SEC, total_samples, endpoint=False)
    
    # Base warm drone chord (Cmaj9 / Fmaj9 progression every 10s)
    audio = np.zeros(total_samples, dtype=np.float32)

    # Chords frequencies (C, E, G, B, D) and (F, A, C, E, G)
    chords = [
        [130.81, 164.81, 196.00, 246.94], # Cmaj7
        [146.83, 174.61, 220.00, 261.63], # Dm7
        [164.81, 196.00, 246.94, 293.66], # Em7
        [174.61, 220.00, 261.63, 329.63], # Fmaj7
        [196.00, 246.94, 293.66, 349.23], # G7
        [130.81, 164.81, 196.00, 261.63], # Cmaj
    ]

    for sec_idx in range(6):
        chord = chords[sec_idx]
        start_samp = sec_idx * 10 * sample_rate
        end_samp = (sec_idx + 1) * 10 * sample_rate
        t_sub = t[start_samp:end_samp] - (sec_idx * 10)
        
        # Envelope: subtle fade in / fade out
        env = np.sin(np.pi * (t_sub / 10.0)) ** 0.5
        
        chord_wave = np.zeros(len(t_sub), dtype=np.float32)
        for freq in chord:
            chord_wave += 0.08 * np.sin(2 * np.pi * freq * t_sub)
            chord_wave += 0.02 * np.sin(2 * np.pi * (freq * 2) * t_sub) # harmonic

        # Scene transition chime at start of scene
        chime_env = np.exp(-t_sub * 2.5)
        chime_wave = 0.12 * np.sin(2 * np.pi * 880 * t_sub) * chime_env + 0.08 * np.sin(2 * np.pi * 1320 * t_sub) * chime_env
        
        audio[start_samp:end_samp] += (chord_wave * env) + chime_wave

    # Normalize and write 16-bit PCM WAV
    audio = audio / (np.max(np.abs(audio)) + 1e-6) * 0.75
    audio_int16 = (audio * 32767).astype(np.int16)

    import wave
    with wave.open(wav_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())
    print(f"Generated Audio Track: {wav_path}")


def render_video_frames(raw_video_path):
    """Renders all 1,200 frames and streams to ffmpeg pipe."""
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    # Try to load Arial or default system fonts
    try:
        font_tag = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
        font_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
        font_stat = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
        font_caption = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    except Exception:
        font_tag = font_title = font_sub = font_body = font_stat = font_caption = ImageFont.load_default()

    # Open ffmpeg subprocess
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "22",
        raw_video_path
    ]

    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    poster_saved = False
    poster_path = os.path.join(VIDEO_DIR, "video_poster.png")

    for f_idx in range(TOTAL_FRAMES):
        current_time = f_idx / FPS
        scene_idx = min(int(current_time // 10), len(SCENES) - 1)
        scene = SCENES[scene_idx]

        # Canvas Image
        img = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
        draw = ImageDraw.Draw(img)

        # Header Ribbon
        draw.rectangle([0, 0, WIDTH, 75], fill=(15, 23, 42))
        draw.line([0, 75, WIDTH, 75], fill=TEAL, width=3)
        draw.text((40, 26), "MERIDIAN BIOPHARMA GLOBAL OPERATIONS", fill=CYAN, font=font_tag)
        draw.text((WIDTH - 380, 26), "MEETINGS DATA QUALITY EXPLAINER", fill=WHITE, font=font_tag)

        # Progress Bar at Bottom
        progress_pct = (f_idx + 1) / TOTAL_FRAMES
        draw.rectangle([0, HEIGHT - 12, WIDTH, HEIGHT], fill=(30, 41, 59))
        draw.rectangle([0, HEIGHT - 12, int(WIDTH * progress_pct), HEIGHT], fill=TEAL)

        # Time Indicator (e.g. 0:24 / 1:00)
        mins = int(current_time) // 60
        secs = int(current_time) % 60
        draw.text((WIDTH - 140, 44), f"0:{secs:02d} / 1:00", fill=MUTED, font=font_tag)

        # Scene Content Box (Card)
        draw.rounded_rectangle([60, 105, WIDTH - 60, HEIGHT - 130], radius=14, fill=SLATE, outline=(51, 65, 85), width=2)

        # Scene Tag & Title
        draw.text((90, 130), scene["tag"], fill=TEAL, font=font_tag)
        draw.text((90, 155), scene["title"], fill=WHITE, font=font_title)
        draw.text((90, 202), scene["subtitle"], fill=MUTED, font=font_sub)
        draw.line([90, 235, WIDTH - 90, 235], fill=(51, 65, 85), width=1)

        # Bullets
        y_text = 255
        for b_text in scene["bullets"]:
            draw.text((90, y_text), b_text, fill=(241, 245, 249), font=font_body)
            y_text += 42

        # Bottom Stat Banner in Card
        draw.rounded_rectangle([90, y_text + 15, WIDTH - 90, y_text + 65], radius=8, fill=(15, 23, 42), outline=scene["stat_color"], width=1)
        draw.text((110, y_text + 26), scene["stat"], fill=scene["stat_color"], font=font_stat)

        # Bottom Synced Subtitle Banner (Black translucent strip)
        draw.rectangle([60, HEIGHT - 115, WIDTH - 60, HEIGHT - 30], fill=(0, 0, 0))
        draw.line([60, HEIGHT - 115, WIDTH - 60, HEIGHT - 115], fill=CYAN, width=2)
        draw.text((80, HEIGHT - 85), f"Voiceover: \"{scene['caption']}\"", fill=WHITE, font=font_caption)

        # Save poster frame around second 12 (Scene 2)
        if f_idx == int(FPS * 12) and not poster_saved:
            img.save(poster_path)
            img.save(os.path.join(ASSETS_DIR, "video_poster.png"))
            poster_saved = True
            print(f"Saved Video Poster: {poster_path}")

        # Pipe frame
        pipe.stdin.write(img.tobytes())

    pipe.stdin.close()
    pipe.wait()
    print(f"Rendered Visual Stream: {raw_video_path}")


def assemble_final_video():
    """Generates audio, renders video, and muxes them into meetings_data_quality_explainer.mp4."""
    wav_path = os.path.join(VIDEO_DIR, "temp_audio.wav")
    raw_video_path = os.path.join(VIDEO_DIR, "temp_video.mp4")
    final_video_path = os.path.join(VIDEO_DIR, "meetings_data_quality_explainer.mp4")

    # 1. Audio
    generate_audio_track(wav_path)

    # 2. Video frames
    render_video_frames(raw_video_path)

    # 3. Mux audio + video with ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", raw_video_path,
        "-i", wav_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        final_video_path
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        print(f"SUCCESS: Rendered Final 60-Second Explainer Video: {final_video_path}")
    else:
        print(f"Muxing failed: {res.stderr.decode()}")

    # Cleanup temp
    if os.path.exists(wav_path):
        os.remove(wav_path)
    if os.path.exists(raw_video_path):
        os.remove(raw_video_path)


if __name__ == "__main__":
    assemble_final_video()

import os
import json
import re
import shutil
import subprocess
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from groq import Groq
import yt_dlp

app = FastAPI(title="Emvic Clipper")

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")
app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "static", "index.html")

DEFAULT_GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
RENDER_SECRET_COOKIE = "/etc/secrets/cookies.txt"
WRITABLE_COOKIE_PATH = "/tmp/cookies.txt"

task_status = {
    "status": "idle",
    "step": "",
    "clips": [],
    "error": None
}

class ClipRequest(BaseModel):
    groq_key: str = ""
    youtube_url: str
    custom_name: str = "Emvic_Clip"
    num_clips: int = 3
    aspect_ratio: str = "9:16"
    min_duration: float = 60.0
    max_duration: float = 120.0

def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[\\/*?:"<>| ]', '_', name.strip())
    return cleaned if cleaned else "Emvic_Clip"

def get_active_cookie_file():
    """Copies read-only Render secret cookies to a writable /tmp directory."""
    if os.path.exists(RENDER_SECRET_COOKIE):
        try:
            shutil.copyfile(RENDER_SECRET_COOKIE, WRITABLE_COOKIE_PATH)
            return WRITABLE_COOKIE_PATH
        except Exception:
            return RENDER_SECRET_COOKIE
    elif os.path.exists("cookies.txt"):
        return "cookies.txt"
    return None

def build_ydl_options(extra_opts=None):
    """Universal extractor settings that accept any available stream."""
    cookie_file = get_active_cookie_file()
    base_opts = {
        'quiet': True,
        'no_warnings': True,
        'overwrites': True,
        'force_keyframes_at_cuts': True,
        'socket_timeout': 30,
        'check_formats': False,
        'extractor_args': {
            'youtube': {
                'player_client': ['web_embedded', 'default', '-tv_downgraded'],
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }
    
    if cookie_file:
        base_opts['cookiefile'] = cookie_file
        
    if extra_opts:
        base_opts.update(extra_opts)
    return base_opts

def process_video_pipeline(groq_key: str, youtube_url: str, custom_name: str, num_clips: int, aspect_ratio: str, min_duration: float, max_duration: float):
    global task_status
    try:
        task_status["status"] = "processing"
        task_status["error"] = None
        task_status["clips"] = []

        safe_prefix = sanitize_filename(custom_name)
        raw_source = "temp_raw_source.mp4"
        audio_fast = "temp_audio_fast.mp3"

        # 1. Download initial media stream using universal fallback format
        task_status["step"] = "Downloading audio stream..."
        ydl_audio_opts = build_ydl_options({
            'format': 'ba/b/best',
            'download_ranges': yt_dlp.utils.download_range_func(None, [(0, 720)]),
            'outtmpl': raw_source
        })

        with yt_dlp.YoutubeDL(ydl_audio_opts) as ydl:
            ydl.download([youtube_url])

        # Convert to lightweight 16kHz mono audio for Whisper
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_source,
            "-vn", "-ac", "1", "-ar", "16000", "-b:a", "32k",
            audio_fast
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(raw_source):
            os.remove(raw_source)

        # 2. Transcribe and score high-retention viral segments
        task_status["step"] = f"Emvic AI analyzing transcript & finding top {num_clips} viral moments..."
        client = Groq(api_key=groq_key)
        with open(audio_fast, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_fast, file.read()),
                model="whisper-large-v3",
                response_format="verbose_json",
            )

        segments = [
            {"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip()}
            for s in transcription.segments
        ][:120]
        formatted_transcript = "\n".join([f"[{s['start']}s - {s['end']}s] {s['text']}" for s in segments])

        all_models = [m.id for m in client.models.list().data]
        excluded = ["whisper", "guard", "allam", "embed", "moderation", "vision"]
        chat_candidates = [m for m in all_models if not any(bad in m.lower() for bad in excluded)]

        prompt = f"""
        Analyze this transcript and select exactly {num_clips} non-overlapping, high-retention viral segments.
        RULES:
        - Each clip duration (end - start) MUST be strictly between {min_duration} and {max_duration} seconds.
        - Must have a strong curiosity hook in the first 3 seconds.

        Return ONLY a JSON list of objects:
        [
          {{"start": 20.0, "end": 90.0, "title": "Hook Title 1"}},
          {{"start": 100.0, "end": 175.0, "title": "Hook Title 2"}}
        ]

        TRANSCRIPT:
        {formatted_transcript}
        """

        clips_list = None
        for model_name in chat_candidates:
            try:
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                raw_output = completion.choices[0].message.content.strip()
                match = re.search(r"\[.*?\]", raw_output, re.DOTALL)
                if match:
                    clips_list = json.loads(match.group(0))
                    break
            except Exception:
                continue

        if not clips_list:
            clips_list = []
            segment_len = max(min_duration, 60.0)
            for i in range(num_clips):
                clips_list.append({
                    "start": i * (segment_len + 10.0),
                    "end": (i * (segment_len + 10.0)) + segment_len,
                    "title": f"Clip {i + 1}"
                })

        # 3. Dynamic Crop Filter Selection
        if aspect_ratio == "1:1":
            vf_filter = "scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080,setsar=1"
            aspect_flag = "1:1"
        elif aspect_ratio == "16:9":
            vf_filter = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1"
            aspect_flag = "16:9"
        else:
            vf_filter = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"
            aspect_flag = "9:16"

        generated_clips = []
        for idx, clip in enumerate(clips_list[:num_clips], start=1):
            start_t = float(clip["start"])
            end_t = float(clip["end"])

            duration = end_t - start_t
            if duration < min_duration:
                end_t = start_t + min_duration + 5.0
            elif duration > max_duration:
                end_t = start_t + max_duration - 5.0

            title = clip.get("title", f"Clip {idx}")
            task_status["step"] = f"Rendering {safe_prefix}_{idx}.mp4 in {aspect_ratio} ({idx}/{len(clips_list[:num_clips])})..."

            raw_chunk = f"temp_chunk_{idx}.mp4"
            filename = f"{safe_prefix}_{idx}.mp4"
            filepath = os.path.join(OUTPUT_DIR, filename)

            ydl_chunk_opts = build_ydl_options({
                'format': 'b/best/bestvideo+bestaudio',
                'download_ranges': yt_dlp.utils.download_range_func(None, [(start_t, end_t)]),
                'outtmpl': raw_chunk
            })

            with yt_dlp.YoutubeDL(ydl_chunk_opts) as ydl:
                ydl.download([youtube_url])

            subprocess.run([
                "ffmpeg", "-y",
                "-i", raw_chunk,
                "-vf", vf_filter,
                "-aspect", aspect_flag,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "0",
                "-c:a", "aac", "-b:a", "192k",
                filepath
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if os.path.exists(raw_chunk):
                os.remove(raw_chunk)

            generated_clips.append({
                "url": f"/outputs/{filename}",
                "filename": filename,
                "title": title,
                "duration": round(end_t - start_t, 1),
                "aspect": aspect_ratio
            })

        if os.path.exists(audio_fast):
            os.remove(audio_fast)

        task_status["clips"] = generated_clips
        task_status["status"] = "completed"
        task_status["step"] = "All clips ready!"

    except Exception as e:
        task_status["status"] = "error"
        task_status["error"] = str(e)

@app.get("/")
def read_root():
    if not os.path.exists(INDEX_PATH):
        return JSONResponse(status_code=404, content={"error": f"index.html missing at {INDEX_PATH}"})
    return FileResponse(INDEX_PATH)

@app.post("/api/generate")
def generate_clips(request: ClipRequest, background_tasks: BackgroundTasks):
    global task_status
    if task_status["status"] == "processing":
        return JSONResponse(status_code=400, content={"message": "Emvic Clipper is currently processing another task."})

    active_key = request.groq_key.strip() or DEFAULT_GROQ_KEY
    if not active_key:
        return JSONResponse(status_code=400, content={"message": "No Groq API key configured on server."})

    background_tasks.add_task(
        process_video_pipeline, 
        active_key, 
        request.youtube_url, 
        request.custom_name, 
        request.num_clips,
        request.aspect_ratio,
        request.min_duration,
        request.max_duration
    )
    return {"message": "Job successfully queued on Emvic Clipper"}

@app.get("/api/status")
def get_status():
    return task_status

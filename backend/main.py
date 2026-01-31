import os
import glob
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp
import uuid

app = FastAPI()

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def cleanup_file(path: str):
    """Background task to remove the file after download is complete."""
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted temp file: {path}")
    except Exception as e:
        print(f"Error cleaning up file: {e}")

@app.post("/convert")
async def convert_video(link: str, background_tasks: BackgroundTasks):
    try:
        # Generate a unique ID to avoid filename collisions
        file_id = str(uuid.uuid4())
        
        # Output template: downloads/unique_id.%(ext)s
        # yt-dlp will replace %(ext)s with 'mp3' after conversion
        output_template = os.path.join(DOWNLOAD_DIR, f"{file_id}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'EmbedThumbnail',  # Embeds the thumbnail into the MP3
                },
                {
                    'key': 'FFmpegMetadata',  # Writes metadata (artist, title)
                }
            ],
            'writethumbnail': True, # Required to download thumb for embedding
            'quiet': True,
        }

        # 1. Download and Convert
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            title = info.get('title', 'audio')
            # Sanitize title for filename safety in the browser download
            safe_filename = "".join([c for c in title if c.isalnum() or c in (' ', '.', '_')]).strip()
            if not safe_filename.endswith(".mp3"):
                safe_filename += ".mp3"

        # 2. Locate the file
        # yt-dlp might leave the original thumbnail file behind (e.g., .jpg or .webp)
        # We only want the .mp3 file.
        mp3_file = os.path.join(DOWNLOAD_DIR, f"{file_id}.mp3")
        
        if not os.path.exists(mp3_file):
            raise HTTPException(status_code=500, detail="Conversion failed, file not found.")

        # Clean up external thumbnail files immediately if they exist
        for f in glob.glob(os.path.join(DOWNLOAD_DIR, f"{file_id}.*")):
            if not f.endswith(".mp3"):
                os.remove(f)

        # 3. Schedule cleanup of the MP3 after the response is sent
        background_tasks.add_task(cleanup_file, mp3_file)

        # 4. Return the file
        return FileResponse(
            path=mp3_file, 
            filename=safe_filename, 
            media_type="audio/mpeg"
        )

    except Exception as e:
        # Cleanup if something crashed midway
        for f in glob.glob(os.path.join(DOWNLOAD_DIR, f"{file_id}*")):
            os.remove(f)
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
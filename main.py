from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Permite que tu web en GitHub Pages se comunique sin bloqueos de seguridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Astral Audio API Online"}

@app.get("/audio/{video_id}")
def get_audio_stream(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info.get('url')
            
            # Buscar el mejor flujo de audio disponible
            if not audio_url and 'formats' in info:
                for f in info['formats']:
                    if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                        audio_url = f.get('url')
                        break

            if not audio_url:
                raise HTTPException(status_code=404, detail="No se encontró el flujo de audio")

            return {
                "title": info.get('title'),
                "audio_url": audio_url
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

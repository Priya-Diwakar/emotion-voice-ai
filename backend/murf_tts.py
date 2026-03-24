import os
import requests
import base64

MURF_API_KEY = os.getenv("MURF_API_KEY", "")
MURF_API_URL = "https://api.murf.ai/v1/speech/generate"

# Murf Falcon voice ID
FALCON_VOICE_ID = "en-US-falcon"

# Emotion -> Murf style mapping
EMOTION_STYLES = {
    "happy":     "Promo",
    "sad":       "Sad",
    "angry":     "Angry",
    "anxious":   "Conversational",
    "curious":   "Conversational",
    "fearful":   "Sad",
    "disgusted": "Conversational",
    "surprised": "Promo",
    "neutral":   "Conversational",
    "calm":      "Conversational",
    "warm":      "Conversational",
}

# Emotion -> speech rate adjustment (-50 to +50)
EMOTION_RATE = {
    "happy":     10,
    "sad":       -15,
    "angry":     10,
    "anxious":   -5,
    "curious":   5,
    "fearful":   -10,
    "disgusted": -5,
    "surprised": 10,
    "neutral":   0,
    "calm":      -5,
    "warm":      0,
}


def text_to_speech(text: str, emotion: str = "neutral") -> dict:
    if not is_configured():
        return {"success": False, "error": "Murf API key not set in .env"}

    if len(text) > 500:
        text = text[:497] + "..."

    style = EMOTION_STYLES.get(emotion, "Conversational")
    rate  = EMOTION_RATE.get(emotion, 0)

    payload = {
        "voiceId":    FALCON_VOICE_ID,
        "style":      style,
        "text":       text,
        "rate":       rate,
        "pitch":      0,
        "sampleRate": 24000,
        "format":     "MP3",
        "channelType": "MONO"
    }

    headers = {
        "Content-Type": "application/json",
        "api-key":       MURF_API_KEY
    }

    try:
        resp = requests.post(MURF_API_URL, json=payload, headers=headers, timeout=20)

        if resp.status_code != 200:
            print(f"[MurfTTS] Error {resp.status_code}: {resp.text[:200]}")
            return {"success": False, "error": f"Murf API error {resp.status_code}"}

        data      = resp.json()
        audio_url = data.get("audioFile") or data.get("audio_file") or data.get("url")

        if not audio_url:
            return {"success": False, "error": "No audio URL in Murf response"}

        audio_resp = requests.get(audio_url, timeout=15)
        if audio_resp.status_code != 200:
            return {"success": False, "error": "Failed to download Murf audio"}

        audio_b64 = base64.b64encode(audio_resp.content).decode("utf-8")
        print(f"[MurfTTS] OK — voice: {FALCON_VOICE_ID}, style: {style}, emotion: {emotion}")

        return {
            "success":      True,
            "audio_base64": audio_b64,
            "format":       "mp3",
            "voice_id":     FALCON_VOICE_ID,
            "style":        style,
            "emotion":      emotion
        }

    except requests.Timeout:
        return {"success": False, "error": "Murf request timed out"}
    except Exception as e:
        print(f"[MurfTTS] Exception: {e}")
        return {"success": False, "error": str(e)}


def is_configured() -> bool:
    return bool(MURF_API_KEY and MURF_API_KEY != "your-murf-api-key-here" and len(MURF_API_KEY) > 10)


def get_status() -> dict:
    return {
        "configured": is_configured(),
        "voice_id":   FALCON_VOICE_ID,
        "styles":     list(set(EMOTION_STYLES.values()))
    }
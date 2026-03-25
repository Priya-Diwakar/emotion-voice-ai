from flask import Blueprint, request, jsonify, session
from groq import Groq
import os
from emotion_engine import detect_emotion, get_tone_instruction
from murf_tts import text_to_speech, is_configured as murf_configured, get_status as murf_status

chat_bp = Blueprint("chat", __name__)

BASE_SYSTEM_PROMPT = """You are Emotion Voice AI — an empathetic, intelligent assistant that truly listens AND answers questions fully.

RULES:
1. ALWAYS answer the user's question first — directly and clearly.
2. If the user asks about a topic (science, nature, tech, health, etc.), give a real informative answer.
3. After answering, add a warm emotional touch based on their detected emotion.
4. Keep responses 3-5 sentences unless more detail is needed.
5. End with a gentle follow-up question related to what they asked.
6. Never ignore the question. Never give only emotional responses.
7. Never sound robotic. Always sound human and caring."""

FALLBACK_RESPONSES = {
    "happy":     "That's wonderful to hear! What's been making you feel this way?",
    "sad":       "I'm really sorry you're feeling this way. What's been weighing on you?",
    "angry":     "I hear your frustration. What happened?",
    "anxious":   "Take a breath — we can work through this. What's on your mind?",
    "curious":   "Great question! What sparked your interest?",
    "fearful":   "You're safe here. What's worrying you?",
    "surprised": "That sounds surprising! Tell me more!",
    "disgusted": "I understand. What bothered you most?",
    "neutral":   "I'm here and listening. What would you like to explore today?",
}


def get_fallback(emotion):
    return FALLBACK_RESPONSES.get(emotion, FALLBACK_RESPONSES["neutral"])


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    print("\n" + "="*40)
    print("CHAT CALLED")

    data     = request.json or {}
    user_msg = data.get("message", "").strip()
    tts_on   = data.get("tts", False)

    print(f"USER: {user_msg}")

    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    # Emotion detection
    try:
        emotion_data = detect_emotion(user_msg)
        emotion      = emotion_data["emotion"]
        confidence   = emotion_data["confidence"]
        tone         = get_tone_instruction(emotion)
        print(f"EMOTION: {emotion}")
    except Exception as e:
        print(f"EMOTION ERROR: {e}")
        emotion    = "neutral"
        confidence = 0.5
        tone       = ""
        emotion_data = {"emotion": emotion, "confidence": confidence, "reason": ""}

    # Chat history
    if "history" not in session:
        session["history"] = []
    history = session["history"][-20:]

    system_prompt = f"{BASE_SYSTEM_PROMPT}\n\nEmotion context: {tone}"
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_msg})

    # Groq API
    groq_key   = os.getenv("GROQ_API_KEY", "")
    groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    ai_reply   = None

    print(f"KEY: {groq_key[:15]}... MODEL: {groq_model}")

    try:
        client = Groq(api_key=groq_key)
        resp = client.chat.completions.create(
            model=groq_model,
            messages=messages,
            max_tokens=300,
            temperature=0.75
        )
        ai_reply = resp.choices[0].message.content.strip()
        print(f"GROQ OK: {ai_reply[:60]}")
    except Exception as e:
        print(f"GROQ ERROR: {type(e).__name__}: {e}")

    used_fallback = False
    if not ai_reply:
        ai_reply      = get_fallback(emotion)
        used_fallback = True
        print("USING FALLBACK")

    print(f"REPLY: {ai_reply[:60]}")
    print("="*40)

    # Save history
    history.append({"role": "user",      "content": user_msg})
    history.append({"role": "assistant", "content": ai_reply})
    session["history"] = history
    session.modified   = True

    # Response
    response_data = {
        "reply":         ai_reply,
        "emotion":       emotion,
        "confidence":    confidence,
        "reason":        emotion_data.get("reason", ""),
        "history_len":   len(history) // 2,
        "used_fallback": used_fallback,
        "murf_ready":    murf_configured(),
    }

    # Murf TTS
    if tts_on and murf_configured():
        try:
            tts_result = text_to_speech(ai_reply, emotion)
            if tts_result.get("success"):
                response_data["audio_base64"] = tts_result["audio_base64"]
                response_data["audio_format"] = "mp3"
                response_data["voice_style"]  = tts_result.get("style", "")
                print(f"MURF OK: {tts_result.get('style')}")
        except Exception as e:
            print(f"MURF ERROR: {e}")

    return jsonify(response_data)


@chat_bp.route("/api/chat/clear", methods=["POST"])
def clear_history():
    session.pop("history", None)
    return jsonify({"status": "cleared"})


@chat_bp.route("/api/status", methods=["GET"])
def status():
    groq_key = os.getenv("GROQ_API_KEY", "")
    ms = murf_status()
    return jsonify({
        "openai":     bool(groq_key and len(groq_key) > 10),
        "model":      os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        "murf":       ms["configured"],
        "murf_voice": ms["voice_id"],
        "tts":        "murf" if ms["configured"] else "browser",
    })
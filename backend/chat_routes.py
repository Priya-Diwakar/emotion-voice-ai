from flask import Blueprint, request, jsonify
from groq import Groq
import os
from emotion_engine import detect_emotion, get_tone_instruction
from murf_tts import text_to_speech, is_configured as murf_configured, get_status as murf_status

chat_bp = Blueprint("chat", __name__)

# In-memory history (fixes Render session issue)
chat_history = []

BASE_SYSTEM_PROMPT = """You are Emotion Voice AI — an empathetic and knowledgeable assistant.

MOST IMPORTANT RULE: ALWAYS answer the user's question directly and completely first.
- If they ask about machine learning, explain machine learning.
- If they ask about nature, talk about nature.
- If they ask for advice, give real practical advice.
- NEVER ignore the question and give only emotional responses.

After answering, add warmth based on their emotion.
Keep responses 3-5 sentences. End with a related follow-up question.
Never sound robotic. Always sound human and caring."""

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
    global chat_history
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
        emotion      = "neutral"
        confidence   = 0.5
        tone         = ""
        emotion_data = {"emotion": emotion, "confidence": confidence, "reason": ""}

    # Build messages with history (last 10 exchanges)
    history = chat_history[-20:]
    system_prompt = f"{BASE_SYSTEM_PROMPT}\n\nEmotion context: {tone}"
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_msg})

    # Groq API
    groq_key   = os.getenv("GROQ_API_KEY", "")
    groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    ai_reply   = None

    print(f"KEY: {'SET ' + groq_key[:15] + '...' if groq_key else 'MISSING'}")
    print(f"MODEL: {groq_model}")

    if not groq_key:
        print("ERROR: GROQ_API_KEY is not set!")
        ai_reply = get_fallback(emotion)
    else:
        try:
            client = Groq(api_key=groq_key)
            resp = client.chat.completions.create(
                model=groq_model,
                messages=messages,
                max_tokens=400,
                temperature=0.75
            )
            ai_reply = resp.choices[0].message.content.strip()
            print(f"GROQ OK: {ai_reply[:80]}")
        except Exception as e:
            print(f"GROQ ERROR TYPE: {type(e).__name__}")
            print(f"GROQ ERROR MSG:  {e}")
            ai_reply = None

    used_fallback = False
    if not ai_reply:
        ai_reply      = get_fallback(emotion)
        used_fallback = True
        print("USING FALLBACK")

    print(f"FINAL REPLY: {ai_reply[:80]}")
    print("="*40)

    # Save to in-memory history
    chat_history.append({"role": "user",      "content": user_msg})
    chat_history.append({"role": "assistant", "content": ai_reply})
    if len(chat_history) > 20:
        chat_history = chat_history[-20:]

    # Response
    response_data = {
        "reply":         ai_reply,
        "emotion":       emotion,
        "confidence":    confidence,
        "reason":        emotion_data.get("reason", ""),
        "history_len":   len(chat_history) // 2,
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
    global chat_history
    chat_history = []
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
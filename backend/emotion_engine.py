from groq import Groq
import os
import json

EMOTION_TONES = {
    "happy":     "The user is happy. Match their joyful energy — be upbeat, warm, and celebratory.",
    "sad":       "The user is sad. Be deeply gentle, empathetic, and comforting. Never minimize their feelings.",
    "angry":     "The user is angry. Stay completely calm. Validate their frustration without escalating.",
    "anxious":   "The user is anxious. Be steady, reassuring, and methodical. Use simple clear language.",
    "curious":   "The user is curious. Be enthusiastic, informative, and encouraging.",
    "fearful":   "The user is fearful. Be calm, safe, and protective. Reassure them step by step.",
    "disgusted": "The user is disgusted. Be neutral, understanding, and non-judgmental.",
    "surprised": "The user is surprised. Be engaging and share in their wonder naturally.",
    "neutral":   "The user is neutral. Be natural, clear, balanced, and conversational.",
}


def detect_emotion(text: str) -> dict:
    groq_key = os.getenv("GROQ_API_KEY", "")
    if not groq_key:
        return {"emotion": "neutral", "confidence": 0.5, "reason": "no key"}
    try:
        client = Groq(api_key=groq_key)
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an emotion detection engine. "
                        "Analyze the emotional tone of the user message. "
                        "Respond ONLY with valid JSON no explanation no markdown: "
                        '{"emotion":"<label>","confidence":<0.0-1.0>,"reason":"<10 words max>"} '
                        "Labels: happy, sad, angry, anxious, curious, fearful, disgusted, surprised, neutral"
                    )
                },
                {"role": "user", "content": text}
            ],
            max_tokens=80,
            temperature=0.2
        )
        raw = response.choices[0].message.content.strip()
        if "```" in raw:
            raw = raw.split("```")[1].lstrip("json").strip()
        result = json.loads(raw)
        emotion = result.get("emotion", "neutral")
        return {
            "emotion":    emotion,
            "confidence": round(float(result.get("confidence", 0.8)), 2),
            "reason":     result.get("reason", ""),
        }
    except Exception as e:
        print(f"[EmotionEngine] Detection failed: {e}")
        return {"emotion": "neutral", "confidence": 0.5, "reason": "detection failed"}


def get_tone_instruction(emotion: str) -> str:
    return EMOTION_TONES.get(emotion, EMOTION_TONES["neutral"])
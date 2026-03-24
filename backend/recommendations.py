from flask import Blueprint, request, jsonify
from groq import Groq
import os, json

rec_bp = Blueprint("recommendations", __name__)

FALLBACK = [
    {"title": "Stay Hydrated",  "detail": "Drink at least 8 glasses of water daily.",       "icon": "💧"},
    {"title": "Move Daily",     "detail": "Aim for 30 minutes of moderate exercise.",         "icon": "🏃"},
    {"title": "Eat Mindfully",  "detail": "Focus on whole foods, vegetables, lean protein.",  "icon": "🥗"},
    {"title": "Sleep Well",     "detail": "Get 7-9 hours of quality sleep each night.",       "icon": "😴"},
]


@rec_bp.route("/api/recommendations", methods=["POST"])
def recommendations():
    data     = request.json or {}
    bmi      = data.get("bmi", 22)
    category = data.get("category", "Normal weight")
    age      = data.get("age", 25)
    gender   = data.get("gender", "not specified")

    groq_key = os.getenv("GROQ_API_KEY", "")
    if not groq_key:
        return jsonify({"recommendations": FALLBACK})

    prompt = f"""User: BMI {bmi} ({category}), Age {age}, Gender {gender}.
Give 4 specific actionable health recommendations.
Return ONLY a JSON array no text before or after:
[{{"title":"...","detail":"...","icon":"<emoji>"}}]
Keep each detail under 20 words. Use relevant emojis."""

    try:
        client = Groq(api_key=groq_key)
        resp = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[
                {"role": "system", "content": "You are a health advisor. Return only valid JSON arrays, no markdown."},
                {"role": "user",   "content": prompt}
            ],
            max_tokens=350,
            temperature=0.6
        )
        raw = resp.choices[0].message.content.strip()
        if "```" in raw:
            raw = raw.split("```")[1].lstrip("json").strip()
        recs = json.loads(raw)
        return jsonify({"recommendations": recs})
    except Exception as e:
        print(f"[Recommendations] Error: {e}")
        return jsonify({"recommendations": FALLBACK})
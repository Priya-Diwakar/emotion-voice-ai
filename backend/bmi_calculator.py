from flask import Blueprint, request, jsonify

bmi_bp = Blueprint("bmi", __name__)


def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("Height and weight must be positive numbers.")
    h   = height_cm / 100
    bmi = round(weight_kg / (h ** 2), 1)

    if bmi < 18.5:
        category, color = "Underweight", "blue"
        advice = "Consider increasing caloric intake with nutrient-dense foods."
    elif bmi < 25.0:
        category, color = "Normal weight", "green"
        advice = "Great! Maintain your current healthy lifestyle."
    elif bmi < 30.0:
        category, color = "Overweight", "amber"
        advice = "Consider more physical activity and a balanced diet."
    else:
        category, color = "Obese", "red"
        advice = "Consult a healthcare provider for a personalized plan."

    return {"bmi": bmi, "category": category, "color": color, "advice": advice}


@bmi_bp.route("/api/bmi", methods=["POST"])
def bmi_route():
    data = request.json or {}
    try:
        weight = float(data.get("weight_kg", 0))
        height = float(data.get("height_cm", 0))
        return jsonify(calculate_bmi(weight, height))
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
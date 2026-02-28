import os
from flask import Flask, render_template, request
import re

app = Flask(__name__)

# -----------------------------------
# Risk Calculation Function
# -----------------------------------
def calculate_risk(text):
    text = text.lower()
    risk = 0

    scam_reasons = []
    genuine_reasons = []

    # -------------------------
    # SCAM INDICATORS
    # -------------------------

    # Registration / Processing Fee (High Weight)
    if "registration fee" in text or "processing fee" in text:
        if not re.search(r"(no|not|without)\s+(any\s+)?(registration|processing)\s+fee", text):
            risk += 35
            scam_reasons.append("Registration fee requested")

    # Smart Payment + Money Detection
    if re.search(r"(pay|fee|amount).*(₹?\s?\d{3,6}|\d+\s?k|\d{1,3}(,\d{3})+)", text):
            risk += 35
            scam_reasons.append("Payment with specific amount requested")

    elif re.search(r"(₹?\s?\d{3,6}|\d+\s?k|\d{1,3}(,\d{3})+)", text):
             risk += 20
             scam_reasons.append("Money amount mentioned")

    # No Interview
    if "no interview" in text or "without interview" in text:
        risk += 20
        scam_reasons.append("No proper interview process")

    # WhatsApp Only Communication
    if "whatsapp only" in text or "contact only on whatsapp" in text:
        risk += 20
        scam_reasons.append("WhatsApp only communication")

    # Work From Home + Earnings
    if "work from home" in text and re.search(r"earn|salary|income", text):
        risk += 15
        scam_reasons.append("Unrealistic work-from-home earning pattern")

    # Urgency Pressure
    if "limited vacancies" in text or "urgent joining" in text:
        risk += 10
        scam_reasons.append("Creates urgency pressure")

    # Suspicious Short Links
    if re.search(r"(bit\.ly|tinyurl|t\.me|wa\.me)", text):
        risk += 20
        scam_reasons.append("Shortened or suspicious link detected")

    # -------------------------
    # GENUINE INDICATORS
    # -------------------------

    if re.search(r"\b(interview scheduled|google meet|zoom meeting)\b", text):
        risk -= 25
        genuine_reasons.append("Proper interview process mentioned")

    if re.search(r"\b(no fee|do not charge|not charge any fee)\b", text):
        risk -= 30
        genuine_reasons.append("Clearly states no fee required")

    if re.search(r"\b(www\.\w+\.com)\b", text):
        risk -= 10
        genuine_reasons.append("Official website mentioned")

    if re.search(r"\b(hr@|careers@)\w+\.com\b", text):
        risk -= 15
        genuine_reasons.append("Official HR email detected")

    # Normalize Score
    risk = max(0, min(risk, 100))

    # Final Reasons Selection
    if risk == 0:
        reasons = genuine_reasons
        if not reasons:
            reasons = ["No suspicious patterns detected"]
    else:
        reasons = scam_reasons

    return risk, reasons


# -----------------------------------
# Routes
# -----------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    message = request.form.get('message', '')

    threat_score, reasons = calculate_risk(message)

    # Classification
    if threat_score >= 60:
        status = "THREAT"
    elif threat_score >= 25:
        status = "SUSPICIOUS"
    else:
        status = "SAFE"

    # Security Advice
    if status == "THREAT":
        advice = [
            "Do not respond to the sender.",
            "Never pay any registration or processing fees.",
            "Do not share OTP, bank details, or personal information.",
            "Report this message as spam or fraud."
        ]
    elif status == "SUSPICIOUS":
        advice = [
            "Verify the company through its official website.",
            "Avoid clicking unknown links.",
            "Be cautious before sharing personal details."
        ]
    else:
        advice = [
            "Message appears safe based on analysis.",
            "Still verify sender identity before taking action."
        ]

    return render_template(
        "result.html",
        status=status,
        threat_score=threat_score,
        reasons=reasons,
        advice=advice
    )


# -----------------------------------
# Run App
# -----------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
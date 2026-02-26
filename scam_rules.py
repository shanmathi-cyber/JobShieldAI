import re

def load_keywords():
    with open("keywords.txt", "r") as f:
        return [line.strip().lower() for line in f]

suspicious_keywords = load_keywords()

def calculate_risk(text):
    text = text.lower()
    risk = 0
    reasons = []

    # -------------------------
    # SCAM INDICATORS
    # -------------------------

    # Fee request (only if asking to pay)
    if re.search(r"pay\s+(rs\.?|₹|\d+)", text):
        risk += 35
        reasons.append("Payment requested")

    if "registration fee" in text or "processing fee" in text:
        if not re.search(r"(no|not|without)\s+(any\s+)?(registration|processing)\s+fee", text):
            risk += 25
            reasons.append("Registration fee requested")

    # No interview
    if "no interview" in text or "without interview" in text:
        risk += 20
        reasons.append("No proper interview process")

    # WhatsApp only
    if "whatsapp only" in text or "contact only on whatsapp" in text:
        risk += 20
        reasons.append("WhatsApp only communication")

    # Work from home + high earning combo
    if "work from home" in text and re.search(r"earn|salary|income", text):
        risk += 15
        reasons.append("Work from home earning pattern")

    # Urgency pressure
    if "limited vacancies" in text or "urgent joining" in text:
        risk += 10
        reasons.append("Creates urgency pressure")

    # -------------------------
    # GENUINE INDICATORS (reduce risk)
    # -------------------------

    if re.search(r"\b(interview scheduled|google meet|zoom meeting)\b", text):
        risk -= 25

    if re.search(r"\b(no fee|do not charge|not charge any fee)\b", text):
        risk -= 30

    if re.search(r"\b(www\.\w+\.com)\b", text):
        risk -= 10

    if re.search(r"\b(hr@|careers@)\w+\.com\b", text):
        risk -= 15

    # -------------------------
    # Normalize score
    # -------------------------
    risk = max(0, min(risk, 100))

    return risk, reasons
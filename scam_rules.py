import re

def load_keywords():
    with open("keywords.txt", "r") as f:
        return [line.strip().lower() for line in f]

suspicious_keywords = load_keywords()

def calculate_risk(text):
    score = 0
    reasons = []
    text = text.lower()

    for keyword in suspicious_keywords:
        if keyword in text:
            score += 1
            reasons.append(f"Keyword detected: {keyword}")

    if "security deposit" in text:
        score += 3    
        reasons.append("Suspicious phone number detected")

    return score, reasons


def classify_risk(score):
    if score >= 5:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    else:
        return "LOW"
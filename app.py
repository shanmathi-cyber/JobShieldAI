
from flask import Flask, render_template, request
from scam_rules import calculate_risk, classify_risk

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/scan', methods=['POST'])
def scan():
    job_text = request.form['job_text']

    score, reasons = calculate_risk(job_text)
    risk_level = classify_risk(score)

    return render_template(
        "index.html",
        score=score,
        risk_level=risk_level,
        reasons=reasons
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
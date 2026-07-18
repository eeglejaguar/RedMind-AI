from flask import Flask, request, render_template_string
from markupsafe import Markup

app = Flask(__name__)

SAFE_TEMPLATE = """
<!doctype html>
<html>
  <head><meta charset="utf-8"><title>Echo - Safe</title></head>
  <body>
    <h1>Echo Page (safe)</h1>
    <p>q = {{ q }}</p>
  </body>
</html>
"""

VULN_TEMPLATE = """
<!doctype html>
<html>
  <head><meta charset="utf-8"><title>Echo - Vulnerable</title></head>
  <body>
    <h1>Echo Page (vulnerable)</h1>
    <p>q = {{ q|safe }}</p>
  </body>
</html>
"""

SQLSIM_TEMPLATE = """
<!doctype html>
<html>
  <head><meta charset="utf-8"><title>SQLSim</title></head>
  <body>
    <h1>SQLSim</h1>
    <p>Query = {{ q }}</p>
    {% if error %}
    <pre style="color:red;">{{ error }}</pre>
    {% endif %}
  </body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "")
    return render_template_string(SAFE_TEMPLATE, q=q)

@app.route("/vulnerable", methods=["GET"])
def vulnerable():
    q = request.args.get("q", "")
    # Intentional unescaped reflection for local testing only
    return render_template_string(VULN_TEMPLATE, q=Markup(q))

@app.route("/sqlsim", methods=["GET"])
def sqlsim():
    q = request.args.get("q", "")
    # Naive simulation: if payload contains typical SQLi markers, show fake SQL error
    low = (q or "").lower()
    error = None
    if ("or 1=1" in low) or ("' or '" in low) or (";--" in low) or ("union select" in low) or ("sql" in low and ("error" in low or "syntax" in low)):
        error = "You have an error in your SQL syntax near " + repr(q)  # fake error text
    return render_template_string(SQLSIM_TEMPLATE, q=q, error=error)

if __name__ == "__main__":
    # run on port 3001
    app.run(host="127.0.0.1", port=3001, debug=True)

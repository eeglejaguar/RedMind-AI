from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html>
  <head><meta charset="utf-8"><title>Echo</title></head>
  <body>
    <h1>Echo Page</h1>
    <p>q = {{ q }}</p>
  </body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "")
    # Ye line intentionally escape nahi karti (testing purpose ke liye)
    return render_template_string(TEMPLATE, q=q)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3001, debug=True)

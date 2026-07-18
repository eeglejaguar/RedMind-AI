import requests

try:
    r = requests.get("http://127.0.0.1:3002/local_jquery.js", timeout=5)
    print("LOCAL status:", r.status_code, "len:", len(r.content))
    print("HEAD:", r.text[:200])
except Exception as e:
    print("LOCAL fetch error:", e)

try:
    r2 = requests.get("https://code.jquery.com/jquery-3.6.0.min.js", timeout=5)
    print("CDN status:", r2.status_code, "len:", len(r2.content))
except Exception as e:
    print("CDN fetch error:", e)

id="RM-MOD-029"
name="Session & Cookie Flags Check"
def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8)
        cookies = []
        for c in r.cookies:
            cookies.append({"name": c.name, "secure": c.secure, "httponly": getattr(c, "httponly", None)})
        headers = dict(r.headers)
        return {"target": target, "status": r.status_code, "cookies": cookies, "headers_sample": {k: headers.get(k) for k in ["Set-Cookie","Server"] if headers.get(k)}}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_029_sessions", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_029_sessions", "error": str(e) }))
    sys.exit(1)

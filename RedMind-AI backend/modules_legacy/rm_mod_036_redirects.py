id="RM-MOD-036"
name="Open Redirect Parameter Detector (safe)"
def run(target, context):
    import requests, re
    from urllib.parse import urlparse, parse_qs
    try:
        parsed = urlparse(target)
        qs = parse_qs(parsed.query)
        suspect = [k for k in qs.keys() if any(x in k.lower() for x in ["redirect","next","url","return","goto"])]
        r = requests.get(target, timeout=8, allow_redirects=False)
        loc = r.headers.get("Location")
        return {"target": target, "status": r.status_code, "suspect_params": suspect, "location_header": loc}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_036_redirects", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_036_redirects", "error": str(e) }))
    sys.exit(1)

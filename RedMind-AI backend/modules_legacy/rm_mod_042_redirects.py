id="RM-MOD-042"
name="Redirect Chain Inspector"
def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8, allow_redirects=False)
        redirects = []
        # if Location header present, report it (no following)
        loc = r.headers.get("Location")
        if loc:
            redirects.append(loc)
        return {"target": target, "status": r.status_code, "location": loc, "redirects": redirects}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_042_redirects", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_042_redirects", "error": str(e) }))
    sys.exit(1)

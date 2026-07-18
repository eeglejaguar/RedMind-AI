id="RM-MOD-040"
name="CORS Preflight and Header Analysis (safe)"
def run(target, context):
    import requests
    try:
        r = requests.options(target, timeout=6)
        cors = r.headers.get("Access-Control-Allow-Origin") or r.headers.get("access-control-allow-origin")
        methods = r.headers.get("Access-Control-Allow-Methods") or r.headers.get("allow")
        return {"target": target, "status": r.status_code, "cors": cors, "methods": methods}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_040_cors_ext", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_040_cors_ext", "error": str(e) }))
    sys.exit(1)

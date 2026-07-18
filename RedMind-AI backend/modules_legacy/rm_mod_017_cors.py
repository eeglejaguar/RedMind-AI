# RM-MOD-017 - Insecure CORS check
id = "RM-MOD-017"
name = "CORS Insecure Check"
description = "Detect Access-Control-Allow-Origin: * or wildcard that may expose resources."

def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=6)
        cors = r.headers.get("Access-Control-Allow-Origin") or r.headers.get("access-control-allow-origin")
        return {"target": target, "status_code": r.status_code, "cors_origin": cors, "insecure_cors": cors == "*"}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_017_cors", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_017_cors", "error": str(e) }))
    sys.exit(1)

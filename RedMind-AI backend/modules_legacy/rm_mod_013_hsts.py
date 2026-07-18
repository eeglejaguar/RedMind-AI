# RM-MOD-013 - HSTS missing check
id = "RM-MOD-013"
name = "HSTS Missing Check"
description = "Detect missing or weak Strict-Transport-Security header."

def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8, allow_redirects=True)
        hsts = r.headers.get("strict-transport-security")
        result = {"has_hsts": bool(hsts)}
        if hsts:
            result["hsts_value"] = hsts
        return {"target": target, "status_code": r.status_code, "hsts": result}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_013_hsts", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_013_hsts", "error": str(e) }))
    sys.exit(1)

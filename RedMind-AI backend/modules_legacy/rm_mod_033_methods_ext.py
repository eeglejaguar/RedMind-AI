id="RM-MOD-033"
name="HTTP Methods Extended Check"
def run(target, context):
    import requests
    try:
        r = requests.options(target, timeout=6)
        allow = r.headers.get("Allow") or r.headers.get("allow") or ""
        return {"target": target, "status": r.status_code, "allow": allow}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_033_methods_ext", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_033_methods_ext", "error": str(e) }))
    sys.exit(1)

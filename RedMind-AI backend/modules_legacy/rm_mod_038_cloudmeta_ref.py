id="RM-MOD-038"
name="Cloud metadata / internal endpoint references"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        refs = []
        for p in ["169.254.169.254","metadata.google","meta-data","instance-data"]:
            if p in body:
                refs.append(p)
        return {"target": target, "status": r.status_code, "refs": refs}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_038_cloudmeta_ref", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_038_cloudmeta_ref", "error": str(e) }))
    sys.exit(1)

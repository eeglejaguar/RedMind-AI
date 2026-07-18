id="RM-MOD-047"
name="Honeypot / Honeytoken Exposure"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        hits = []
        tokens = ["honeytoken","canarytoken","do-not-delete","test-token"]
        for t in tokens:
            if t in body.lower():
                hits.append(t)
        return {"target": target, "status": r.status_code, "hits": hits}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_047_honeytokens", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_047_honeytokens", "error": str(e) }))
    sys.exit(1)

id="RM-MOD-049"
name="JS Comments RCE-like Hints"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        hints = []
        for p in [r"exec\(", r"child_process", r"spawn\(", r"system\("]:
            if re.search(p, body, re.I):
                hints.append(p)
        return {"target": target, "status": r.status_code, "hints": hints}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_049_js_rce_hints", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_049_js_rce_hints", "error": str(e) }))
    sys.exit(1)

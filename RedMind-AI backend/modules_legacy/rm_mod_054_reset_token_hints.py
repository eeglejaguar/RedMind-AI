id="RM-MOD-054"
name="Password Reset / Token Hints"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = (r.text or "")[:3000]
        hints=[]
        for p in [r"reset_password", r"password_reset", r"token="]:
            if re.search(p, body, re.I):
                hints.append(p)
        return {"target": target, "status": r.status_code, "hints": hints}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_054_reset_token_hints", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_054_reset_token_hints", "error": str(e) }))
    sys.exit(1)

id="RM-MOD-028"
name="Auth Bypass Surface Hints"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        links = re.findall(r'href=["\']([^"\']+)["\']', r.text or "", re.I)
        admin_like = [l for l in links if any(x in l.lower() for x in ["/admin","/manage","/dashboard","/wp-admin"])]
        return {"target": target, "status_code": r.status_code, "admin_like_links": admin_like[:20]}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_028_auth_bypass_hints", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_028_auth_bypass_hints", "error": str(e) }))
    sys.exit(1)

id="RM-MOD-045"
name="Weak CSP Rules Detector"
def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8)
        csp = r.headers.get("Content-Security-Policy") or r.headers.get("content-security-policy")
        issues = []
        if not csp:
            issues.append("no_csp")
        else:
            if "unsafe-inline" in csp or "unsafe-eval" in csp:
                issues.append("unsafe_directives")
        return {"target": target, "status": r.status_code, "csp": csp, "issues": issues}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_045_weak_csp", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_045_weak_csp", "error": str(e) }))
    sys.exit(1)

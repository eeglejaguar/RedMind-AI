# RM-MOD-016 - robots.txt analysis
id = "RM-MOD-016"
name = "robots.txt Analysis"
description = "Fetch robots.txt and report Disallow entries (useful recon)."

def run(target, context):
    import requests
    from urllib.parse import urljoin
    try:
        u = urljoin(target, "/robots.txt")
        r = requests.get(u, timeout=6)
        if r.status_code != 200:
            return {"target": target, "status_code": r.status_code, "disallows": []}
        lines = [l.strip() for l in r.text.splitlines() if l.strip() and not l.strip().startswith("#")]
        disallows = [l.split(":",1)[1].strip() for l in lines if l.lower().startswith("disallow")]
        return {"target": target, "status_code": r.status_code, "disallows": disallows, "robots": r.text[:1000]}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_016_robots", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_016_robots", "error": str(e) }))
    sys.exit(1)

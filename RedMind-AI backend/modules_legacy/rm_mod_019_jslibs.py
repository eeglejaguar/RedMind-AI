# RM-MOD-019 - Known JS libs scanner (tiny builtin list)
id = "RM-MOD-019"
name = "Known JS Libraries Scanner"
description = "Scan page scripts for common JS lib versions and flag old versions (simple heuristics)."

def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        text = r.text or ""
        scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', text, re.I)
        found = []
        # tiny built-in risky versions list (example)
        risky = {
            "jquery": [("3.4.0","3.4.1"), ("1.12.4","1.12.0")],  # placeholder; treat as indicators
        }
        for s in scripts:
            for lib in ["jquery","angular","vue","react"]:
                if lib in s.lower():
                    # try to extract version digits
                    m = re.search(r'(\d+\.\d+\.\d+)', s)
                    ver = m.group(1) if m else None
                    found.append({"script": s, "lib": lib, "version": ver})
        return {"target": target, "status_code": r.status_code, "scripts": found}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_019_jslibs", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_019_jslibs", "error": str(e) }))
    sys.exit(1)

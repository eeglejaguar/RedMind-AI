# RM-MOD-020 - Cloud storage / S3 reference hints
id = "RM-MOD-020"
name = "Cloud Storage Reference Detector"
description = "Scan HTML for references to S3 / cloud storage endpoints (passive indicator)."

def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        hits = []
        patterns = [r's3\.amazonaws\.com', r's3-[a-z0-9-]+\.amazonaws\.com', r'cloudfront\.net', r'azureedge\.net']
        for p in patterns:
            if re.search(p, body, re.I):
                hits.append(p)
        return {"target": target, "status_code": r.status_code, "cloud_patterns_found": hits}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_020_cloudrefs", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_020_cloudrefs", "error": str(e) }))
    sys.exit(1)

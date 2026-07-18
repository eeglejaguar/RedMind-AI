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

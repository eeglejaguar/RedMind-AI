id="RM-MOD-058"
name="OAuth Callback / client_id Detector"
def run(target, context):
    import requests, re
    from urllib.parse import urlparse, parse_qs
    try:
        parsed = urlparse(target)
        qs = parse_qs(parsed.query)
        hints = []
        if "client_id" in qs or any("oauth" in k.lower() for k in qs.keys()):
            hints.append(list(qs.keys()))
        r = requests.get(target, timeout=8)
        return {"target": target, "status": r.status_code, "qs_keys": list(qs.keys()), "hints": hints}
    except Exception as e:
        return {"target": target, "error": str(e)}

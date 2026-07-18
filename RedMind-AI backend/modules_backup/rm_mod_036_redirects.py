id="RM-MOD-036"
name="Open Redirect Parameter Detector (safe)"
def run(target, context):
    import requests, re
    from urllib.parse import urlparse, parse_qs
    try:
        parsed = urlparse(target)
        qs = parse_qs(parsed.query)
        suspect = [k for k in qs.keys() if any(x in k.lower() for x in ["redirect","next","url","return","goto"])]
        r = requests.get(target, timeout=8, allow_redirects=False)
        loc = r.headers.get("Location")
        return {"target": target, "status": r.status_code, "suspect_params": suspect, "location_header": loc}
    except Exception as e:
        return {"target": target, "error": str(e)}

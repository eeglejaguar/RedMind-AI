# RM-MOD-018 - JSONP callback detection
id = "RM-MOD-018"
name = "JSONP / callback Endpoint Detection"
description = "Try adding callback parameter and look for function-wrapped JSON (naive)."

def run(target, context):
    import requests
    from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
    try:
        parsed = urlparse(target)
        qs = dict(parse_qsl(parsed.query))
        param = context.get("param") or "callback"
        qs[param] = "testcb"
        new = urlunparse(parsed._replace(query=urlencode(qs)))
        r = requests.get(new, timeout=6)
        body = (r.text or "")[:2000]
        jsonp = body.strip().startswith("testcb(") or ("testcb(" in body)
        return {"target": target, "probe_url": new, "status_code": r.status_code, "jsonp": jsonp, "snippet": body[:400]}
    except Exception as e:
        return {"target": target, "error": str(e)}

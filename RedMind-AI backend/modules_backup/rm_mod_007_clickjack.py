# RM-MOD-007 - Clickjacking header check
id = "RM-MOD-007"
name = "Clickjacking Header (X-Frame-Options / CSP frame-ancestors) Check"
description = "Detect missing X-Frame-Options and missing frame-ancestors CSP."

def run(target, context):
    import requests
    r = None
    try:
        r = requests.get(target, timeout=8)
        headers = {k:v for k,v in r.headers.items()}
        xfo = headers.get("x-frame-options") or headers.get("X-Frame-Options")
        csp = headers.get("content-security-policy") or headers.get("Content-Security-Policy") or ""
        frame_ancestors = "frame-ancestors" in csp.lower()
        return {"target":target,"status_code": r.status_code,"x_frame_options": bool(xfo), "csp_frame_ancestors": bool(frame_ancestors),"headers":headers}
    except Exception as e:
        return {"target":target,"error":str(e)}

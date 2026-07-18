# RM-MOD-011 - Content Security Policy (CSP) missing check
id = "RM-MOD-011"
name = "CSP Header Missing Check"
description = "Check if Content-Security-Policy header exists and includes script-src/frame-ancestors."

def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8)
        headers = dict(r.headers)
        csp = headers.get("Content-Security-Policy") or headers.get("content-security-policy")
        has_csp = bool(csp)
        script_src = "script-src" in (csp or "").lower()
        frame_ancestors = "frame-ancestors" in (csp or "").lower()
        return {"target":target,"status_code":r.status_code,"has_csp":has_csp,"script_src":script_src,"frame_ancestors":frame_ancestors,"csp":csp}
    except Exception as e:
        return {"target":target,"error":str(e)}

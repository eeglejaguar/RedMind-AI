# RM-MOD-009 - Server banner check
id = "RM-MOD-009"
name = "Server Banner / Version Disclosure Check"
description = "Return Server header and common security-related headers."

def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8)
        headers = dict(r.headers)
        server = headers.get("server")
        x_powered_by = headers.get("x-powered-by")
        return {"target":target,"status_code":r.status_code,"server_header":server,"x_powered_by":x_powered_by,"headers":headers}
    except Exception as e:
        return {"target":target,"error":str(e)}

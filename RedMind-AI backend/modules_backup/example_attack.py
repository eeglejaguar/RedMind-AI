id = "RM-MOD-001"
name = "X-Powered-By Header Check"
description = "Simple module: GET request and return X-Powered-By header"

def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=6)
        header = r.headers.get("X-Powered-By") or r.headers.get("x-powered-by") or "Not Found"
        return {"target": target, "status_code": r.status_code, "x_powered_by": header}
    except Exception as e:
        return {"error": str(e)}

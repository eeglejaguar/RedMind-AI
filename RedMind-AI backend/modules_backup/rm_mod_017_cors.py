# RM-MOD-017 - Insecure CORS check
id = "RM-MOD-017"
name = "CORS Insecure Check"
description = "Detect Access-Control-Allow-Origin: * or wildcard that may expose resources."

def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=6)
        cors = r.headers.get("Access-Control-Allow-Origin") or r.headers.get("access-control-allow-origin")
        return {"target": target, "status_code": r.status_code, "cors_origin": cors, "insecure_cors": cors == "*"}
    except Exception as e:
        return {"target": target, "error": str(e)}

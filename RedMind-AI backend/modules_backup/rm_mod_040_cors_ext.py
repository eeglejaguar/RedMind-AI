id="RM-MOD-040"
name="CORS Preflight and Header Analysis (safe)"
def run(target, context):
    import requests
    try:
        r = requests.options(target, timeout=6)
        cors = r.headers.get("Access-Control-Allow-Origin") or r.headers.get("access-control-allow-origin")
        methods = r.headers.get("Access-Control-Allow-Methods") or r.headers.get("allow")
        return {"target": target, "status": r.status_code, "cors": cors, "methods": methods}
    except Exception as e:
        return {"target": target, "error": str(e)}

id="RM-MOD-033"
name="HTTP Methods Extended Check"
def run(target, context):
    import requests
    try:
        r = requests.options(target, timeout=6)
        allow = r.headers.get("Allow") or r.headers.get("allow") or ""
        return {"target": target, "status": r.status_code, "allow": allow}
    except Exception as e:
        return {"target": target, "error": str(e)}

id="RM-MOD-059"
name="Rate Limit / Throttle Hints"
def run(target, context):
    import requests
    try:
        r = requests.head(target, timeout=6)
        headers = {}
        for k in r.headers:
            if "rate" in k.lower() or "retry" in k.lower() or "limit" in k.lower():
                headers[k]=r.headers[k]
        return {"target": target, "status": r.status_code, "rate_headers": headers}
    except Exception as e:
        return {"target": target, "error": str(e)}

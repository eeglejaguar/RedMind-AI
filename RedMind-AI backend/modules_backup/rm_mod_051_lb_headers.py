id="RM-MOD-051"
name="Load Balancer / Proxy Header Heuristics"
def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8)
        hdrs = r.headers
        interesting = {}
        for h in ["Via","X-Forwarded-For","X-Real-IP","Server"]:
            if h in hdrs:
                interesting[h] = hdrs.get(h)
        return {"target": target, "status": r.status_code, "interesting_headers": interesting}
    except Exception as e:
        return {"target": target, "error": str(e)}

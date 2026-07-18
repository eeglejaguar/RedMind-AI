id="RM-MOD-047"
name="Honeypot / Honeytoken Exposure"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        hits = []
        tokens = ["honeytoken","canarytoken","do-not-delete","test-token"]
        for t in tokens:
            if t in body.lower():
                hits.append(t)
        return {"target": target, "status": r.status_code, "hits": hits}
    except Exception as e:
        return {"target": target, "error": str(e)}

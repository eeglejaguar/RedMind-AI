id="RM-MOD-042"
name="Redirect Chain Inspector"
def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8, allow_redirects=False)
        redirects = []
        # if Location header present, report it (no following)
        loc = r.headers.get("Location")
        if loc:
            redirects.append(loc)
        return {"target": target, "status": r.status_code, "location": loc, "redirects": redirects}
    except Exception as e:
        return {"target": target, "error": str(e)}

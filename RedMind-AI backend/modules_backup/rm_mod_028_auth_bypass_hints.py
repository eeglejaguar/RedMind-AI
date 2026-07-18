id="RM-MOD-028"
name="Auth Bypass Surface Hints"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        links = re.findall(r'href=["\']([^"\']+)["\']', r.text or "", re.I)
        admin_like = [l for l in links if any(x in l.lower() for x in ["/admin","/manage","/dashboard","/wp-admin"])]
        return {"target": target, "status_code": r.status_code, "admin_like_links": admin_like[:20]}
    except Exception as e:
        return {"target": target, "error": str(e)}

id="RM-MOD-039"
name="Management Interface Presence (safe HEAD/GET)"
def run(target, context):
    import requests
    from urllib.parse import urljoin
    try:
        base = target.rstrip("/")
        candidates = ["/phpmyadmin/","/server-status","/manager/html","/admin/"]
        results=[]
        for c in candidates:
            u = urljoin(base, c)
            try:
                r = requests.head(u, timeout=5, allow_redirects=True)
                results.append({"path":c,"status": r.status_code})
            except Exception as e:
                results.append({"path":c,"error": str(e)})
        return {"target": target, "checks": results}
    except Exception as e:
        return {"target": target, "error": str(e)}

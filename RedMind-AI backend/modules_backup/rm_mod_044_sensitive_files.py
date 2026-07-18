id="RM-MOD-044"
name="Sensitive File Types Served"
def run(target, context):
    import requests, re
    from urllib.parse import urljoin
    try:
        candidates = ["/.git/config","/.env","/id_rsa","/server.key",".pem",".sql",".bak"]
        findings = []
        for c in candidates:
            u = urljoin(target, c)
            try:
                h = requests.head(u, timeout=5, allow_redirects=True)
                if h.status_code == 200:
                    findings.append({"path": c, "status": h.status_code, "content_type": h.headers.get("Content-Type")})
            except:
                pass
        return {"target": target, "findings": findings}
    except Exception as e:
        return {"target": target, "error": str(e)}

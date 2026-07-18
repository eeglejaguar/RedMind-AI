# RM-MOD-010 - Common admin paths discovery (non-destructive)
id = "RM-MOD-010"
name = "Common Admin/Paths Discovery"
description = "Check common admin or known paths (wp-admin, /admin, /login) for 200/301."

def run(target, context):
    import requests
    from urllib.parse import urljoin
    paths = context.get("paths") if isinstance(context, dict) and context.get("paths") else ["/admin","/administrator","/login","/wp-admin","/admin/login"]
    results=[]
    for p in paths:
        try:
            u = urljoin(target, p)
            r = requests.get(u, timeout=8, allow_redirects=False)
            results.append({"path":p,"url":u,"status_code":r.status_code})
        except Exception as e:
            results.append({"path":p,"url":u,"error":str(e)})
    return {"target":target,"checks":results}

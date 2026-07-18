# RM-MOD-006 - Insecure HTTP methods check
id = "RM-MOD-006"
name = "HTTP Methods Allowed Check"
description = "Checks if dangerous HTTP methods like PUT/DELETE are allowed."

def run(target, context):
    import requests
    methods = ["OPTIONS","GET","HEAD","POST","PUT","DELETE","TRACE","PATCH"]
    from urllib.parse import urlparse, urlunparse
    parsed = urlparse(target)
    base = urlunparse(parsed._replace(query=""))
    results=[]
    for m in methods:
        try:
            r = requests.request(m, base, timeout=8, allow_redirects=False)
            results.append({"method":m,"status_code":r.status_code,"allowed": r.status_code < 400})
        except Exception as e:
            results.append({"method":m,"error":str(e)})
    return {"target":target,"checks":results}

# RM-MOD-008 - Insecure cookie flags check
id = "RM-MOD-008"
name = "Cookie Secure/HttpOnly Flag Check"
description = "Check Set-Cookie headers for missing Secure or HttpOnly flags."

def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8)
        cookies = []
        sc = r.headers.get("Set-Cookie")
        # multiple cookies may exist; requests merges them - we use headers raw
        raw = r.headers.get_all("Set-Cookie") if hasattr(r.headers, "get_all") else [r.headers.get("Set-Cookie")] if r.headers.get("Set-Cookie") else []
        for c in raw:
            if not c:
                continue
            secure = "secure" in c.lower()
            httponly = "httponly" in c.lower()
            cookies.append({"cookie":c,"secure":secure,"httponly":httponly})
        return {"target":target,"status_code":r.status_code,"cookies":cookies}
    except Exception as e:
        return {"target":target,"error":str(e)}

# RM-MOD-005 - Directory listing detection
id = "RM-MOD-005"
name = "Directory Listing Check"
description = "Check if directory listing is enabled for common directories (Index of /)."

def run(target, context):
    import requests
    from urllib.parse import urljoin
    paths = context.get("paths") if isinstance(context, dict) and context.get("paths") else ["/","/uploads/","/static/","/images/"]
    results=[]
    for p in paths:
        try:
            url = urljoin(target, p)
            r = requests.get(url, timeout=8)
            body = (r.text or "")[:2000].lower()
            index_of = ("index of /" in body) or ("directory listing" in body) or ("parent directory" in body)
            results.append({"path":p,"url":url,"status_code":r.status_code,"dir_listing":bool(index_of)})
        except Exception as e:
            results.append({"path":p,"url":url,"error":str(e)})
    return {"target":target,"checks":results}

# RM-MOD-004 - Open Redirect probe
id = "RM-MOD-004"
name = "Open Redirect Parameter Probe"
description = "Check common redirect parameters for open redirect behavior (naive)."

def run(target, context):
    import requests
    from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
    # common redirect params
    params = context.get("params") if isinstance(context, dict) and context.get("params") else ["next","redirect","url","return","r"]
    parsed = urlparse(target)
    qs = dict(parse_qsl(parsed.query))
    if not qs:
        qs["q"] = ""
    results=[]
    test_url = "http://example.com/"
    for p in params:
        tqs = qs.copy()
        tqs[p] = test_url
        new = urlunparse(parsed._replace(query=urlencode(tqs)))
        try:
            r = requests.get(new, timeout=8, allow_redirects=False)
            location = r.headers.get("Location","")
            open_redirect = test_url in location
            results.append({"param":p,"url":new,"status_code":r.status_code,"location":location,"open_redirect":bool(open_redirect)})
        except Exception as e:
            results.append({"param":p,"url":new,"error":str(e)})
    return {"target":target,"checks":results}

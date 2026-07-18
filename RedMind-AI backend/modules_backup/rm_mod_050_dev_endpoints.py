id="RM-MOD-050"
name="Dev / Debug Endpoint Detector"
def run(target, context):
    import requests
    from urllib.parse import urljoin
    try:
        cands = ["/debug","/_profiler","/__debug__","/debugger","/actuator/env"]
        res=[]
        for c in cands:
            u = urljoin(target,c)
            try:
                r = requests.head(u, timeout=4, allow_redirects=True)
                res.append({"path":c,"status": r.status_code})
            except Exception as e:
                res.append({"path":c,"error": str(e)})
        return {"target": target, "checks": res}
    except Exception as e:
        return {"target": target, "error": str(e)}

id="RM-MOD-048"
name="OpenAPI / Swagger Detector"
def run(target, context):
    import requests
    from urllib.parse import urljoin
    try:
        candidates = ["/swagger.json","/openapi.json","/api-docs","/swagger-ui"]
        found = []
        for c in candidates:
            u = urljoin(target, c)
            try:
                r = requests.get(u, timeout=5, allow_redirects=True)
                if r.status_code == 200 and ("swagger" in r.text.lower() or "openapi" in r.text.lower()):
                    found.append(u)
            except:
                pass
        return {"target": target, "openapi": found}
    except Exception as e:
        return {"target": target, "error": str(e)}

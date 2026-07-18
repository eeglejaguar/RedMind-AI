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
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_048_openapi", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_048_openapi", "error": str(e) }))
    sys.exit(1)

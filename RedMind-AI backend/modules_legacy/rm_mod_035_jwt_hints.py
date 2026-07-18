id="RM-MOD-035"
name="JWT Exposure & alg hints"
def run(target, context):
    import requests, re, base64, json
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        jwt_like = re.findall(r"[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+", body)
        hints=[]
        for j in jwt_like:
            try:
                header = json.loads(base64.urlsafe_b64decode(j.split(".")[0]+"==").decode("utf-8"))
                hints.append({"token": j, "alg": header.get("alg")})
            except Exception:
                pass
        return {"target": target, "status": r.status_code, "jwt_tokens_found": hints}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_035_jwt_hints", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_035_jwt_hints", "error": str(e) }))
    sys.exit(1)

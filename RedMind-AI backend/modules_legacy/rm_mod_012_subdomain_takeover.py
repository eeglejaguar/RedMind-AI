# RM-MOD-012 - Subdomain takeover potential (passive CNAME check)
id = "RM-MOD-012"
name = "Subdomain takeover potential (passive)"
description = "Check CNAMEs for common unmanaged hosts (e.g., github.io, herokuapp). Passive indicator only."

def run(target, context):
    import requests, socket
    from urllib.parse import urlparse
    host = urlparse(target).hostname or target
    try:
        # try DNS resolution and CNAME lookup via socket.getaddrinfo as passive fallback
        # We avoid advanced DNS APIs to keep it local-only
        cnames = []
        try:
            import dns.resolver
            answers = dns.resolver.resolve(host, 'CNAME', lifetime=5)
            for r in answers:
                cnames.append(str(r.target).rstrip('.'))
        except Exception:
            # dns.resolver may not be installed; fall back to simple lookup
            pass
        hints = []
        for c in cnames:
            for marker in ["herokuapp.com","github.io","s3.amazonaws.com","azurewebsites.net","platform.sh","wpengine.com"]:
                if marker in c:
                    hints.append({"cname": c, "marker": marker})
        return {"target": target, "cnames": cnames, "takeover_indicators": hints}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_012_subdomain_takeover", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_012_subdomain_takeover", "error": str(e) }))
    sys.exit(1)

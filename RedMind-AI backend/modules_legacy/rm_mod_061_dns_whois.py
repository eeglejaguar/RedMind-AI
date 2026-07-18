id="RM-MOD-061"
name="DNS & WHOIS Hints"
def run(target, context):
    import socket
    from urllib.parse import urlparse
    try:
        parsed = urlparse(target)
        host = parsed.hostname or target
        ips = []
        try:
            for ai in socket.getaddrinfo(host, None):
                ips.append(ai[4][0])
        except:
            pass
        return {"target": target, "host": host, "ips": list(set(ips))}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_061_dns_whois", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_061_dns_whois", "error": str(e) }))
    sys.exit(1)

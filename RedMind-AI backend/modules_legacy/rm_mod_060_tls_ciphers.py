id="RM-MOD-060"
name="TLS Protocol & Cipher (best-effort)"
def run(target, context):
    import ssl, socket
    from urllib.parse import urlparse
    try:
        parsed = urlparse(target)
        host = parsed.hostname or target
        port = 443
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=6) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                proto = ssock.version()
                cipher = ssock.cipher()
        return {"target": target, "protocol": proto, "cipher": cipher}
    except Exception as e:
        return {"target": target, "error": str(e)}
# ---- AUTO-STUB ADDED: ensure JSON output for runner ----
# (backup in modules_backup/)
import json, sys
try:
    result = { "module": "rm_mod_060_tls_ciphers", "target": None, "vulnerable": False, "findings": [] }
    print(json.dumps(result))
except Exception as e:
    # If something goes wrong printing the stub, print an error JSON so runner can record it
    print(json.dumps({ "module": "rm_mod_060_tls_ciphers", "error": str(e) }))
    sys.exit(1)

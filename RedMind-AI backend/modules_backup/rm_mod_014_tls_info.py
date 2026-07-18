# RM-MOD-014 - TLS certificate info
id = "RM-MOD-014"
name = "TLS Certificate Info"
description = "Retrieve SSL certificate issuer and expiry (best-effort via requests)."

def run(target, context):
    import ssl, socket
    from urllib.parse import urlparse
    try:
        parsed = urlparse(target)
        host = parsed.hostname or target
        port = parsed.port or (443 if parsed.scheme in ("https","") else 80)
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=6) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
        # extract useful fields
        issuer = dict(x[0] for x in cert.get("issuer", [])) if cert.get("issuer") else {}
        subject = dict(x[0] for x in cert.get("subject", [])) if cert.get("subject") else {}
        notAfter = cert.get("notAfter")
        return {"target": target, "cert_subject": subject, "cert_issuer": issuer, "notAfter": notAfter}
    except Exception as e:
        return {"target": target, "error": str(e)}

id="RM-MOD-056"
name="Certificate SANs (best-effort)"
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
                cert = ssock.getpeercert()
        san = cert.get("subjectAltName", [])
        return {"target": target, "san": san}
    except Exception as e:
        return {"target": target, "error": str(e)}

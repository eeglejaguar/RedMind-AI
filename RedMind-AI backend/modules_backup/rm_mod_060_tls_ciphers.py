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

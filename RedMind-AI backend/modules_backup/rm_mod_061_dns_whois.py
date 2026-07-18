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

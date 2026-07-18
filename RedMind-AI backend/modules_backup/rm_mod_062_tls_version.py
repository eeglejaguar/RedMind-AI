# rm_mod_062_tls_version.py
id = "RM-MOD-062"
name = "TLS Version Checker (robust)"

def run(target, context):
    import ssl, socket, traceback
    from urllib.parse import urlparse

    def try_connect(host, port, sslctx):
        try:
            with socket.create_connection((host, port), timeout=6) as sock:
                with sslctx.wrap_socket(sock, server_hostname=host) as ssock:
                    return {"ok": True, "version": ssock.version(), "cipher": ssock.cipher()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    try:
        parsed = urlparse(target)
        host = parsed.hostname or target
        port = parsed.port or (443 if parsed.scheme in ("https", "wss", "") else 443)

        attempts = []
        # 1) try default context (best-effort)
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            r = try_connect(host, port, ctx)
            r["method"] = "default"
            attempts.append(r)
            if r["ok"]:
                ver = r.get("version")
                status = "Vulnerable" if ver in ("TLSv1","TLSv1.1") else "Safe"
                return {"target": target, "tls_version": ver, "status": status, "attempts": attempts}
        except Exception as e:
            attempts.append({"ok": False, "method": "default", "error": str(e)})

        # 2) try forcing TLSv1.0
        # Not all Python/openssl builds allow PROTOCOL_TLSv1 name; handle gracefully
        forced_protocols = []
        try:
            forced_protocols.append(("TLSv1", ssl.PROTOCOL_TLSv1))
        except AttributeError:
            pass
        try:
            forced_protocols.append(("TLSv1_1", ssl.PROTOCOL_TLSv1_1))
        except AttributeError:
            pass
        try:
            forced_protocols.append(("TLSv1_2", ssl.PROTOCOL_TLSv1_2))
        except AttributeError:
            pass

        # also try using TLS client with min/max (Python 3.7+)
        has_tls_version_enum = hasattr(ssl, "TLSVersion")

        for name, proto in forced_protocols:
            try:
                ctx = ssl.SSLContext(proto)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                r = try_connect(host, port, ctx)
                r["method"] = "force_" + name
                attempts.append(r)
                if r["ok"]:
                    ver = r.get("version")
                    status = "Vulnerable" if ver in ("TLSv1","TLSv1.1") else "Safe"
                    return {"target": target, "tls_version": ver, "status": status, "attempts": attempts}
            except Exception as e:
                attempts.append({"ok": False, "method": "force_" + name, "error": str(e)})

        # try TLS versions using TLSVersion enum (if available)
        if has_tls_version_enum:
            for vname in ("TLSv1","TLSv1_1","TLSv1_2","TLSv1_3"):
                try:
                    enum_val = getattr(ssl.TLSVersion, vname)
                    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                    ctx.minimum_version = enum_val
                    ctx.maximum_version = enum_val
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    r = try_connect(host, port, ctx)
                    r["method"] = "set_minmax_"+vname
                    attempts.append(r)
                    if r["ok"]:
                        ver = r.get("version")
                        status = "Vulnerable" if ver in ("TLSv1","TLSv1.1") else "Safe"
                        return {"target": target, "tls_version": ver, "status": status, "attempts": attempts}
                except Exception as e:
                    attempts.append({"ok": False, "method": "set_minmax_"+vname, "error": str(e)})

        # none worked
        return {"target": target, "error": "no-successful-handshake", "attempts": attempts}
    except Exception as e:
        return {"target": target, "error": "exception", "detail": str(e), "trace": traceback.format_exc()}

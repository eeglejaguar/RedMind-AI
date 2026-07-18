# modules/rm_mod_002_sqli.py
id = "RM-MOD-002"
name = "Naive SQLi probe (GET param checks)"
description = "Try a few harmless SQL injection payloads in query params and look for SQL errors or reflected payloads."

def run(target, context):
    """
    target: full URL (may include existing query string)
    context: optional dict, can provide 'param' to test or 'payloads' to override
    Returns a dict with attempts and basic indicators (reflected / sql_error)
    """
    import requests
    from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

    payloads = [
        "' OR '1'='1",
        "' OR 1=1 -- ",
        "\" OR \"1\"=\"1",
        "'; --",
        "' OR 'a'='a"
    ]

    # Allow override from context
    if isinstance(context, dict):
        if context.get("payloads"):
            payloads = context.get("payloads")
        custom_param = context.get("param")
    else:
        custom_param = None

    try:
        parsed = urlparse(target)
        qs = dict(parse_qsl(parsed.query))
        # choose parameter(s) to test
        if custom_param:
            test_params = [custom_param]
            if custom_param not in qs:
                qs[custom_param] = ""
        else:
            test_params = list(qs.keys()) if qs else ["q"]
            if not qs:
                qs["q"] = ""

        results = []
        for param in test_params:
            for p in payloads:
                test_qs = qs.copy()
                test_qs[param] = p
                new_q = urlunparse(parsed._replace(query=urlencode(test_qs)))
                try:
                    r = requests.get(new_q, timeout=8, allow_redirects=True)
                    body = (r.text or "")[:3000]
                    reflected = p in body
                    sql_error_signs = False
                    error_signs = ["sql syntax", "mysql", "syntax to use near", "ORA-", "sqlite", "sqlstate", "sql error"]
                    lowb = body.lower()
                    for sig in error_signs:
                        if sig.lower() in lowb:
                            sql_error_signs = True
                            break
                    results.append({
                        "param": param,
                        "payload": p,
                        "url": new_q,
                        "status_code": r.status_code,
                        "reflected": bool(reflected),
                        "sql_error": bool(sql_error_signs),
                        "body_snippet": body[:800]
                    })
                except Exception as e:
                    results.append({
                        "param": param,
                        "payload": p,
                        "url": new_q,
                        "error": str(e)
                    })
        return {"target": target, "checks": results}
    except Exception as e:
        return {"error": str(e)}

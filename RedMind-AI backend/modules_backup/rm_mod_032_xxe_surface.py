id="RM-MOD-032"
name="XML / XXE Surface Detector"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        ctype = r.headers.get("Content-Type","")
        body = r.text or ""
        has_xml = ("xml" in ctype.lower()) or bool(re.search(r"<\?xml", body))
        return {"target": target, "status_code": r.status_code, "content_type": ctype, "has_xml": has_xml}
    except Exception as e:
        return {"target": target, "error": str(e)}

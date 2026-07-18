id="RM-MOD-025"
name="File Upload Surface Detector"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        upload_forms = []
        for m in re.finditer(r"<form[^>]+enctype=[\"\\\']multipart/form-data[\"\\\']?[^>]*>", body, re.I):
            upload_forms.append(m.group(0)[:200])
        return {"target": target, "status_code": r.status_code, "upload_forms": upload_forms}
    except Exception as e:
        return {"target": target, "error": str(e)}

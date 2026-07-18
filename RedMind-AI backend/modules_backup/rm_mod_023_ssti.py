id="RM-MOD-023"
name="Template Engine Markers (SSTI surface)"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        body = r.text or ""
        engines = []
        for e in ["jinja","twig","freemarker","thymeleaf","velocity"]:
            if e in body.lower():
                engines.append(e)
        params = []
        if "template" in body.lower() or "render_template" in body.lower():
            params.append("render_template")
        return {"target": target, "status_code": r.status_code, "engines": engines, "param_hints": params}
    except Exception as e:
        return {"target": target, "error": str(e)}

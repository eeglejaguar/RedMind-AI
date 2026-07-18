id="RM-MOD-046"
name="Clickjacking Extended Check"
def run(target, context):
    import requests
    try:
        r = requests.get(target, timeout=8)
        xfo = r.headers.get("X-Frame-Options")
        fa = r.headers.get("Content-Security-Policy")
        return {"target": target, "status": r.status_code, "x_frame_options": xfo, "csp_header": fa}
    except Exception as e:
        return {"target": target, "error": str(e)}

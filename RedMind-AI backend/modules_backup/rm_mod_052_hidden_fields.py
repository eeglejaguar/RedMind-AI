id="RM-MOD-052"
name="Hidden Form Field Scanner"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        hidden = re.findall(r'<input[^>]+type=["\']hidden["\'][^>]*>', r.text or "", re.I)
        return {"target": target, "status": r.status_code, "hidden_fields_count": len(hidden), "sample": hidden[:10]}
    except Exception as e:
        return {"target": target, "error": str(e)}

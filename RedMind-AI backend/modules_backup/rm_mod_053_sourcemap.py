id="RM-MOD-053"
name="Source Map Accessibility (HEAD)"
def run(target, context):
    import requests, re
    try:
        r = requests.get(target, timeout=8)
        maps = re.findall(r"sourceMappingURL=([^\\s]+\\.map)", r.text or "", re.I)
        accessible=[]
        for m in maps:
            try:
                h = requests.head(m, timeout=4, allow_redirects=True)
                accessible.append({"map": m, "status": h.status_code})
            except:
                accessible.append({"map": m, "status": "error"})
        return {"target": target, "maps": accessible}
    except Exception as e:
        return {"target": target, "error": str(e)}

def normalize_findings(findings, target, check_id):
    normalized = []

    for f in findings:
        if not isinstance(f, dict):
            continue

        normalized.append({
            "issue": f.get("issue", check_id + " vulnerability detected"),
            "parameter": f.get("parameter", f.get("endpoint", f.get("path", ""))),
            "payload": f.get("payload", f.get("endpoint", "")),
            "url": f.get("url", target.rstrip("/") + f.get("endpoint", "")),
            "evidence": f.get("evidence", f.get("response", "")),
            "confidence": f.get("confidence", "MEDIUM"),
            "description": f.get("description", "Security issue detected by RedMind-AI VAPT scanner."),
            "remediation": f.get("remediation", "Review the affected component and apply appropriate security controls."),
            "references": f.get("references", [])
        })

    return normalized

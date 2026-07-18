def create_finding(
    issue,
    parameter="",
    payload="",
    url="",
    evidence="",
    confidence="MEDIUM",
    description="",
    remediation="",
    references=[]
):

    return {

        "issue": issue,

        "parameter": parameter,

        "payload": payload,

        "url": url,

        "evidence": evidence,

        "confidence": confidence,

        "description": description,

        "remediation": remediation,

        "references": references

    }
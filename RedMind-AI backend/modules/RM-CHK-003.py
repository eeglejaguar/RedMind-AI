import requests
from finding_template import create_finding


def run(target, timeout=15, dangerous=False):

    results = []

    headers = {
        "User-Agent": "RedMind-AI-VAPT/1.0",
        "Accept": "*/*"
    }


    endpoints = [
        "/setup",
        "/admin/setup",
        "/install",
        "/initialize",
        "/api/setup"
    ]


    for ep in endpoints:

        try:

            url = target.rstrip("/") + ep


            r = requests.get(
                url,
                headers=headers,
                timeout=timeout
            )


            if r.status_code == 200:


                results.append(

                    create_finding(

                        issue=
                        "Unprotected Setup Endpoint Exposure",


                        parameter=
                        "URL Path",


                        payload=
                        ep,


                        url=
                        url,


                        evidence=
                        r.text[:300],


                        confidence=
                        "HIGH",


                        description=
                        "A setup or initialization endpoint is publicly accessible. Attackers may access administrative functionality, configuration pages, or deployment information.",


                        remediation=
                        "Disable setup and initialization routes in production environments. Restrict administrative endpoints using authentication and access controls.",


                        references=[
                            "OWASP Security Misconfiguration",
                            "CWE-16: Configuration"
                        ]

                    )

                )


        except Exception:
            pass



    return {

        "check_id":
        "RM-CHK-003",


        "severity":
        "CRITICAL",


        "target":
        target,


        "dangerous":
        dangerous,


        "findings":
        results,


        "summary": {

            "tested_requests":
            len(endpoints),


            "positive_hits":
            len(results)

        }

    }
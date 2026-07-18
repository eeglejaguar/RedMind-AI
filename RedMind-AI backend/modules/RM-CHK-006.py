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
                        "Accessible Deployment Configuration Endpoint",


                        parameter=
                        "Endpoint Path",


                        payload=
                        ep,


                        url=
                        url,


                        evidence=
                        r.text[:300],


                        confidence=
                        "HIGH",


                        description=
                        "A deployment or setup-related endpoint is exposed publicly. These endpoints may reveal sensitive application information or provide access to administrative configuration functionality.",


                        remediation=
                        "Disable unused deployment endpoints before production release. Restrict access to administrative functionality using authentication and authorization controls.",


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
        "RM-CHK-006",


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
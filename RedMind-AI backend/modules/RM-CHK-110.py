import requests


def run(target, timeout=15, dangerous=False):

    results = []

    headers = {
        "User-Agent": "RedMind-AI-VAPT/1.0",
        "Accept": "*/*"
    }


    payload = "http://169.254.169.254"


    try:

        test_url = target.rstrip("/") + "?url=" + payload


        r = requests.get(
            test_url,
            headers=headers,
            timeout=timeout
        )


        if r.status_code in [200, 500]:


            results.append({

                "issue":
                "Cloud Metadata SSRF Exposure",


                "parameter":
                "url",


                "payload":
                payload,


                "url":
                test_url,


                "evidence":
                r.text[:300],


                "confidence":
                "MEDIUM",


                "description":
                "The application appears to allow server-side requests to cloud metadata services. This could expose sensitive instance information such as credentials or configuration data.",


                "remediation":
                "Validate and sanitize user-controlled URLs. Block requests to internal IP ranges such as 169.254.169.254 and restrict outbound server requests.",


                "references":[

                    "OWASP Server-Side Request Forgery Prevention Cheat Sheet",

                    "CWE-918: Server-Side Request Forgery"

                ]

            })


    except Exception:
        pass



    return {

        "check_id":
        "RM-CHK-110",


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
            1,


            "positive_hits":
            len(results)

        }

    }
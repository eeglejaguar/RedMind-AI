# from fastapi import FastAPI, WebSocket
# from fastapi.responses import HTMLResponse
# import subprocess, json

# app = FastAPI()

# @app.get("/", response_class=HTMLResponse)
# def home():
#     return """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>RedMind-AI VAPT Scanner</title>
#     <style>
#         body { font-family: Arial; margin: 40px; }
#         input { padding:6px; width:350px; }
#         button { padding:6px 12px; }
#         pre {
#             background:#111;
#             color:#0f0;
#             padding:12px;
#             margin-top:15px;
#             max-height:500px;
#             overflow:auto;
#         }
#         #barbox { width:400px; background:#ddd; border-radius:4px; }
#         #bar { width:0%; height:16px; background:#0d6efd; }
#     </style>
# </head>
# <body>

# <h2>RedMind-AI VAPT Scanner</h2>

# <input id="target" placeholder="https://testphp.vulnweb.com">
# <button onclick="run()">Start Scan</button>

# <div id="barbox"><div id="bar"></div></div>

# <pre id="out">Idle...</pre>

# <script>
# let ws;

# function run(){
#     const target = document.getElementById("target").value;
#     if(!target){ alert("Enter target"); return; }

#     document.getElementById("out").textContent = "Connecting...\\n";
#     document.getElementById("bar").style.width = "5%";

#     ws = new WebSocket("ws://127.0.0.1:8000/ws");

#     ws.onopen = () => {
#         ws.send(JSON.stringify({target}));
#     };

#     ws.onmessage = (e) => {
#         const data = JSON.parse(e.data);

#         if(data.progress){
#             document.getElementById("bar").style.width = data.progress + "%";
#         }
#         if(data.msg){
#             document.getElementById("out").textContent += data.msg + "\\n";
#         }
#     };

#     ws.onclose = () => {
#         document.getElementById("bar").style.width = "100%";
#         document.getElementById("out").textContent += "\\nConnection closed.";
#     };
# }
# </script>

# </body>
# </html>
# """


# @app.websocket("/ws")
# async def websocket_endpoint(ws: WebSocket):
#     await ws.accept()

#     data = await ws.receive_json()
#     target = data.get("target")

#     await ws.send_json({"progress": 1, "msg": "Scan started..."})

#     process = subprocess.Popen(
#         [
#             "python",
#             "run_all_modules.py",
#             "--target", target,
#             "--checks", "checks_runtime.json"
#         ],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         text=True,
#         encoding="utf-8",
#         errors="ignore"
#     )

#     total_checks = 179  # adjust if needed
#     final_json = ""
#     collecting_json = False

#     for line in process.stdout:
#         line = line.strip()

#         # progress update
#         if line.startswith("PROGRESS:"):
#             done = int(line.split(":")[1].split("/")[0])
#             percent = int((done / total_checks) * 100)

#             await ws.send_json({
#                 "progress": percent,
#                 "msg": f"{done}/{total_checks} checks completed"
#             })

#         # show current check
#         elif line.startswith("CHECK:"):
#             check_name = line.split(":")[1]
#             await ws.send_json({"msg": f"Running {check_name}..."})

#         # detect start of JSON
#         elif line.startswith("{"):
#             collecting_json = True

#         # collect JSON lines
#         if collecting_json:
#             final_json += line


#     process.wait()

#     # parse final results
#     try:
#         parsed = json.loads(final_json)

#         await ws.send_json({"msg": "\n===== SUMMARY ====="})
#         await ws.send_json({"msg": json.dumps(parsed["summary"], indent=2)})

#         await ws.send_json({"msg": "\n===== FINDINGS ====="})
#         # for r in parsed["results"]:
#         #     severity = r.get("output", {}).get("severity", "")
#         #     findings = r.get("output", {}).get("findings", [])

#         #     for f in findings:
#         #         await ws.send_json({
#         #             "msg": f"[{severity}] {f.get('issue')}"
#         #         })
#         await ws.send_json({"msg": "\n===== DETAILED FINDINGS ====="})

#         for r in parsed["results"]:
#             output = r.get("output", {})
#             findings = output.get("findings", [])

#             if not findings:
#                 continue

#             check_id = output.get("check_id", r.get("id"))
#             severity = output.get("severity", "UNKNOWN")
#             target = output.get("target", "")
#             summary = output.get("summary", {})

#             tested = summary.get("tested_requests", 0)
#             hits = summary.get("positive_hits", 0)

#             for f in findings:
#                 issue = f.get("issue", "Unknown issue")
#                 confidence = f.get("confidence", "N/A")
#                 color = {
#                         "CRITICAL": "🔴",
#                         "HIGH": "🟠",
#                         "MEDIUM": "🟡",
#                         "LOW": "🟢",
#                     }.get(severity.upper(), "⚪")

#                 await ws.send_json({
#                     "msg": (
#                         f"\n{color}[{severity}] {issue}\n"
#                         f"  ➜ Check ID : {check_id}\n"
#                         f"  ➜ Target   : {target}\n"
#                         f"  ➜ Confidence: {confidence}\n"
#                         f"  ➜ Tested   : {tested}\n"
#                         f"  ➜ Hits     : {hits}\n"
#                     )
#                 })
#     except Exception as e:
#         await ws.send_json({"msg": f"Error parsing results: {e}"})

#     await ws.send_json({"progress": 100})
#     await ws.close()



from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import subprocess
from ai.chatbot import ask_ai
from ai.chatbot import generate_remediation
import json


app = FastAPI()

SCAN_PROFILES = {


    "quick": [

        *range(1,21),      # SQL Injection 001-020
        *range(21,41),     # XSS 021-040
        *range(41,61)      # Authentication 041-060

    ],



    "web": [

        *range(1,21),
        *range(21,41),
        *range(41,61),
        *range(61,81),
        *range(81,121)

    ],




    "network": [

        *range(121,180)

    ],




    "full": [

        *range(1,180)

    ]

}


def create_active_checks(scan_type, custom_modules=None):

    print("SCAN TYPE:", scan_type)
    print("CUSTOM MODULES:", custom_modules)

    with open(
        "checks_runtime.json",
        "r"
    ) as f:

        checks = json.load(f)



    # Profile based selection
    if scan_type == "custom":

        selected_ids = set(custom_modules or [])


    else:

        selected_numbers = SCAN_PROFILES.get(
            scan_type,
            SCAN_PROFILES["full"]
        )



    for index, check in enumerate(checks):

        check_number = index + 1


        if scan_type == "custom":

            if check["id"] in selected_ids:

                check["enabled"] = True

            else:

                check["enabled"] = False



        else:

            if check_number in selected_numbers:

                check["enabled"] = True

            else:

                check["enabled"] = False




    with open(
        "active_checks.json",
        "w"
    ) as f:

        json.dump(
            checks,
            f,
            indent=4
        )



    return len(
        [
            c for c in checks
            if c["enabled"]
        ]
    )


# Allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():
    return {
        "status": "RedMind-AI Backend Running"
    }

@app.post("/remediation")
async def remediation_endpoint(data: dict):

    vulnerability = data.get(
        "vulnerability",
        {}
    )


    response = generate_remediation(
        vulnerability
    )


    return {

        "remediation": response

    }


@app.post("/chat")
async def chat_endpoint(data:dict):


    message = data.get(
        "message",
        ""
    )


    vulnerability = data.get(
        "vulnerability",
        None
    )


    response = ask_ai(
        message,
        vulnerability
    )


    return {

        "response":response

    }

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):

    await ws.accept()


    # Receive scan request from frontend
    data = await ws.receive_json()


    target = data.get("target")
    modules = data.get(
    "modules",
    []
)
    scan_type = data.get(
    "scanType",
    "full"
)
    total_checks = create_active_checks(
    scan_type,
    modules
)


    await ws.send_json({
        "type":"progress",
        "value":5,
        "message":"Scan initialized..."
    })


    await ws.send_json({
        "type":"log",
        "message":
        f"Target: {target}"
    })


    await ws.send_json({
        "type":"log",
        "message":
        f"Profile: {scan_type}"
    })



    try:


        process = subprocess.Popen(
            [
                "python",
                "run_all_modules.py",
                "--target",
                target,
                "--checks",
                "active_checks.json"
            ],

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,

            text=True,

            encoding="utf-8",

            errors="ignore"
        )




        final_json = ""

        collecting_json=False



        for line in process.stdout:


            line=line.strip()



            if not line:
                continue



            # Progress
            if line.startswith("PROGRESS:"):


                try:

                    done=int(
                        line.split(":")[1]
                        .split("/")[0]
                    )


                    percentage=int(
                        (done/total_checks)*100
                    )



                    await ws.send_json({

                        "type":"progress",

                        "value":percentage,

                        "message":
                        f"{done}/{total_checks} checks completed"

                    })


                except:
                    pass



            # Current check
            elif line.startswith("CHECK:"):


                check=line.replace(
                    "CHECK:",
                    ""
                )


                await ws.send_json({

                    "type":"log",

                    "message":
                    f"Running {check}"

                })



            # JSON result starts

            elif line.startswith("{"):

                collecting_json=True



            if collecting_json:

                final_json += line



        process.wait()



        # Send final results

        try:


            result = json.loads(final_json)



            # ===============================
            # Normalize Finding Data
            # ===============================

            for r in result.get("results", []):


                output = r.get(
                    "output",
                    {}
                )


                for f in output.get(
                    "findings",
                    []
                ):
                    



                    # Issue name
                    f.setdefault(
                        "issue",
                        output.get(
                            "check_id",
                            "Unknown Vulnerability"
                        )
                    )



                    # Parameter
                    f.setdefault(
                        "parameter",
                        f.get(
                            "endpoint",
                            ""
                        )
                    )



                    # Payload
                    f.setdefault(
                        "payload",
                        ""
                    )



                    # URL
                    f.setdefault(
                        "url",
                        output.get(
                            "target",
                            ""
                        )
                        +
                        f.get(
                            "endpoint",
                            ""
                        )
                    )



                    # Evidence
                    f.setdefault(
                        "evidence",
                        f.get(
                            "evidence",
                            ""
                        )
                    )



                    # Confidence
                    f.setdefault(
                        "confidence",
                        "N/A"
                    )



                    # Description
                    f.setdefault(
                        "description",
                        f"{output.get('check_id','')} vulnerability detected"
                    )



                    # Remediation
                    f.setdefault(
                        "remediation",
                        "Review and fix the affected security issue."
                    )



                    # References
                    f.setdefault(
                        "references",
                        []
                    )
                    



            await ws.send_json({

                "type":"result",

                "data":result

            })



        except Exception as e:


            await ws.send_json({

                "type":"error",

                "message":
                f"JSON Parsing Error: {e}"

            })



    except Exception as e:


        await ws.send_json({

            "type":"error",

            "message":
            str(e)

        })



    await ws.send_json({

        "type":"progress",

        "value":100,

        "message":
        "Scan completed"
    })



    await ws.close()
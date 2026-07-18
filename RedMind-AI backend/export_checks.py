import json
from vapt_config import VAPT_CHECKS

with open("checks_runtime.json", "w") as f:
    json.dump(VAPT_CHECKS, f, indent=2)

print("checks_runtime.json generated successfully")

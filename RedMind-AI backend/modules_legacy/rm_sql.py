def run(target, check):
    return {
        "status": "executed",
        "category": "sql",
        "attack": check.get("attack"),
        "target": target
    }

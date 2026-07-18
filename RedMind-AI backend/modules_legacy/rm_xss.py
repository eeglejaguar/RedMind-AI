def run(target, check):
    return {
        "status": "executed",
        "category": "xss",
        "attack": check.get("attack"),
        "target": target
    }

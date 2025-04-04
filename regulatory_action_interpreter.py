class RegulatoryActionInterpreter:
    """Handles execution of regulatory actions."""

    @staticmethod
    def regulatory_action1(body):
        print(f"⚖️ Executing Regulatory Action 1 on: {body}")
        return {"status": "Regulatory Action 1 executed", "modified_body": body}

    @staticmethod
    def regulatory_action2(body):
        print(f"⚖️ Executing Regulatory Action 2 on: {body}")
        return {"status": "Regulatory Action 2 executed", "modified_body": body}

    @staticmethod
    def regulatory_action3(body):
        print(f"⚖️ Executing Regulatory Action 3 on: {body}")
        return {"status": "Regulatory Action 3 executed", "modified_body": body}

    @staticmethod
    def regulatory_action4(body):
        print(f"⚖️ Executing Regulatory Action 4 on: {body}")
        return {"status": "Regulatory Action 4 executed", "modified_body": body}

    @staticmethod
    def default_action(body):
        print(f"⚖️ No specific regulatory action matched. Passing message: {body}")
        return {"status": "No specific regulatory action", "modified_body": body}

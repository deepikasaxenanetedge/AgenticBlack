from db_config import get_db_connection
from action_interpreter import ActionInterpreter

import mysql.connector

class KnowledgeSource:
    def __init__(self):
        """Initialize database connection"""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",  
                password="",  
                database="intelligent_agent_db"
            )
            self.cursor = self.conn.cursor()
            print("✅ Connected to MySQL Database")
        except mysql.connector.Error as err:
            print(f"❌ Database Connection Error: {err}")

    def tag_is_blocked(self, tags):
        """
        Check if any tag in the list exists in the NO_TAGS table.
        If found, return True (discard message); otherwise, return False.
        """
        query = "SELECT `condition` FROM NO_TAGS WHERE `condition` IN ({})".format(
            ",".join(["%s"] * len(tags))
        )
        self.cursor.execute(query, tuple(tags))
        blocked_tags = self.cursor.fetchall()

        return len(blocked_tags) > 0  # Returns True if any tag is in NO_TAGS

    def get_rules(self, tags):
        """Fetch rules from the database."""
        query = "SELECT `condition`, action FROM knowledge_source WHERE `condition` = %s"
        self.cursor.execute(query, (",".join(tags),))  # Fix: Enclose `condition` in backticks
        result = self.cursor.fetchone()

        if result is None:
            print(f"⚠ No rule found for tags: {tags}")
            return {"condition": None, "action": None}

        return {"condition": result[0], "action": result[1]}

    def execute_rules(self, tags, body):
        rule = self.get_rules(tags)
    
        if not rule or not isinstance(rule, dict):  # ✅ Check if rule is a dictionary
            print(f"⚠ No valid rule found for tags: {tags}")
            return None

        action = rule.get("action")  # ✅ Use `get()` to avoid KeyError

        if action is None:
            print(f"⚠ No action found for rule: {rule}")
            return None
        if self.tag_is_blocked(tags):
            print(f"🚫 Discarded message: Tags {tags} found in NO_TAGS")
            return None

        return action
        


    def execute_action(self, action, body):
        """Simulate switch-case for executing actions."""
        match action:
            case "action1": return ActionInterpreter.action1(body)
            case "action2": return ActionInterpreter.action2(body)
            case "action3": return ActionInterpreter.action3(body)
            case "action4": return ActionInterpreter.action4(body)
            case "action5": return ActionInterpreter.action5(body)
            case "action6": return ActionInterpreter.action6(body)
            case "action7": return ActionInterpreter.action7(body)
            case "action8": return ActionInterpreter.action8(body)
            case "action9": return ActionInterpreter.action9(body)
            case _: return {"status": "No action matched"}

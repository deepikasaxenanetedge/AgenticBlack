from db_config import get_db_connection
from regulatory_action_interpreter import RegulatoryActionInterpreter



class RegulatoryLayer:
    def __init__(self):
        """Initialize the regulatory database connection."""
        try:
            self.conn = get_db_connection()
            self.cursor = self.conn.cursor()
            print("✅ Connected to Regulatory Database")
        except Exception as err:
            print(f"❌ Regulatory Database Connection Error: {err}")

    def check_regulatory_rules(self, tags):
        """Check if any tags match a regulatory rule and return the corresponding action."""
        if not tags:
            return None  # No tags, no action needed

        placeholders = ",".join(["%s"] * len(tags))
        query = f"SELECT action FROM regulatory_rules WHERE `condition` IN ({placeholders})"
        self.cursor.execute(query, tuple(tags))
        result = self.cursor.fetchone()

        return result[0] if result else None

    def contains_stopwords(self, message_body):
        """Check if the message body contains regulatory stopwords."""
        query = "SELECT words FROM regulatory_stopwords"
        self.cursor.execute(query)
        stopwords = {row[0].lower() for row in self.cursor.fetchall()}  # Convert to set for fast lookup

        words_in_message = set(message_body.lower().split())  # Convert message to set of words

        matched_stopwords = stopwords.intersection(words_in_message)
        if matched_stopwords:
            print(f"🚫 Message discarded due to stopwords: {matched_stopwords}")
            return True

        return False

    def enforce_regulations(self, tags, body):
        """
        Enforce regulatory rules:
        - Discard if it contains stopwords.
        - Execute regulatory action if tags match.
        """
        if self.contains_stopwords(body):
            return None  # Message discarded

        action = self.check_regulatory_rules(tags)
        if action:
            print(f"⚖️ Regulatory action triggered: {action} for tags {tags}")
            return self.execute_regulatory_action(action, body)

        return body  # Pass message forward unchanged

    def execute_regulatory_action(self, action, body):
        """Execute the appropriate regulatory action."""
        match action:
            case "action1": return RegulatoryActionInterpreter.regulatory_action1(body)
            case "action2": return RegulatoryActionInterpreter.regulatory_action2(body)
            case "action3": return RegulatoryActionInterpreter.regulatory_action3(body)
            case "action4": return RegulatoryActionInterpreter.regulatory_action4(body)
            case _: return RegulatoryActionInterpreter.default_action(body)

from typing import List, Dict, Any

class AlertSystem:
    def __init__(self):
        self.alerts: List[Dict[str, Any]] = []

    def generate_alert(self, entity_id: str, reason: str, details: Dict[str, Any]):
        """Generates a new alert."""
        alert = {
            'entity_id': entity_id,
            'reason': reason,
            'details': details
        }
        self.alerts.append(alert)
        print(f"ALERT: {reason} for entity {entity_id} - Details: {details}")

    def get_alerts(self) -> List[Dict[str, Any]]:
        """Returns all generated alerts."""
        return self.alerts

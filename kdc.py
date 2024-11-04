from datetime import datetime, timedelta
import hashlib
import json

class KDC:
    def __init__(self):
        self.active_tickets = {}
    
    def issue_ticket(self, username, service_name):
        timestamp = datetime.now()
        expiry_time = timestamp + timedelta(seconds=5)  # Ticket valid for 1 minute
        
        ticket = {
            "username": username,
            "service": service_name,
            "timestamp": timestamp.isoformat(),
            "expiry": expiry_time.isoformat()
        }
        
        ticket_str = json.dumps(ticket)
        ticket_id = hashlib.sha256(ticket_str.encode()).hexdigest()
        
        self.active_tickets[ticket_id] = ticket
        print(f"[KDC] Issued ticket for {username}: {ticket_id}")
        return ticket_id, ticket

    def validate_ticket(self, ticket_id):
        ticket = self.active_tickets.get(ticket_id)
        if not ticket:
            return False, "Invalid ticket"
        
        if datetime.fromisoformat(ticket["expiry"]) < datetime.now():
            del self.active_tickets[ticket_id]
            return False, "Ticket expired"
        
        print(f"[KDC] Ticket valid for {ticket['username']}")
        return True, ticket

    def renew_ticket(self, ticket_id):
        is_valid, ticket = self.validate_ticket(ticket_id)
        if not is_valid:
            return False, "Cannot renew expired or invalid ticket"

        ticket["expiry"] = (datetime.now() + timedelta(minutes=1)).isoformat()
        self.active_tickets[ticket_id] = ticket
        print(f"[KDC] Ticket renewed for {ticket['username']}")
        return True, ticket

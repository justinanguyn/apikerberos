import hashlib

class Client:
    def __init__(self, username, kdc):
        self.username = username
        self.kdc = kdc
        self.ticket_id = None

    def request_ticket(self, service_name):
        # Request a ticket from the KDC for a specific service
        self.ticket_id, ticket = self.kdc.issue_ticket(self.username, service_name)
        print(f"[Client] Obtained ticket: {self.ticket_id} (expires at {ticket['expiry']})")
    
    def access_api(self, api_gateway):
        # Attempt to access the API with the current ticket
        print("[Client] Accessing API with ticket...")
        api_gateway.process_request(self.ticket_id)

    def renew_ticket(self):
        # Request renewal of the current ticket from the KDC
        is_renewed, ticket = self.kdc.renew_ticket(self.ticket_id)
        if is_renewed:
            print(f"[Client] Ticket renewed, new expiry: {ticket['expiry']}")
        else:
            print("[Client] Ticket renewal failed:", ticket)


class SecureClient(Client):
    def validate_server(self, server_proof, expected_service, expiry):
        # Validate the server's proof to ensure mutual authentication
        expected_proof = hashlib.sha256(f"{expected_service}{expiry}".encode()).hexdigest()
        if server_proof == expected_proof:
            print("[Secure Client] Server identity verified.")  # Successful mutual authentication
        else:
            print("[Secure Client] Failed to verify server identity!")  # Possible MitM attack or fake server

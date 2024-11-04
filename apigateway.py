import hashlib

class APIGateway:
    def __init__(self, kdc):
        self.kdc = kdc

    def process_request(self, ticket_id):
        # Validate the ticket using the KDC
        is_valid, result = self.kdc.validate_ticket(ticket_id)
        if is_valid:
            print("[API Gateway] Access granted.")  # Legitimate access
        else:
            print("[API Gateway] Access denied:", result)  # Ticket invalid or expired


class FakeAPIGateway:
    def process_request(self, ticket_id):
        # Fake server pretending to be the real API gateway
        print("[Fake API Gateway] Intercepting request... Ticket:", ticket_id)
        print("[Fake API Gateway] Access granted (malicious).")  # Maliciously granting access without validation


class SecureAPIGateway:
    def __init__(self, kdc):
        self.kdc = kdc

    def process_request(self, ticket_id):
        # Validate the ticket and generate server proof for mutual authentication
        is_valid, ticket = self.kdc.validate_ticket(ticket_id)
        if is_valid:
            print("[Secure API Gateway] Access granted.")
            # Generate proof of the server's identity for mutual authentication
            server_proof = self.generate_server_proof(ticket)
            return server_proof
        else:
            print("[Secure API Gateway] Access denied:", ticket)
            return None

    def generate_server_proof(self, ticket):
        # Generate proof by hashing the service name and expiry time
        proof = hashlib.sha256(f"{ticket['service']}{ticket['expiry']}".encode()).hexdigest()
        print(f"[Secure API Gateway] Sending proof: {proof}")
        return proof

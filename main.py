import time
from apikerberos.kdc import KDC
from apikerberos.client import Client, SecureClient
from apikerberos.apigateway import APIGateway, FakeAPIGateway, SecureAPIGateway

# Initialize KDC and API Gateway
kdc = KDC()
api_gateway = APIGateway(kdc)

# Simulate client interactions
client = Client("client1", kdc)

# Step 1: Client requests a ticket for the API service
client.request_ticket("api_service")

# Step 2: Client accesses the API with the obtained ticket
client.access_api(api_gateway)

# Simulate time passing to allow the ticket to expire
time.sleep(61)  # Wait for 1 minute + 1 second for ticket expiration

# Step 3: Client attempts to access API with the expired ticket (should fail)
print("\n[Client] Attempting to access API with expired ticket.")
client.access_api(api_gateway)

# Step 4: Client renews the ticket and accesses API again
client.renew_ticket()
client.access_api(api_gateway)

# Step 5: Simulate replay attack from a malicious client
print("\n[Malicious Client] Simulating replay attack with stolen ticket.")
malicious_client = Client("malicious_user", kdc)
malicious_client.access_api(api_gateway)  # Using the legitimate client's ticket

# Step 6: Demonstrate CSRF Prevention
print("\n[CSRF Prevention Demonstration]")
print("CSRF typically exploits browser-stored session tokens or cookies.")
print("In this system, no such tokens are stored in the browser.")
print("Every request is authenticated with a dynamically obtained, time-limited ticket.")
print("Thus, CSRF attacks cannot succeed as no session cookies or browser-stored tokens are available to exploit.")

# Step 7: Simulate MitM attack by the fake server
print("\n[Client] Simulating interaction with a fake server (MitM attack).")
fake_api_gateway = FakeAPIGateway()
client.access_api(fake_api_gateway)  # Fake server grants unauthorized access

# Step 8: Simulate mutual authentication to prevent MitM attack
print("\n[Secure Client] Demonstrating mutual authentication.")
secure_api_gateway = SecureAPIGateway(kdc)
server_proof = secure_api_gateway.process_request(client.ticket_id)

if server_proof:
    # Secure client attempts to verify the server
    secure_client = SecureClient(client.username, kdc)
    secure_client.validate_server(server_proof, "api_service", client.kdc.active_tickets[client.ticket_id]['expiry'])

    # Simulate MitM attack with mutual authentication
    print("\n[Secure Client] Attempting interaction with a fake server (MitM attack) during mutual authentication.")
    fake_server_proof = "fake_proof"  # Fake server cannot generate the correct proof
    secure_client.validate_server(fake_server_proof, "api_service", client.kdc.active_tickets[client.ticket_id]['expiry'])

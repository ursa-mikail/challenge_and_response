import hmac
import hashlib
import os

def generate_challenge():
    return os.urandom(16)

def sign_id(user_id, user_secret_key):
    return hmac.new(user_secret_key.encode(), user_id.encode(), hashlib.sha256).hexdigest()

def sign_id_and_cvv(user_id, cvv, service_secret_key):
    message = f"{user_id}:{cvv}"
    return hmac.new(service_secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

def sign_order_details(order_details, verifier_id, user_secret_key):
    message = f"{order_details}:{verifier_id}"
    return hmac.new(user_secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

def verify_signature(message, signature, secret_key):
    expected_signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

# Usage
user_id = "user123"
user_secret_key = "user_secret_key"
service_secret_key = "service_secret_key"
cvv = "123"
order_details = "itemX:100USD"
merchant_secret_key = "merchant_secret_key"

# Step 1: User signs their ID
signed_id = sign_id(user_id, user_secret_key)
print(f"User Signed ID: {signed_id}")

# Step 2: Service signs the ID and CVV
signed_id_and_cvv = sign_id_and_cvv(user_id, cvv, service_secret_key)
print(f"Service Signed ID and CVV: {signed_id_and_cvv}")

# Step 3: User signs the order details and verifier ID
verifier_id = signed_id_and_cvv
signed_order_details = sign_order_details(order_details, verifier_id, user_secret_key)
print(f"User Signed Order Details: {signed_order_details}")

# Step 4: Merchant verifies all signatures
full_message = f"{order_details}:{verifier_id}"
is_verified_by_user = verify_signature(user_id, signed_id, user_secret_key)
is_verified_by_service = verify_signature(f"{user_id}:{cvv}", signed_id_and_cvv, service_secret_key)
is_verified_by_merchant = verify_signature(full_message, signed_order_details, user_secret_key)

if is_verified_by_user and is_verified_by_service and is_verified_by_merchant:
    print("All signatures verified. Transaction accepted.")
else:
    print("Signature verification failed. Transaction rejected.")

"""
User Signed ID: 4815144e6aaff1a157888f1fb1a73243b96153c368ca24a9d157bb2d490dc8be
Service Signed ID and CVV: 35ff01c8710e292c3ae7cc5c3d1aba91ba10c9e696908f8f73ffe6ca337c55ff
User Signed Order Details: e6f62830351bee004c77efd0d85859b59de236078b05d86f27c7babdf73c9d93
All signatures verified. Transaction accepted.
"""
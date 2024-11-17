# challenge_response_using_hmac.py
# caveat: anti-nonce/random replay (e.g. rainbow table attacks) unavailable here.
import hmac
import hashlib
import os

def generate_random_challenge(length=16):
    return os.urandom(length)

def compute_hmac(key, message):
    return hmac.new(key, message, hashlib.sha256).digest()

def verify_hmac(key, message, received_hmac):
    return hmac.compare_digest(compute_hmac(key, message), received_hmac)


# Usage
# Keys for both parties (in practice, these should be securely shared)
key_A = b'secret_key_A'
key_B = b'secret_key_B'

# Step 1: Generate random challenges
challenge_A_to_B = generate_random_challenge() # issued by A to B
challenge_B_to_A = generate_random_challenge() # issued by B to A

# Step 2: Compute HMACs
hmac_A_to_B = compute_hmac(key_A, challenge_B_to_A)
hmac_B_to_A = compute_hmac(key_B, challenge_A_to_B)

# Simulate sending and receiving HMACs
received_hmac_A_to_B = hmac_A_to_B  # Party B receives this from Party A
received_hmac_B_to_A = hmac_B_to_A  # Party A receives this from Party B

# Step 3: Verify HMACs
if verify_hmac(key_A, challenge_B_to_A, received_hmac_A_to_B):
    print("Party B's challenge verified by Party A.")
else:
    print("Party B's challenge verification failed by Party A.")

if verify_hmac(key_B, challenge_A_to_B, received_hmac_B_to_A):
    print("Party A's challenge verified by Party B.")
else:
    print("Party A's challenge verification failed by Party B.")

"""
Party B's challenge verified by Party A.
Party A's challenge verified by Party B.
"""

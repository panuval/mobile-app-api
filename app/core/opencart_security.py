import hashlib

def verify_opencart_password(plain_password: str, stored_hash: str, salt: str) -> bool:
    """
    Verify an OpenCart password.
    OpenCart uses SHA-1(salt + plain_password)
    """
    # Calculate the SHA-1 hash
    calculated_hash = hashlib.sha1((salt + plain_password).encode()).hexdigest()
    
    # Compare with stored hash
    return calculated_hash == stored_hash
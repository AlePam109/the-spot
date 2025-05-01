import hashlib

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256 and returns the hex digest."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

import secrets
import base64

def generate_user_id():
    # 16 bytes  22 base64 chars (trimmed)
    return base64.urlsafe_b64encode(secrets.token_bytes(16)).decode("utf-8").rstrip("=")

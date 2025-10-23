import secrets

def generate_secret_key(length: int = 32) -> str:
    """
    Generate a cryptographically secure, URL-safe secret key.
    Default length is 32 bytes (~43 characters).
    """
    return secrets.token_urlsafe(length)

class ShotcutAPIError(Exception):
    """Base exception for Shotcut API errors"""
    
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class RateLimitError(ShotcutAPIError):
    """Raised when API rate limit is exceeded"""
    pass

class AuthenticationError(ShotcutAPIError):
    """Raised when API key is invalid or missing"""
    pass

class ValidationError(ShotcutAPIError):
    """Raised when request data is invalid"""
    pass


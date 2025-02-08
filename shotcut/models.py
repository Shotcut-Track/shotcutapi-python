from dataclasses import dataclass
from typing import Optional, List, Dict, Union
from datetime import datetime

@dataclass
class BaseModel:
    """Base model with common fields"""
    id: int
    created_at: datetime
    updated_at: datetime

@dataclass
class Link(BaseModel):
    """Model for shortened URL links"""
    url: str
    shorturl: str
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[Dict[str, str]] = None
    custom: Optional[str] = None
    password: Optional[str] = None
    expiry: Optional[datetime] = None
    clicks: int = 0
    status: bool = True

@dataclass
class Campaign(BaseModel):
    """Model for campaigns"""
    name: str
    slug: str
    public: bool = False
    total_links: int = 0
    total_clicks: int = 0

@dataclass
class Channel(BaseModel):
    """Model for channels"""
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    starred: bool = False
    total_items: int = 0

@dataclass
class Domain(BaseModel):
    """Model for branded domains"""
    domain: str
    status: bool
    redirect_root: Optional[str] = None
    redirect_404: Optional[str] = None
    ssl_status: bool = False

@dataclass
class Pixel(BaseModel):
    """Model for tracking pixels"""
    type: str
    name: str
    tag: str
    status: bool = True

@dataclass
class QRCode(BaseModel):
    """Model for QR codes"""
    type: str
    data: Union[str, Dict]
    link: str
    background: Optional[str] = None
    foreground: Optional[str] = None
    logo: Optional[str] = None

@dataclass
class Splash(BaseModel):
    """Model for splash pages"""
    name: str
    content: str
    status: bool = True

@dataclass
class AccountStats:
    """Model for account statistics"""
    total_links: int
    total_clicks: int
    total_campaigns: int
    total_channels: int
    total_domains: int
    total_pixels: int
    total_qr_codes: int

@dataclass
class PaginatedResponse:
    """Model for paginated API responses"""
    items: List[Union[Link, Campaign, Channel, Domain, Pixel, QRCode, Splash]]
    total: int
    current_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

@dataclass
class APIResponse:
    """Model for standard API responses"""
    error: int
    message: Optional[str] = None
    data: Optional[Union[Dict, List, BaseModel, PaginatedResponse]] = None

def convert_datetime(date_str: Optional[str]) -> Optional[datetime]:
    """Convert datetime string to datetime object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

def create_model_from_response(model_class: type, data: Dict) -> Union[BaseModel, None]:
    """Create a model instance from API response data"""
    if not data:
        return None
        
    # Convert datetime strings to datetime objects
    if 'created_at' in data:
        data['created_at'] = convert_datetime(data['created_at'])
    if 'updated_at' in data:
        data['updated_at'] = convert_datetime(data['updated_at'])
    if 'expiry' in data:
        data['expiry'] = convert_datetime(data['expiry'])
        
    try:
        return model_class(**data)
    except TypeError as e:
        raise ValueError(f"Invalid data for {model_class.__name__}: {str(e)}")
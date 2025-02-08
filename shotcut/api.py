import requests
from typing import Dict, List, Optional, Union
import json
from datetime import datetime

class ShotcutAPIError(Exception):
    """Custom exception for Shotcut API errors"""
    pass

class ShotcutAPI:
    """
    Python client for the Shotcut.in API
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Shotcut API client
        
        Args:
            api_key (str): Your Shotcut API key
        """
        self.api_key = api_key
        self.base_url = "https://shotcut.in/api"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """
        Make HTTP request to the API
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint
            data (dict, optional): Request body data
            params (dict, optional): Query parameters
            
        Returns:
            dict: Response data
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data if data else None,
                params=params if params else None
            )
            
            response_data = response.json()
            
            # Check for rate limit headers
            if response.headers.get('X-RateLimit-Remaining') == '0':
                reset_time = datetime.fromtimestamp(int(response.headers.get('X-RateLimit-Reset', 0)))
                raise ShotcutAPIError(f"Rate limit exceeded. Reset at {reset_time}")
            
            # Check for API errors
            if response_data.get('error') and response_data['error'] != 0:
                raise ShotcutAPIError(response_data.get('message', 'Unknown API error'))
                
            return response_data
            
        except requests.exceptions.RequestException as e:
            raise ShotcutAPIError(f"Request failed: {str(e)}")

    # Account Methods
    def get_account(self) -> Dict:
        """Get account information"""
        return self._make_request("GET", "account")

    def update_account(self, email: Optional[str] = None, password: Optional[str] = None) -> Dict:
        """Update account information"""
        data = {}
        if email:
            data['email'] = email
        if password:
            data['password'] = password
        return self._make_request("PUT", "account/update", data=data)

    # Branded Domains Methods
    def list_domains(self, limit: int = 10, page: int = 1) -> Dict:
        """List branded domains"""
        params = {'limit': limit, 'page': page}
        return self._make_request("GET", "domains", params=params)

    def create_domain(self, domain: str, redirect_root: Optional[str] = None, redirect_404: Optional[str] = None) -> Dict:
        """Create a branded domain"""
        data = {
            'domain': domain,
            'redirectroot': redirect_root,
            'redirect404': redirect_404
        }
        return self._make_request("POST", "domain/add", data=data)

    def update_domain(self, domain_id: int, redirect_root: Optional[str] = None, redirect_404: Optional[str] = None) -> Dict:
        """Update a branded domain"""
        data = {}
        if redirect_root:
            data['redirectroot'] = redirect_root
        if redirect_404:
            data['redirect404'] = redirect_404
        return self._make_request("PUT", f"domain/{domain_id}/update", data=data)

    def delete_domain(self, domain_id: int) -> Dict:
        """Delete a branded domain"""
        return self._make_request("DELETE", f"domain/{domain_id}/delete")

    # CTA Overlays Methods
    def list_overlays(self, limit: int = 10, page: int = 1) -> Dict:
        """List CTA overlays"""
        params = {'limit': limit, 'page': page}
        return self._make_request("GET", "overlay", params=params)

    # Campaigns Methods
    def list_campaigns(self, limit: int = 10, page: int = 1) -> Dict:
        """List campaigns"""
        params = {'limit': limit, 'page': page}
        return self._make_request("GET", "campaigns", params=params)

    def create_campaign(self, name: str, slug: Optional[str] = None, public: bool = False) -> Dict:
        """Create a campaign"""
        data = {
            'name': name,
            'slug': slug,
            'public': public
        }
        return self._make_request("POST", "campaign/add", data=data)

    def assign_link_to_campaign(self, campaign_id: int, link_id: int) -> Dict:
        """Assign a link to a campaign"""
        return self._make_request("POST", f"campaign/{campaign_id}/assign/{link_id}")

    def update_campaign(self, campaign_id: int, name: str, slug: Optional[str] = None, public: Optional[bool] = None) -> Dict:
        """Update a campaign"""
        data = {'name': name}
        if slug:
            data['slug'] = slug
        if public is not None:
            data['public'] = public
        return self._make_request("PUT", f"campaign/{campaign_id}/update", data=data)

    def delete_campaign(self, campaign_id: int) -> Dict:
        """Delete a campaign"""
        return self._make_request("DELETE", f"campaign/{campaign_id}/delete")

    # Channels Methods
    def list_channels(self, limit: int = 10, page: int = 1) -> Dict:
        """List channels"""
        params = {'limit': limit, 'page': page}
        return self._make_request("GET", "channels", params=params)

    def list_channel_items(self, channel_id: int, limit: int = 10, page: int = 1) -> Dict:
        """List items in a channel"""
        params = {'limit': limit, 'page': page}
        return self._make_request("GET", f"channel/{channel_id}", params=params)

    def create_channel(self, name: str, description: Optional[str] = None, 
                      color: Optional[str] = None, starred: bool = False) -> Dict:
        """Create a channel"""
        data = {
            'name': name,
            'description': description,
            'color': color,
            'starred': starred
        }
        return self._make_request("POST", "channel/add", data=data)

    def assign_item_to_channel(self, channel_id: int, item_type: str, item_id: int) -> Dict:
        """Assign an item to a channel"""
        return self._make_request("POST", f"channel/{channel_id}/assign/{item_type}/{item_id}")

    def update_channel(self, channel_id: int, name: Optional[str] = None, 
                      description: Optional[str] = None, color: Optional[str] = None, 
                      starred: Optional[bool] = None) -> Dict:
        """Update a channel"""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if color:
            data['color'] = color
        if starred is not None:
            data['starred'] = starred
        return self._make_request("PUT", f"channel/{channel_id}/update", data=data)

    def delete_channel(self, channel_id: int) -> Dict:
        """Delete a channel"""
        return self._make_request("DELETE", f"channel/{channel_id}/delete")

    # Custom Splash Methods
    def list_splash(self, limit: int = 10, page: int = 1) -> Dict:
        """List custom splash pages"""
        params = {'limit': limit, 'page': page}
        return self._make_request("GET", "splash", params=params)

    # Links Methods
    def list_links(self, limit: int = 10, page: int = 1, order: str = 'date', short: Optional[str] = None) -> Dict:
        """List links"""
        params = {'limit': limit, 'page': page, 'order': order}
        if short:
            params['short'] = short
        return self._make_request("GET", "urls", params=params)

    def get_link(self, link_id: int) -> Dict:
        """Get a single link"""
        return self._make_request("GET", f"url/{link_id}")

    def shorten_link(self, url: str, **kwargs) -> Dict:
        """
        Shorten a link with optional parameters
        
        Args:
            url (str): URL to shorten
            **kwargs: Optional parameters (custom, type, password, domain, expiry, etc.)
        """
        data = {'url': url, **kwargs}
        return self._make_request("POST", "url/add", data=data)

    def update_link(self, link_id: int, **kwargs) -> Dict:
        """Update a link"""
        return self._make_request("PUT", f"url/{link_id}/update", data=kwargs)

    def delete_link(self, link_id: int) -> Dict:
        """Delete a link"""
        return self._make_request("DELETE", f"url/{link_id}/delete")

    # Pixels Methods
    def list_pixels(self, limit: int = 10, page: int = 1) -> Dict:
        """List pixels"""
        params = {'limit': limit, 'page': page}
        return self._make_request("GET", "pixels", params=params)

    def create_pixel(self, type: str, name: str, tag: str) -> Dict:
        """Create a pixel"""
        data = {
            'type': type,
            'name': name,
            'tag': tag
        }
        return self._make_request("POST", "pixel/add", data=data)

    def update_pixel(self, pixel_id: int, name: Optional[str] = None, tag: Optional[str] = None) -> Dict:
        """Update a pixel"""
        data = {}
        if name:
            data['name'] = name
        if tag:
            data['tag'] = tag
        return self._make_request("PUT", f"pixel/{pixel_id}/update", data=data)

    def delete_pixel(self, pixel_id: int) -> Dict:
        """Delete a pixel"""
        return self._make_request("DELETE", f"pixel/{pixel_id}/delete")

    # QR Codes Methods
    def list_qr_codes(self, limit: int = 10, page: int = 1) -> Dict:
        """List QR codes"""
        params = {'limit': limit, 'page': page}
        return self._make_request("GET", "qr", params=params)

    def get_qr_code(self, qr_id: int) -> Dict:
        """Get a single QR code"""
        return self._make_request("GET", f"qr/{qr_id}")

    def create_qr_code(self, type: str, data: Union[str, Dict], 
                      background: Optional[str] = None, 
                      foreground: Optional[str] = None,
                      logo: Optional[str] = None) -> Dict:
        """Create a QR code"""
        qr_data = {
            'type': type,
            'data': data
        }
        if background:
            qr_data['background'] = background
        if foreground:
            qr_data['foreground'] = foreground
        if logo:
            qr_data['logo'] = logo
        return self._make_request("POST", "qr/add", data=qr_data)

    def update_qr_code(self, qr_id: int, data: Union[str, Dict],
                      background: Optional[str] = None,
                      foreground: Optional[str] = None,
                      logo: Optional[str] = None) -> Dict:
        """Update a QR code"""
        qr_data = {'data': data}
        if background:
            qr_data['background'] = background
        if foreground:
            qr_data['foreground'] = foreground
        if logo:
            qr_data['logo'] = logo
        return self._make_request("PUT", f"qr/{qr_id}/update", data=qr_data)

    def delete_qr_code(self, qr_id: int) -> Dict:
        """Delete a QR code"""
        return self._make_request("DELETE", f"qr/{qr_id}/delete")
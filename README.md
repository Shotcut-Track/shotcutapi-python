# Shotcut Python API Client

A comprehensive Python client for the [Shotcut.in](shotcut.in) URL shortener API. This package provides an intuitive interface to interact with all Shotcut.in API endpoints.

Get Your API Key [Here](https://shotcut.in/developers)

## Table of Contents
- [Installation](#installation)
- [Features](#features)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
  - [Account Management](#account-management)
  - [URL Shortening](#url-shortening)
  - [QR Codes](#qr-codes)
  - [Campaigns](#campaigns)
  - [Branded Domains](#branded-domains)
  - [Channels](#channels)
  - [Pixels](#pixels)
  - [Custom Splash Pages](#custom-splash-pages)
  - [CTA Overlays](#cta-overlays)
- [Error Handling](#error-handling)
- [Development](#development)
- [License](#license)

## Installation

```bash
pip install shotcut-python
```

## Features

- **URL Shortening**: Create and manage shortened URLs with custom aliases
- **QR Code Generation**: Create customizable QR codes with logos and colors
- **Campaign Management**: Organize and track marketing campaigns
- **Branded Domains**: Set up and manage custom domains
- **Channels**: Organize content into channels with custom settings
- **Pixels**: Implement tracking pixels for analytics
- **Custom Splash Pages**: Create and manage intermediate pages
- **CTA Overlays**: Add call-to-action overlays to links
- **Error Handling**: Built-in handling for API errors and rate limits
- **Type Hints**: Full typing support for better IDE integration

## Quick Start

```python
from shotcut import ShotcutAPI

# Initialize the client
api = ShotcutAPI(api_key="your_api_key_here")

# Shorten a URL
response = api.shorten_link(
    url="https://example.com",
    custom="my-custom-alias"
)
print(response['shorturl'])

# Create a QR code
qr = api.create_qr_code(
    type="link",
    data="https://example.com",
    background="rgb(255,255,255)",
    foreground="rgb(0,0,0)"
)
print(qr['link'])
```

## API Reference

### Account Management

```python
# Get account information
account = api.get_account()

# Update account details
api.update_account(
    email="newemail@example.com",
    password="newpassword123"
)
```

### URL Shortening

```python
# Create a shortened URL
url = api.shorten_link(
    url="https://example.com",
    custom="my-link",
    password="secret123",
    expiry="2025-12-31",
    domain="custom.com"
)

# List all URLs
urls = api.list_links(
    limit=20,
    page=1,
    order="clicks"
)

# Get single URL details
url_details = api.get_link(link_id=123)

# Update URL
api.update_link(
    link_id=123,
    url="https://newexample.com",
    password="newpassword123"
)

# Delete URL
api.delete_link(link_id=123)
```

### QR Codes

```python
# Create QR code
qr = api.create_qr_code(
    type="link",
    data="https://example.com",
    background="rgb(255,255,255)",
    foreground="rgb(0,0,0)",
    logo="https://example.com/logo.png"
)

# List QR codes
qr_codes = api.list_qr_codes(limit=20, page=1)

# Get single QR code
qr_details = api.get_qr_code(qr_id=123)

# Update QR code
api.update_qr_code(
    qr_id=123,
    data="https://newexample.com",
    background="rgb(0,0,255)"
)

# Delete QR code
api.delete_qr_code(qr_id=123)
```

### Campaigns

```python
# Create campaign
campaign = api.create_campaign(
    name="Summer Sale 2025",
    slug="summer-sale",
    public=True
)

# List campaigns
campaigns = api.list_campaigns(limit=20, page=1)

# Assign link to campaign
api.assign_link_to_campaign(
    campaign_id=123,
    link_id=456
)

# Update campaign
api.update_campaign(
    campaign_id=123,
    name="Winter Sale 2025",
    public=False
)

# Delete campaign
api.delete_campaign(campaign_id=123)
```

### Branded Domains

```python
# List domains
domains = api.list_domains(limit=20, page=1)

# Create domain
domain = api.create_domain(
    domain="short.example.com",
    redirect_root="https://example.com",
    redirect_404="https://example.com/404"
)

# Update domain
api.update_domain(
    domain_id=123,
    redirect_root="https://newexample.com"
)

# Delete domain
api.delete_domain(domain_id=123)
```

### Channels

```python
# Create channel
channel = api.create_channel(
    name="Marketing",
    description="Marketing campaign links",
    color="rgb(255,0,0)",
    starred=True
)

# List channels
channels = api.list_channels(limit=20, page=1)

# List channel items
items = api.list_channel_items(
    channel_id=123,
    limit=20,
    page=1
)

# Update channel
api.update_channel(
    channel_id=123,
    name="Sales",
    starred=False
)

# Delete channel
api.delete_channel(channel_id=123)
```

### Pixels

```python
# Create pixel
pixel = api.create_pixel(
    type="facebook",
    name="FB Conversion Pixel",
    tag="123456789"
)

# List pixels
pixels = api.list_pixels(limit=20, page=1)

# Update pixel
api.update_pixel(
    pixel_id=123,
    name="Updated FB Pixel",
    tag="987654321"
)

# Delete pixel
api.delete_pixel(pixel_id=123)
```

### Custom Splash Pages

```python
# List splash pages
splash_pages = api.list_splash(limit=20, page=1)
```

### CTA Overlays

```python
# List overlays
overlays = api.list_overlays(limit=20, page=1)
```

## Error Handling

```python
from shotcut import ShotcutAPI, ShotcutAPIError

try:
    api = ShotcutAPI(api_key="your_key")
    response = api.create_link(url="https://example.com")
except ShotcutAPIError as e:
    print(f"API Error: {str(e)}")
except RateLimitError as e:
    print(f"Rate limit exceeded. Reset at {e.reset_time}")
except AuthenticationError as e:
    print("Invalid API key")
except ValidationError as e:
    print(f"Invalid data: {str(e)}")
```

## Development

To contribute to this project:

1. Clone the repository
```bash
git clone https://github.com/Shotcut-Track/shotcutapi-python.git
```

2. Install development dependencies
```bash
pip install -e ".[dev]"
```

3. Run tests
```bash
pytest
```

## License

MIT License - see [LICENSE](https://github.com/Shotcut-Track/shotcutapi-python/blob/main/LICENSE) file for details.

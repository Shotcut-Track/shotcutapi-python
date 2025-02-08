from typing import Optional, Dict, Any
from datetime import datetime

def validate_date(date_str: Optional[str]) -> bool:
    """Validate date string format"""
    if not date_str:
        return True
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def clean_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from params dictionary"""
    return {k: v for k, v in params.items() if v is not None}

def validate_rgb_color(color: Optional[str]) -> bool:
    """Validate RGB color format"""
    if not color:
        return True
    if not color.startswith("rgb(") or not color.endswith(")"):
        return False
    try:
        values = color[4:-1].split(",")
        if len(values) != 3:
            return False
        return all(0 <= int(v.strip()) <= 255 for v in values)
    except ValueError:
        return False

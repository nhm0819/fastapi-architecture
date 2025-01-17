from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    lat: Optional[float] = None
    lng: Optional[float] = None

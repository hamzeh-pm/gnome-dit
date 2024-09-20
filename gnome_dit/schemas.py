from dataclasses import dataclass

from gnome_dit.constants import IconType


@dataclass
class UbuntuIcon:
    """Ubuntu Icons"""

    icon_type: IconType
    name: str
    location: str
    image_location: str

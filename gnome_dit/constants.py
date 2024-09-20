from enum import Enum


class IconType(Enum):
    GNOME = 1
    SNAPD = 2


GNOME_DESKTOP_ICON_LOCATION = "/usr/share/applications/"
SNAPD_DESKTOP_ICON_LOCATION = "/var/lib/snapd/desktop/applications/"
GNOME_DESKTOP_ICON_EXTENSION = ".desktop"
UBUNTU_ICON_IMAGE_LOCATION = "/usr/share/icons/"
SNAPD_ICON_IMAGE_LOCATION = "/snap/"

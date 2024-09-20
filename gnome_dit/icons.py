import os
import shutil

import cairosvg

from gnome_dit.constants import (
    GNOME_DESKTOP_ICON_EXTENSION,
    GNOME_DESKTOP_ICON_LOCATION,
    SNAPD_DESKTOP_ICON_LOCATION,
    SNAPD_ICON_IMAGE_LOCATION,
    UBUNTU_ICON_IMAGE_LOCATION,
    IconType,
)
from gnome_dit.schemas import UbuntuIcon


def load_icon_images() -> list[tuple]:
    icon_images = []
    icon_image_extensions = [".png", ".svg", ".jpg", ".jpeg"]

    for root, dirs, files in os.walk(UBUNTU_ICON_IMAGE_LOCATION):
        for file in files:
            if file.endswith(tuple(icon_image_extensions)):
                icon_images.append((root, file))

    for root, dirs, files in os.walk(SNAPD_DESKTOP_ICON_LOCATION):
        for file in files:
            if file.endswith(tuple(icon_image_extensions)):
                icon_images.append((root, file))

    return icon_images


def search_for_icon_file(icon_images, icon_name: str) -> str:
    for image in icon_images:
        if image[1].startswith(icon_name):
            if image[1].endswith(".svg"):
                try:
                    # convert svg file to png
                    png_image_name = image[1].removesuffix(".svg") + ".png"
                    png_image_location = os.path.join("png_icons", png_image_name)
                    if not os.path.exists(png_image_location):
                        cairosvg.svg2png(
                            url=os.path.join(image[0], image[1]),
                            write_to=png_image_location,
                        )
                        return png_image_location
                except:
                    return None
            else:
                return os.path.join(image[0], image[1])


def get_icon_image_name_from_desktop_file(desktop_file_path: str):
    with open(desktop_file_path, "r") as f:
        for line in f:
            if line.startswith("Icon="):
                return line.split("=")[1].strip()


def get_gnome_desktop_icons(desktop_images: list[tuple]) -> list[UbuntuIcon]:
    gnome_icons: list[UbuntuIcon] = []

    for f in os.listdir(GNOME_DESKTOP_ICON_LOCATION):
        if f.endswith(GNOME_DESKTOP_ICON_EXTENSION):
            image_name = get_icon_image_name_from_desktop_file(
                os.path.join(GNOME_DESKTOP_ICON_LOCATION + f)
            )

            if image_name:
                image_location = search_for_icon_file(desktop_images, image_name)

                if image_location:
                    # create a new UbuntuIcon object
                    icon = UbuntuIcon(
                        icon_type=IconType.GNOME,
                        name=f,
                        location=os.path.join(GNOME_DESKTOP_ICON_LOCATION + f),
                        image_location=image_location,
                    )
                    gnome_icons.append(icon)

    return gnome_icons


def get_snapd_desktop_icons(desktop_images: list[tuple]) -> list[UbuntuIcon]:
    snapd_icons: list[UbuntuIcon] = []

    for f in os.listdir(SNAPD_DESKTOP_ICON_LOCATION):
        if f.endswith(GNOME_DESKTOP_ICON_EXTENSION):
            image_name = get_icon_image_name_from_desktop_file(
                os.path.join(SNAPD_DESKTOP_ICON_LOCATION + f)
            )

            if image_name:
                image_location = search_for_icon_file(desktop_images, image_name)

                if image_location:
                    # create a new UbuntuIcon object
                    icon = UbuntuIcon(
                        icon_type=IconType.GNOME,
                        name=f,
                        location=os.path.join(SNAPD_ICON_IMAGE_LOCATION + f),
                        image_location=image_location,
                    )
                    snapd_icons.append(icon)

    return snapd_icons


def action_copy_icon_to_desktop(ubuntu_icon: UbuntuIcon):
    source_path = ubuntu_icon.location
    destination_path = os.path.join(os.path.expanduser("~/Desktop"), ubuntu_icon.name)

    shutil.copy(source_path, destination_path)
    # Allow launching the .desktop file
    os.chmod(destination_path, 0o755)

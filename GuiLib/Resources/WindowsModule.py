import platform
import sys
from pathlib import Path


# this is just a script for every window in the app to get the image for the bitmap

# Make so every window in the app gets it's bitmap from here


# For the image to work after making the app an exe
def resource_path(relative_path):
    # If running as a PyInstaller bundle
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent  # Adjust as needed for your structure
    return base_path / relative_path


# convert image to ico for windows and png for linux and return the path based on the the system of the pc
def get_path_to_BitMap() -> str:  # Default to dark mode

    image_path: str = ""

    passwordManagerIcoW: str = "Password Manager Bitmap White.ico"
    passwordManagerPngW: str = "Password Manager Bitmap White.png"

    if platform.system() == "Windows":
        image_path = resource_path(f"Resources/{passwordManagerIcoW}")
    else:
        image_path = resource_path(f"Resources/{passwordManagerPngW}")

    return image_path


def on_close(self):
    # Destroy both the toplevel and the root window
    self.destroy()
    if self.master:
        self.master.destroy()

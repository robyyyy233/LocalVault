import json
import os

import customtkinter as ctk
from PIL import Image
import sys
from pathlib import Path


from . import LoginWindowMainFunctions as mainfuncs
from GuiLib import SelectVaultWindow as VaultSelectWindow
from .VaultSetup import get_config_file_path
from GuiLib.Resources import WindowsModule as WM


DEBUG_INFO: bool = False


# For the image to work after making the app an exe
def resource_path(relative_path):
    # If running as a PyInstaller bundle
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent  # Adjust as needed for your structure
    return base_path / relative_path


def get_hidden_show_password_image(entry, showButton=None):

    image_show: str = "ShowPassword.png"
    image_hide: str = "HidePassword.png"

    charMask = entry.cget("show")

    # first time call
    if showButton is None:
        filename = image_show if charMask == "" else image_show
        return resource_path(f"Resources/{filename}")

    # initial setup
    if charMask == "":

        # Button configurate
        if showButton is not None:
            showButton.configure(
                image=ctk.CTkImage(
                    Image.open(resource_path(f"Resources/{image_show}")), size=(30, 30)
                )
            )

        # Entry configurate
        entry.configure(show="*")
        entry.configure(font=("Arial", 28))

    elif charMask == "*":
        # Button configurate
        if showButton is not None:
            showButton.configure(
                image=ctk.CTkImage(
                    Image.open(resource_path(f"Resources/{image_hide}")), size=(30, 30)
                )
            )

        # Entry configurate
        entry.configure(show="")
        entry.configure(font=("Arial", 22))

    else:
        if DEBUG_INFO:
            print("Error in get_hidden_show_password_image function")


def get_path_to_logo() -> str:

    image: str = "LogoW.png"

    logo_path = resource_path(f"Resources/{image}")
    return logo_path

def get_path_to_settings_png() -> str:
    image: str = "Settings.png"
    png_path = resource_path(f"Resources/{image}")
    return png_path


def master_password_not_set_actions(
    login_button: ctk.CTkButton,
    master_entry: ctk.CTkEntry,
    LoginWindow,
    pathToFolder: str,
) -> None:

    login_button.configure(text="Register")
    login_button.configure(
        command=lambda: mainfuncs.show_message_box(
            master_entry, LoginWindow, pathToFolder
        )
    )
    master_entry.configure(placeholder_text="Set Master Password")



def create_config() -> None:
    #get appdata
    appdata_path = os.environ.get("APPDATA")

    if not appdata_path:
        raise FileNotFoundError("AppData not found.")

    # create folder
    LocalVaultFolder = os.path.join(appdata_path, "LocalVault")
    os.makedirs(LocalVaultFolder, exist_ok=True)


    config_file = os.path.join(LocalVaultFolder, "config.json")

    default_config = {
        "Versions": {
            "version": "1.0",
            "vault_version": "1.0",
        },
        "Vault": {
            "current_vault": "None",
            "vault_version": "1.0",
            "vault_magic_string": "LVPM",
        }
    }

    # create config.json
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            json.dump(default_config, f, indent=4)
    else: print("Config exists")


#check if the config has a vault saved
def check_saved_vault() -> bool:
    config_path = get_config_file_path()

    with open(config_path, "r") as config_read:
        config = json.load(config_read)

    current_vault = config["Vault"]["current_vault"]
    print(f"Current Vault: {current_vault}")

    if current_vault == "None":
        return False

    return True



#show settings window
def show_vault_selection_window(master, label) -> None:


    window = VaultSelectWindow.SelectVaultWindow(master, label)
    window.transient(master)
    window.grab_set()
    window.focus_force()
    master.wait_window(window)




if __name__ == "__main__":
    pass
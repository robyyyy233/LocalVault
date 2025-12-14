import json
from pathlib import Path

#todo: make the function to generate a password and email



def close_window(window):
    window.destroy()


#todo: save password to json file
def save_password_json(password: str, email: str, site: str, optional: str):

    #Location
    passwords_path : Path = Path.home() / "Documents" / "PasswordManager" / "Passwords.json"

   #todo: do it later







if __name__ == "__main__":
    save_password_json()

import json

from pathlib import Path

#Creates settings file
def create_settings_json() -> str:
    file_name: str = "Settings.json"
    file_path = Path.home() / "Documents" / "PasswordManager" / file_name

    if not file_path.exists() and not file_path.is_file():
        with open(file_path, "w") as settings_file:
         print(f"Settings file created at {file_path}")
    else:
        print(f"Settings file found at {file_path}")


    return str(file_path)

if __name__ == "__main__":
    pass
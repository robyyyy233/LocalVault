import customtkinter as ctk
from PIL import Image

# For bitmap
from GuiLib.Resources import WindowsModule

import GuiLib.LoginWindowFunctions.LoginWindowSetupFunctions as SetupFuncs

#vault functions
import GuiLib.VaultFunctions.VaultUnlock as VaultUnlock
from GuiLib.VaultFunctions.VaultSetup import get_current_vault_path

from GuiLib.MainWindowFunctions import TabsFunctions as TabsFunctions
from GuiLib.NewTabTopLevel import SaveTab

from GuiLib.GenerateSettingsFunctions import GenerateSettingsFunctions as SettingsFuncs
from GuiLib.TopLevelPasswordFunctions import SavePasswordTopLevelFunctions as SaveFuncs
from GuiLib.MainWindowFunctions import PasswordListFunctions


class MainWindow(ctk.CTk):
    def __init__(self, vault_key: bytes): 
        super().__init__()

        #key for encrypting/decrypting
        self.vault_key = vault_key
        vault_key = None
        del vault_key

        #Open vault and decrypt
        self.vault_data = VaultUnlock.decrypt(self.vault_key) 
        self.vault_path = get_current_vault_path()
        

        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(200, lambda: self.attributes("-topmost", False))

        self.delete_tab_mode: bool = False
        self.tab_buttons: list = []
        self.current_tab: str = "All"

        self.configure(fg_color="#0f1215")
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("dark")

        self.title("SafeKeep - Password Manager")
        self.geometry("800x400")
        self.resizable(False, False)

        self.lift()
        self.focus_force()

        # Icon bitmap
        self.icon_path = WindowsModule.get_path_to_BitMap()
        self.iconbitmap(self.icon_path)
    
    

        # Grid Columns:
        # 0 = tabs frame
        # 1 = separator
        # 2 = password list frame
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # Grid rows
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        # Tabs frame (left)
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent", width=180)
        self.left_frame.grid(
            row=0, column=0, sticky="nsw", rowspan=3, padx=(10, 10), pady=(10, 10)
        )

        self.left_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.left_frame.rowconfigure(5, weight=1)

        self.TabsFrameLocation = ctk.CTkScrollableFrame(
            self.left_frame,
            fg_color="transparent",
            width=180,
            scrollbar_button_color="#151A22",
            scrollbar_button_hover_color="#1D2F60",
        )
        self.TabsFrameLocation.grid(row=0, column=0, rowspan=5, sticky="nsew")
        
        
        # render tabs
        TabsFunctions.render_tabs(self)
        

        self.button_tabs = ctk.CTkFrame(
            self.left_frame, fg_color="transparent", width=180, height=60
        )
        self.button_tabs.grid(row=6, column=0, sticky="nsew")

        # New tab button
        self.new_tab_button = ctk.CTkButton(
            self.button_tabs,
            text="New Tab",
            font=("Arial", 16),
            width=100,
            height=40,
            fg_color="#1C2F63",
            hover_color="#233A78",
            text_color="#FFFFFF",
            corner_radius=3,
            command=lambda: TabsFunctions.show_top_level(
                self, SaveTab, self.TabsFrameLocation
            ),
        )
        self.new_tab_button.grid(row=0, column=0, padx=(0, 5), pady=(0, 7), sticky="ew")

        self.delete_tab_button = ctk.CTkButton(
            self.button_tabs,
            text="Delete Tab",
            font=("Arial", 16),
            width=100,
            height=40,
            fg_color="#9A3131",
            hover_color="#B03838",
            text_color="#FFFFFF",
            corner_radius=3,
        )

        self.delete_tab_button.configure(
            command=lambda: TabsFunctions.delete_tab_mode(self)
        )
        self.delete_tab_button.grid(
            row=0, column=1, padx=(0, 0), pady=(0, 7), sticky="ew"
        )

        # Separator (middle)
        self.separator = ctk.CTkFrame(self, fg_color="#26292d", width=2)
        self.separator.grid(row=0, column=1, sticky="ns", rowspan=3, pady=10)

        # Password list frame (right)
        self.main_frame = ctk.CTkFrame(
            self, fg_color="#0f1215"
        )  # change color back later to fg color
        self.main_frame.grid(
            row=0,
            column=2,
            rowspan=3,
            sticky="nsew",
            padx=(0, 0),
            pady=(0, 0),
        )

        # Password list frame grid configuration
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=0)

        self.main_frame.grid_rowconfigure(1, weight=0)  # for buttons
        self.main_frame.grid_rowconfigure(2, weight=0)  # for separator
        self.main_frame.grid_rowconfigure(3, weight=1)

        # buttons frame
        self.buttons_frame = ctk.CTkFrame(
            self.main_frame, fg_color="#0f1215", height=80
        )
        self.buttons_frame.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="new",
            padx=(10, 10),
            pady=(10, 10),
        )

        # Column 2 expands to push settings button to the right
        self.buttons_frame.grid_columnconfigure(2, weight=1)

        # Settings button
        settings_image = Image.open(SetupFuncs.get_path_to_settings_png())
        self.ctk_settings_image = ctk.CTkImage(dark_image=settings_image, size=(40, 40))

        self.settings_button = ctk.CTkButton(
            self.buttons_frame,
            text="",
            image=self.ctk_settings_image,
            fg_color="transparent",
            hover_color="#0f1215",
            corner_radius=8,
            width=42,
            height=42,
            border_width=0,
            command=lambda: SettingsFuncs.show_generate_settings(self),
        )
        self.settings_button.grid(row=0, column=3, padx=(5, 10), pady=(10, 10), sticky="e")

        # Add Password button
        self.add_password_button = ctk.CTkButton(
            self.buttons_frame,
            text="Add Password",
            font=("Arial", 18),
            fg_color="#22262b",
            text_color="#ffffff",
            corner_radius=8,
            width=160,
            height=42,
            border_width=1,
            border_color="#2e3338",
            hover_color="#2c3139",
            command=lambda: SaveFuncs.show_add_password_window(self),
        )
        self.add_password_button.grid(row=0, column=0, padx=(10, 5), pady=(10, 10))

        # Generate Password button
        self.generate_button = ctk.CTkButton(
            self.buttons_frame,
            text="Generate",
            font=("Arial", 18),
            fg_color="#22262b",
            text_color="#ffffff",
            corner_radius=8,
            width=160,
            height=42,
            border_width=1,
            border_color="#2e3338",
            hover_color="#2c3139",
            command=lambda: SettingsFuncs.show_generate_window(self),
        )
        self.generate_button.grid(row=0, column=1, padx=(5, 5), pady=(10, 10))

        # Current tab indicator
        self.current_tab_label = ctk.CTkLabel(
            self.buttons_frame,
            text="All",
            text_color="#9a9a9a",
            font=("Arial", 15),
            anchor="e",
        )
        self.current_tab_label.grid(row=0, column=2, padx=(10, 5), sticky="e")

        # main frame separator
        self.main_frame_separator = ctk.CTkFrame(
            self.main_frame, fg_color="#26292d", height=2
        )
        self.main_frame_separator.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=(0, 10),
        )

        # password list display frame
        self.password_list_frame = ctk.CTkScrollableFrame(
            self.main_frame, fg_color="#0f1215",
            scrollbar_button_color="#26292d",
            scrollbar_button_hover_color="#3A3D41",
        )
        self.password_list_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            rowspan=2,
            sticky="nsew",
            padx=(10, 10),
            pady=(10, 10),
        )

        PasswordListFunctions.render_passwords(self)

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", WindowsModule.on_close.__get__(self))


if __name__ == "__main__":
    mainWindow = MainWindow()
    mainWindow.mainloop()

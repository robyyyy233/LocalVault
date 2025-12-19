import customtkinter as ctk
from PIL import Image

from GuiLib.LoginWindowFunctions import LoginWindowMainFunctions as MainFuncs
from GuiLib.LoginWindowFunctions import LoginWindowSetupFunctions as SetupFuncs


# For bitmap
from Resources import WindowsModule


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Create the folder to store the passwords
        folder_path = MainFuncs.create_folder()
        master_password_exists = MainFuncs.check_user_has_master_password(folder_path)

        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color="#0f1215")

        self.title("Password Manager Login")
        self.geometry("700x400")
        self.eval("tk::PlaceWindow %s center" % self.winfo_toplevel())
        self.resizable(False, False)

        # Icon
        icon_path = WindowsModule.get_path_to_BitMap()
        self.iconbitmap(icon_path)

        self.rowconfigure((0,1,2), weight=1)
        self.columnconfigure((0,1,2), weight=1)

        self.MainFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.MainFrame.grid(row=0, column=0, rowspan=3, columnspan=3, padx=(10,10), pady=(10,10), sticky="nsew")

        self.MainFrame.rowconfigure((0,1,2), weight=0)
        self.MainFrame.columnconfigure((0,2), weight=0)
        self.MainFrame.columnconfigure(1, weight=1)




        #Logo + App Name
        self.LogoFrame = ctk.CTkFrame(self.MainFrame, fg_color="transparent", height=75)
        self.LogoFrame.grid(row=0, column=1, sticky="n")

        self.LogoFrame.rowconfigure((0,1,2), weight=0)
        self.LogoFrame.columnconfigure((0,1,2), weight=0)

        #Logo
        logo = Image.open(SetupFuncs.get_path_to_logo())
        ctk_logo = ctk.CTkImage(dark_image=logo, size=(125,125))
        self.Logo = ctk.CTkLabel(self.LogoFrame, image=ctk_logo, text="")
        self.Logo.grid(row=0, column=0, sticky="nsew")

        self.LogoLabel = ctk.CTkLabel(self.LogoFrame, text="LocalVault", font=("Arial", 66, "bold"), text_color="#ffffff")
        self.LogoLabel.grid(row=0, column=1, sticky="ew")


        #Settings frame + button
        self.SettingsFrame = ctk.CTkFrame(self.MainFrame, fg_color="transparent", height=10, width=10)
        self.SettingsFrame.grid(row=0, column=2, sticky="ne")

        #settings image
        settings_image = Image.open(SetupFuncs.get_path_to_settings_png())
        ctk_settings_image = ctk.CTkImage(dark_image=settings_image, size=(40,40))
        self.SettingsButton = ctk.CTkButton(self.SettingsFrame,image=ctk_settings_image, text="", fg_color="transparent", hover_color="#0f1215", width=10, height=10, cursor="hand2",
                                            #todo:add command
                                            )
        self.SettingsButton.grid(row=0, column=0, sticky="nsew")



        #Entry + show password button
        self.EntryFrame = ctk.CTkFrame(self.MainFrame, fg_color="transparent", height=75, )
        self.EntryFrame.grid(row=1, column=1, sticky="nsew", pady=(10,0))

        self.EntryFrame.rowconfigure((0,1,2), weight=0)
        self.EntryFrame.columnconfigure((0,1,2,3,4,5,6), weight=1)


        #Master password entry
        self.MasterPasswordEntry = ctk.CTkEntry(self.EntryFrame,
            width=300,
            height=60,
            corner_radius=10,
            border_width=1,
            bg_color="#0f1215",
            fg_color="#111317",
            border_color="#1e2126",
            placeholder_text_color="#474d59",
            text_color="#FFFFFF",
            font=("Arial", 28),
            placeholder_text="Enter Master Password",
            justify="left",
            show="*",)
        self.MasterPasswordEntry.grid(row=0, column=3, columnspan = 3, sticky="ew", padx=(10,0))


        # get show/hide password image
        self.showButtonImage = ctk.CTkImage(
            Image.open(
                SetupFuncs.get_hidden_show_password_image(self.MasterPasswordEntry, None)
            ),
            size=(30, 30),
        )

        # Show master password button
        self.ShowPasswordButton = ctk.CTkButton(self.EntryFrame,
                                                width=40,
                                                height=40,
                                                corner_radius=10,
                                                fg_color="transparent",
                                                hover_color="#0f1215",
                                                text="",
                                                image=self.showButtonImage,
                                                command=lambda: SetupFuncs.get_hidden_show_password_image(self.MasterPasswordEntry, self.ShowPasswordButton),)
        self.ShowPasswordButton.grid(row=0, column=6, sticky="w", padx=(5,0))

        #Login frame + button

        self.LoginButtonFrame = ctk.CTkFrame(self.MainFrame, fg_color="transparent", height=50)
        self.LoginButtonFrame.grid(row=2, column=0, columnspan=3, pady=(20,0), sticky="nsew")

        self.LoginButtonFrame.rowconfigure((0,1,2), weight=0)
        self.LoginButtonFrame.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13), weight=1)


        # Login button
        self.LoginButton = ctk.CTkButton(
            self.LoginButtonFrame,
            fg_color="#2563eb", text_color="#e6edf3",
            text="Login", corner_radius=10, width=100, height=40, font=("Arial", 20, "bold"),
            border_width=1, border_color="#1e3a8a", hover_color="#1d4ed8")
        self.LoginButton.grid(row=0, column=10, sticky="ns", padx=(0,0))



        


        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", WindowsModule.on_close.__get__(self))
        self.focus()
        self.focus_force()


if __name__ == "__main__":
    loginWindow = LoginWindow()
    loginWindow.mainloop()

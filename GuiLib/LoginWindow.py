import customtkinter as ctk
from PIL import Image


from LoginWindowFunctions import LoginWindowMainFunctions as MainFuncs
from LoginWindowFunctions import LoginWindowSetupFunctions as SetupFuncs

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
        self.icon_path = WindowsModule.get_path_to_BitMap()
        self.iconbitmap(self.icon_path)

        # Grid: center column for content, side columns as flexible spacers
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)  # content column
        self.grid_columnconfigure(2, weight=1)

        # Rows:
        # 0 = logo (fixed)
        # 1 = spacer (expands)
        # 2 = entry (fixed)
        # 3 = spacer (expands)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)

        # --- Logo Frame (row 0) ---
        self.logo_frame = ctk.CTkFrame(
            self,
            width=400,
            height=110,  # slightly taller for image padding
            corner_radius=10,
            fg_color="transparent",
        )
        self.logo_frame.grid(row=0, column=1, padx=0, pady=(16, 8), sticky="n")
        self.logo_frame.grid_propagate(False)
        self.logo_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.logo_frame.grid_rowconfigure(0, weight=1)

        # Logo Image
        self.logo_path = SetupFuncs.get_path_to_logo()
        self.logo_image = ctk.CTkImage(Image.open(self.logo_path), size=(100, 100))

        self.logo = ctk.CTkLabel(self.logo_frame, image=self.logo_image, text="")
        self.logo.grid(row=0, column=0, padx=0, pady=5, sticky="n")

        # Logo Text (SafeKeep)
        self.logo_text = ctk.CTkLabel(
            self.logo_frame,
            text="SafeKeep",
            font=("Arial", 66, "bold"),
            text_color="#FFFFFF",
            fg_color="transparent",
        )
        self.logo_text.grid(row=0, column=1, padx=0, pady=15, sticky="n")

        # Add a check if the user already has a master password set and change the text accordingly
        # entry master password
        self.masterEntry = ctk.CTkEntry(
            self,
            width=400,
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
            show="*",
        )
        self.masterEntry.grid(row=0, column=1, padx=10, pady=(90, 8), sticky="")
        self.masterEntry.focus()

        # get show/hide password image
        self.showButtonImage = ctk.CTkImage(
            Image.open(
                SetupFuncs.get_hidden_show_password_image(self.masterEntry, None)
            ),
            size=(30, 30),
        )

        # frame for the show button
        self.showButtonFrame = ctk.CTkFrame(
            self,
            width=40,
            height=40,
            corner_radius=10,
            fg_color="transparent",
        )
        self.showButtonFrame.grid(
            row=0, column=1, padx=(465, 0), pady=(90, 8), sticky=""
        )

        # show/hide password button
        self.showButton = ctk.CTkButton(
            self.showButtonFrame,
            width=40,
            height=40,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#0f1215",
            text="",
            image=self.showButtonImage,
            command=lambda: SetupFuncs.get_hidden_show_password_image(
                self.masterEntry, self.showButton
            ),
        )
        self.showButton.grid(row=0, column=1, padx=(0, 0), pady=(5, 8), sticky="")

        # Login button
        self.login_button = ctk.CTkButton(
            self,
            width=100,
            height=35,
            corner_radius=10,
            fg_color="#1E3A8A",
            hover_color="#2E4FB2",
            text_color="#FFFFFF",
            text="Login",
            font=("Arial", 20, "bold"),
            command=lambda: MainFuncs.loginUser(
                self.masterEntry.get(), self, self.masterEntry, folder_path
            ),
        )
        self.login_button.grid(row=0, column=1, padx=0, pady=(235, 16), sticky="")

        # Bind enter to the login button
        self.bind("<Return>", lambda event: self.login_button.invoke())

        if not master_password_exists:
            SetupFuncs.master_password_not_set_actions(
                self.login_button, self.masterEntry, self, folder_path
            )

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", WindowsModule.on_close.__get__(self))


if __name__ == "__main__":
    loginWindow = LoginWindow()
    loginWindow.mainloop()

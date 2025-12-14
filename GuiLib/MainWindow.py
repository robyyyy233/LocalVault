import customtkinter as ctk

# For bitmap
from Resources import WindowsModule


from GuiLib.MainWindowFunctions import MainWindowFunctions as MainFunctions
from GuiLib.MainWindowFunctions import TabsFunctions as TabsFunctions
from NewTabTopLevel import SaveTab



class MainWindow(ctk.CTk):
    def __init__(self): #add the key here
        super().__init__()

        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(200, lambda: self.attributes("-topmost", False))

        delete_tab_mode: bool = False
        self.buttons: list = []

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

        #Create settings tab
        settings_path = MainFunctions.create_settings_json()
        TabsFunctions.add_default_tab(settings_path)

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

        self.left_frame.rowconfigure((0,1,2,3,4), weight=1)
        self.left_frame.rowconfigure(5, weight=1)


        self.TabsFrameLocation = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent", width=180
                                                        ,scrollbar_button_color="#151A22",
                                                        scrollbar_button_hover_color="#1D2F60")
        self.TabsFrameLocation.grid(row=0, column=0, rowspan=5, sticky="nsew")

        #render tabs
        self.buttons: list = TabsFunctions.render_tabs(self, settings_path, self.TabsFrameLocation)


        self.button_tabs = ctk.CTkFrame(self.left_frame, fg_color="transparent", width=180, height=60)
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
            command=lambda: TabsFunctions.show_top_level(self, SaveTab, self.TabsFrameLocation)
        )
        self.new_tab_button.grid(
            row=0, column=0, padx=(0,5), pady=(0,7 ), sticky="ew"
        )


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
            command=lambda b=self.delete_tab_button: setattr(
                self,
                "buttons",  # name of the attribute where you want to store the list
                TabsFunctions.delete_button_tab_configurate(
                    self, delete_tab_mode, b, self.TabsFrameLocation
                )
            )
        )
        self.delete_tab_button.grid(
            row=0, column=1, padx=(0,0), pady=(0, 7), sticky="ew"
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
            self.main_frame, fg_color="#1a1c1f", height=80
        )
        self.buttons_frame.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="new",
            padx=(10, 10),
            pady=(10, 10),
        )

        # Make the add a new password that creates a top level window

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
        self.password_list_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1c1f")
        self.password_list_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            rowspan=2,
            sticky="nsew",
            padx=(10, 10),
            pady=(10, 10),
        )

        # Remove this later
        self.passwordListLabel = ctk.CTkLabel(
            self.password_list_frame,
            text="Password List Frame",
            justify="center",
            font=("Arial", 20),
        )
        self.passwordListLabel.place(relx=0.5, rely=0.5, anchor="center")



        # Handle window close
        self.protocol("WM_DELETE_WINDOW", WindowsModule.on_close.__get__(self))


if __name__ == "__main__":
    mainWindow = MainWindow()
    mainWindow.mainloop()

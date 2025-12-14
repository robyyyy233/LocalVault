import customtkinter as ctk

from GuiLib.MainWindowFunctions import TabsFunctions as Tabs


class SaveTab(ctk.CTkToplevel):
    def __init__(self, master=None, tabsFrameLocation=None):
        ctk.CTkToplevel.__init__(self)

        tabs_frame = tabsFrameLocation

        self.configure(fg_color="#1a1c1f")
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("dark")

        self.title("SafeKeep - Save Tab")
        self.geometry("300x150")
        self.resizable(False, False)

        for x in range(3):
            self.grid_rowconfigure(x, weight=0)
            self.grid_columnconfigure(x, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew")

        self.main_frame.grid_rowconfigure((0,1,2,3), weight=0)
        self.main_frame.grid_columnconfigure((0,1,2), weight=1)

        self.tabs_label = ctk.CTkLabel(self.main_frame, text_color="#ffffff", text="Tabs name", font=("Arial", 22), anchor="w")
        self.tabs_label.grid(row=0, column=0, sticky="nw", padx=(10, 0), pady=(20, 0))

        self.entry_frame = ctk.CTkFrame(self.main_frame, fg_color="#0f1215", height=50)
        self.entry_frame.grid(row=0, column=0, columnspan=3, sticky="sew", pady=(48,7), padx=(10,10))

        for x in range(3):
            self.entry_frame.grid_rowconfigure(x, weight=1)
            self.entry_frame.grid_columnconfigure(x, weight=1)

        self.tabs_entry = ctk.CTkEntry(self.entry_frame, fg_color="#24272B", text_color="#ffffff", height=40,
                                          corner_radius=5, font=("Arial", 18), border_width=1,
                                          border_color="#3A3D41",)
        self.tabs_entry.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=(0,0), pady=(0,0))


        #Button Frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=50)
        self.buttons_frame.grid(row=3, column=0, columnspan=3, sticky="sew", padx=(0,0), pady=(5,5))

        self.cancel_button = ctk.CTkButton(self.buttons_frame, fg_color="#24272B", text_color="#ffffff",
                                        text="Cancel", corner_radius=10, width=100,height=40, font=("Arial", 20),
                                        border_width=1, border_color="#3A3D41",hover_color="#3A3D41",
                                        command=lambda: Tabs.destroy_window(self))
        self.cancel_button.grid(row=0, column=0, padx=(30,0), pady=(0,0), sticky="nsew")

        self.save_button = ctk.CTkButton(self.buttons_frame, fg_color="#24272B", text_color="#ffffff",
                                           text="Save", corner_radius=10, width=100, height=40, font=("Arial", 20),
                                           border_width=1, border_color="#3A3D41", hover_color="#3A3D41",
                                           command=lambda: Tabs.add_tab(master, self.tabs_entry, tabs_frame, self),)

        self.save_button.grid(row=0, column=1, padx=(35, 0), pady=(0, 0), sticky="nsew")

        self.bind("<Return>", lambda e: Tabs.add_tab(master, self.tabs_entry, tabs_frame, self))
        self.tabs_entry.focus_force()

        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(200, lambda: self.attributes("-topmost", False))


if __name__ == '__main__':
    TabWindow = SaveTab()
    TabWindow.mainloop()


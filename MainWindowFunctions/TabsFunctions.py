import json
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox



def destroy_window(self):
    self.destroy()

def show_top_level(self, TopLevel, tabsFrameLocation):
    # Check if we already created an instance
    if hasattr(self, "top_window") and self.top_window.winfo_exists():
        self.top_window.lift()
        self.top_window.focus_force()
        return

    # Create and store the instance
    self.top_window = TopLevel(self, tabsFrameLocation)




def render_tabs(self, settings_path: str, master) -> list:

    settings_path = Path(settings_path)

    #open JSON and get all tabs
    if settings_path.exists() and settings_path.is_file():
        with settings_path.open() as f:
            settings = json.load(f)
    else:
        print("Error trying to load settings file")


    #delete every button in scrollable frame
    for widget in master.winfo_children():
        widget.destroy()

    self.buttons = []

    for tab in settings['tabs']:

        self.button = ctk.CTkButton(master,fg_color="#1a1c1f", text_color="#ffffff",
                                        text=tab, corner_radius=6, width=170,
                                        height=40, font=("Arial", 20),
                                        hover_color="#31508D",)
        self.button.pack(pady=5, anchor="nw")

        self.button.configure(command=lambda b=self.button: show_password_filter( b))

        self.buttons.append(self.button)

    return self.buttons



#todo: show password based on filter
def show_password_filter(button: ctk.CTkButton) -> None:
    button_name = button.cget("text")
    print(f"{button_name} was pressed")



def delete_tab(btn: ctk.CTkButton, main_window, delete_state: bool, delete_button: ctk.CTkButton, settings_path, TabsFrameLocation) -> None:

    answer = messagebox.askyesno("Delete Tab","Are you sure you want to delete this tab?",)

    if answer:


        btn_list = getattr(main_window, "buttons", None)
        if isinstance(btn_list, list) and btn in btn_list:
            btn_list.remove(btn)

        # destroy the widget itself
        btn.destroy()

        name = btn.cget("text")
        print(f"{name} was deleted")

        #delete the button from the JSON
        with open(settings_path, "r+") as file:
            settings = json.load(file)
            tabs_list = settings.get("tabs")
            tabs_list.remove(name)
            settings["tabs"] = tabs_list

            file.seek(0)
            file.truncate()
            json.dump(settings, file, indent=4)

        delete_button_tab_configurate(main_window, delete_state, delete_button, TabsFrameLocation)

        #todo: also add so it deletes from the passwords the tabs that we  deleted
        #todo: don t delete the all tab from passwords






def delete_button_tab_configurate(main_window,
                                  delete_state: bool,
                                  delete_button: ctk.CTkButton,
                                  TabsFrameLocation) -> list:

    file_path = Path.home() / "Documents" / "PasswordManager" / "Settings.json"

    # always work with the current list (perhaps empty)
    buttons = getattr(main_window, "buttons", []) or []

    # toggle state
    delete_state = not delete_state

    if delete_state:
        # ENTERING delete mode
        delete_button.configure(
            text="Cancel",
            command=lambda: delete_button_tab_configurate(
                main_window, delete_state, delete_button, TabsFrameLocation
            )
        )

        for button in buttons:
            button.configure(
                fg_color="#B43232",
                hover_color="#C84141",
                command=lambda b=button: delete_tab(
                    b, main_window, delete_state, delete_button, file_path, TabsFrameLocation
                )
            )
        return None

    else:
        # EXITING delete mode
        delete_button.configure(
            text="Delete Tab",
            command=lambda: delete_button_tab_configurate(
                main_window, delete_state, delete_button, TabsFrameLocation
            )
        )

        # if buttons somehow ended up None, re-render first
        if not isinstance(buttons, list):
            buttons = render_tabs(main_window, str(file_path), TabsFrameLocation)
        else:
            # restore normal look & behavior for existing buttons
            for button in buttons:
                button.configure(
                    fg_color="#1a1c1f",
                    hover_color="#31508D",
                    command=lambda b=button: show_password_filter(b)
                )

            # then re-render from JSON to refresh layout and main_window.buttons
            buttons = render_tabs(main_window, str(file_path), TabsFrameLocation)

        return buttons




#Adds the default tab
def add_default_tab(path: str) -> None:
    settings_path = Path(path)

    with open(settings_path, "r+") as file:

        try:
            settings_content = json.load(file)
        except json.JSONDecodeError:
            settings_content = {"tabs": []}

        tabs_hold = []
        tabs_value = settings_content.get("tabs")

        if isinstance(tabs_value, list):
            for tab in tabs_value:
                if tab != "All":
                    tabs_hold.append(tab)
        elif tabs_value is not None:
            tabs_hold.append(tabs_value)

        settings_content["tabs"] = []
        settings_content["tabs"].insert(0, "All")
        settings_content["tabs"].extend(tabs_hold)

        file.seek(0)
        file.truncate()
        json.dump(settings_content, file, indent=4)



#Adds the tab
def add_tab(self,  entry: ctk.CTkEntry, tabs_frame, topLevel: ctk.CTkToplevel) -> None:
    file_name: str = "Settings.json"
    file_path = Path.home() / "Documents" / "PasswordManager" / file_name

    settings_path = Path(file_path)
    tabs_name = entry.get()


    if not settings_path.exists() or not settings_path.is_file():
        messagebox.showerror("Error", "Settings file not found\nRestart application")

    #if name with that tab already exists
    with open(file_path, "r") as file_read:

        settings = json.load(file_read)

        for tab in settings["tabs"]:

            #check if tab already exist
            if tab.strip().lower() == tabs_name.strip().lower():
                messagebox.showerror("Error", "Tab name already exists")
                return


    with open(file_path, "w") as file_write:
        tabs_name = tabs_name.capitalize()

        settings["tabs"].append(tabs_name)
        json.dump(settings, file_write, indent=4)


    entry.delete(0, "end")
    topLevel.destroy()

    render_tabs(self, str(settings_path), master=tabs_frame)





if __name__ == "__main__":
    pass

import tkinter as tk
import customtkinter as ctk
import webbrowser
from tkinter import messagebox
from urllib.parse import urlparse

from GuiLib.VaultFunctions import VaultUnlock


def is_url(text: str) -> bool:
    try:
        result = urlparse(text)
        return result.scheme in ("http", "https")
    except Exception:
        return False


def format_site_display(site: str) -> str:
    if is_url(site):
        host = urlparse(site).netloc
        if host.startswith("www."):
            host = host[4:]
        parts = host.split(".")
        parts[0] = parts[0].capitalize()
        return ".".join(parts)
    else:
        parts = site.split(".")
        parts[0] = parts[0].capitalize()
        return ".".join(parts)


def render_passwords(master):
    for widget in master.password_list_frame.winfo_children():
        widget.destroy()

    passwords = master.vault_data.get("Passwords", [])

    current_tab = getattr(master, "current_tab", "All")
    if current_tab == "Unassigned":
        passwords = [p for p in passwords if not p.get("tab")]
    elif current_tab and current_tab != "All":
        passwords = [p for p in passwords if p.get("tab") == current_tab]

    if not passwords:
        msg = "No unassigned passwords." if current_tab == "Unassigned" else "No passwords saved yet."
        ctk.CTkLabel(
            master.password_list_frame,
            text=msg,
            text_color="#555a61",
            font=("Arial", 16),
        ).pack(expand=True)
        return

    for entry in passwords:
        _create_password_card(master.password_list_frame, entry, master)


def _create_password_card(parent, entry: dict, master):
    card = ctk.CTkFrame(
        parent, fg_color="#1A1C1F",
        corner_radius=8,
        border_width=1, border_color="#2a2d32",
    )
    card.pack(fill="x", padx=10, pady=5)
    card.grid_columnconfigure(0, weight=1)
    card.grid_columnconfigure(1, weight=0)
    card.grid_columnconfigure(2, weight=0)
    card.grid_columnconfigure(3, weight=0)

    raw_site = entry.get("site", "")
    display_name = format_site_display(raw_site)

    site_label = ctk.CTkLabel(
        card, text=display_name, text_color="#ffffff",
        font=("Arial", 20, "bold"), anchor="w",
        cursor="hand2" if is_url(raw_site) else "",
    )
    if is_url(raw_site):
        site_label.bind("<Button-1>", lambda e, url=raw_site: webbrowser.open(url))
    site_label.grid(row=0, column=0, sticky="ew", padx=(14, 5), pady=(13, 13))

    # Detail frame — hidden by default, must exist before show_btn command is set
    detail_frame = ctk.CTkFrame(card, fg_color="#141618", corner_radius=0)
    detail_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(8, 8), pady=(0, 10))
    detail_frame.grid_remove()
    _build_detail_frame(detail_frame, entry, master)

    # Copy ▼
    copy_btn = ctk.CTkButton(
        card, text="Copy ▼", width=105, height=34,
        fg_color="#24272B", text_color="#ffffff",
        hover_color="#3A3D41", corner_radius=6,
        border_width=1, border_color="#3A3D41",
        font=("Arial", 14), command=None,
    )
    copy_btn.configure(command=lambda b=copy_btn, e=entry: _show_copy_popup(master, e, b))
    copy_btn.grid(row=0, column=1, padx=(0, 5), pady=(13, 13))

    # Show / Hide
    show_btn = ctk.CTkButton(
        card, text="Show", width=72, height=34,
        fg_color="#24272B", text_color="#ffffff",
        hover_color="#3A3D41", corner_radius=6,
        border_width=1, border_color="#3A3D41",
        font=("Arial", 14), command=None,
    )
    show_btn.configure(command=lambda df=detail_frame, sb=show_btn: _toggle_details(df, sb))
    show_btn.grid(row=0, column=2, padx=(0, 5), pady=(13, 13))

    # Delete
    del_btn = ctk.CTkButton(
        card, text="🗑", width=42, height=34,
        fg_color="#6B1C1C", text_color="#ffa198",
        hover_color="#8B2020", corner_radius=6,
        border_width=1, border_color="#8B2020",
        font=("Arial", 14),
        command=lambda eid=entry.get("id"): _delete_entry(master, eid),
    )
    del_btn.grid(row=0, column=3, padx=(0, 10), pady=(13, 13))


def _build_detail_frame(frame, entry: dict, master):
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=0)

    row_idx = 0
    for label, value in [
        ("Email",    entry.get("email", "")),
        ("Password", entry.get("password", "")),
    ]:
        if not value:
            continue
        ctk.CTkLabel(
            frame, text=f"{label}:", text_color="#9a9a9a",
            font=("Arial", 14), anchor="w", width=72,
        ).grid(row=row_idx, column=0, sticky="w", padx=(10, 4), pady=(5, 5))
        ctk.CTkLabel(
            frame, text=value, text_color="#ffffff",
            font=("Arial", 14), anchor="w",
        ).grid(row=row_idx, column=1, sticky="ew", columnspan=2, padx=(0, 10), pady=(5, 5))
        row_idx += 1

    # Tab row — always shown with a move control
    ctk.CTkLabel(
        frame, text="Tab:", text_color="#9a9a9a",
        font=("Arial", 14), anchor="w", width=72,
    ).grid(row=row_idx, column=0, sticky="w", padx=(10, 4), pady=(5, 5))

    all_tabs = master.vault_data.get("Tabs", [])
    tabs = [t for t in all_tabs if t != "All"] or [entry.get("tab", "")]
    current = entry.get("tab", tabs[0] if tabs else "")
    tab_var = ctk.StringVar(value=current)

    ctk.CTkOptionMenu(
        frame, values=tabs, variable=tab_var,
        fg_color="#24272B", text_color="#ffffff",
        button_color="#3A3D41", button_hover_color="#4A4D51",
        dropdown_fg_color="#24272B", dropdown_text_color="#ffffff",
        dropdown_hover_color="#3A3D41",
        font=("Arial", 13), height=28, corner_radius=4,
    ).grid(row=row_idx, column=1, sticky="w", padx=(0, 5), pady=(5, 5))

    ctk.CTkButton(
        frame, text="Move", width=60, height=28,
        fg_color="#1C2F63", text_color="#ffffff",
        hover_color="#233A78", corner_radius=4,
        font=("Arial", 13),
        command=lambda tv=tab_var, eid=entry.get("id"): _change_tab(master, eid, tv.get()),
    ).grid(row=row_idx, column=2, sticky="w", padx=(0, 10), pady=(5, 5))
    row_idx += 1

    notes = entry.get("notes", "")
    if notes:
        ctk.CTkLabel(
            frame, text="Notes:", text_color="#9a9a9a",
            font=("Arial", 14), anchor="w", width=72,
        ).grid(row=row_idx, column=0, sticky="w", padx=(10, 4), pady=(5, 5))
        ctk.CTkLabel(
            frame, text=notes, text_color="#ffffff",
            font=("Arial", 14), anchor="w",
        ).grid(row=row_idx, column=1, sticky="ew", columnspan=2, padx=(0, 10), pady=(5, 5))


def _toggle_details(detail_frame, show_btn):
    if detail_frame.winfo_viewable():
        detail_frame.grid_remove()
        show_btn.configure(text="Show")
    else:
        detail_frame.grid()
        show_btn.configure(text="Hide")


def _change_tab(master, entry_id: str, new_tab: str):
    for p in master.vault_data.get("Passwords", []):
        if p.get("id") == entry_id:
            p["tab"] = new_tab
            break

    encrypted = VaultUnlock.encrypt(master.vault_key, str(master.vault_data).encode("utf-8"))
    VaultUnlock.write_enc_data(encrypted)
    master.vault_data = VaultUnlock.decrypt(master.vault_key)

    # If we just cleared the last unassigned password, leave Unassigned view
    if getattr(master, "current_tab", "All") == "Unassigned":
        still_unassigned = [p for p in master.vault_data.get("Passwords", []) if not p.get("tab")]
        if not still_unassigned:
            master.current_tab = "All"
            if hasattr(master, "current_tab_label"):
                master.current_tab_label.configure(text="All")

    from GuiLib.MainWindowFunctions import TabsFunctions
    TabsFunctions.render_tabs(master)
    render_passwords(master)


def _show_copy_popup(master, entry: dict, button):
    popup = tk.Toplevel(master)
    popup.overrideredirect(True)
    popup.configure(bg="#1A1C1F")

    def copy_and_close(text):
        _copy_to_clipboard(master, text)
        if popup.winfo_exists():
            popup.destroy()

    ctk.CTkButton(
        popup, text="Copy Email", height=42,
        fg_color="#1A1C1F", text_color="#ffffff",
        hover_color="#3A3D41", corner_radius=0,
        font=("Arial", 15),
        command=lambda: copy_and_close(entry.get("email", "")),
    ).pack(fill="x")

    ctk.CTkButton(
        popup, text="Copy Password", height=42,
        fg_color="#1A1C1F", text_color="#ffffff",
        hover_color="#3A3D41", corner_radius=0,
        font=("Arial", 15),
        command=lambda: copy_and_close(entry.get("password", "")),
    ).pack(fill="x")

    popup.update_idletasks()
    h = sum(w.winfo_reqheight() for w in popup.winfo_children())
    w = max(w.winfo_reqwidth() for w in popup.winfo_children()) + 20
    x = button.winfo_rootx()
    y = button.winfo_rooty() + button.winfo_height() + 2
    popup.geometry(f"{w}x{h}+{x}+{y}")

    # grab_set routes outside clicks to popup
    # only destroy when event.widget IS popup itself — not when it propagated up from a child button
    popup.grab_set()
    popup.bind(
        "<Button-1>",
        lambda e: popup.destroy() if (popup.winfo_exists() and e.widget is popup) else None,
    )


def _copy_to_clipboard(master, text: str):
    master.clipboard_clear()
    master.clipboard_append(text)


def _delete_entry(master, entry_id: str):
    confirm = messagebox.askyesno("Delete", "Delete this password?")
    if not confirm:
        return

    master.vault_data["Passwords"] = [
        p for p in master.vault_data.get("Passwords", [])
        if p.get("id") != entry_id
    ]

    encrypted = VaultUnlock.encrypt(master.vault_key, str(master.vault_data).encode("utf-8"))
    VaultUnlock.write_enc_data(encrypted)
    master.vault_data = VaultUnlock.decrypt(master.vault_key)

    render_passwords(master)

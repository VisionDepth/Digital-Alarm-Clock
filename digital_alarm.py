import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import ctypes
import datetime as dt
import winsound
import os

root = tk.Tk()
root.title("Digital Clock")
root.geometry("400x275")
root.configure(bg="black")
root.resizable(True, True)

alarm_time = None
alarm_active = False
use_24h = False
current_theme = "Default"
current_theme_bg = "black"
current_theme_fg = "#00ff2b"
flash_on = False 

sound_path = os.path.join("assets", "alarm_sound.wav")

ctypes.windll.gdi32.AddFontResourceW(os.path.abspath("assets/Digital-7.ttf"))
digital_font = tkfont.Font(family="Digital-7", size=64)

button_style = {
    "fg": "#00ff2b",
    "bg": "black",
    "activeforeground": "#00ff2b",
    "activebackground": "#003300",
    "borderwidth": 2,
    "highlightthickness": 0,
}

themes = {
    "Default": {"bg": "#f5f5dc", "fg": "#2e2e2e", "highlight": "#dcd4aa"},
    "Matrix": {"bg": "black", "fg": "#00ff2b", "highlight": "#003300"},
    "Retro Blue": {"bg": "#001a33", "fg": "#55ccff", "highlight": "#00334d"},
    "Red Alert": {"bg": "#330000", "fg": "#ff4444", "highlight": "#660000"},
    "Neon Purple": {"bg": "#1a0033", "fg": "#c77dff", "highlight": "#5a0099"},
    "Synthwave": {"bg": "#240046", "fg": "#ff78f0", "highlight": "#5900b3"},
    "Terminal Green": {"bg": "#002b00", "fg": "#16ff00", "highlight": "#004d00"},
    "Deep Ocean": {"bg": "#001a26", "fg": "#00eaff", "highlight": "#004d66"},
    "Amber Glow": {"bg": "#332000", "fg": "#ffb400", "highlight": "#664000"},
}

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Alarm.TCombobox",
    fieldbackground="black",
    background="black",
    foreground="#00ff2b",
    arrowcolor="#00ff2b",
)

style.map(
    "Alarm.TCombobox",
    fieldbackground=[("readonly", "black")],
    foreground=[("readonly", "#00ff2b")],
)

def apply_theme(theme_name: str):
    global current_theme, current_theme_bg, current_theme_fg
    current_theme = theme_name

    theme = themes.get(theme_name)
    if not theme:
        return

    bg = theme["bg"]
    fg = theme["fg"]
    highlight = theme["highlight"]

    current_theme_bg = bg
    current_theme_fg = fg

    root.configure(bg=bg)

    for widget in [date_label, time_label, ampm_label, status_label]:
        widget.config(bg=bg, fg=fg)

    time_frame.config(bg=bg)
    alarm_frame.config(bg=bg)
    buttons_frame.config(bg=bg)
    top_controls.config(bg=bg)

    for widget in [hour_label, minute_label]:
        widget.config(bg=bg, fg=fg)

    for entry in [hour_entry, minute_entry]:
        entry.config(bg=bg, fg=fg, insertbackground=fg)
        entry.config(highlightbackground=highlight, highlightcolor=highlight)

    for button in [
        set_alarm_button,
        cancel_button,
        dismiss_button,
        snooze_button,
        use_24h_button
        ]:
        button.config(bg=bg, fg=fg, activebackground=highlight, activeforeground=fg)

    status_label.config(fg=fg)

    style.configure(
        "Alarm.TCombobox",
        fieldbackground=bg,
        background=bg,
        foreground=fg,
        arrowcolor=fg,
        bordercolor=bg,
    )
    style.map(
        "Alarm.TCombobox",
        fieldbackground=[("readonly", bg)],
        foreground=[("readonly", fg)],
        selectbackground=[("readonly", bg)],
        selectforeground=[("readonly", fg)],
    )


def set_alarm(event=None):
    global alarm_time

    hour_str = hour_entry.get().strip()
    minute_str = minute_entry.get().strip()

    # minute validation (shared)
    if not minute_str.isdigit() or not (0 <= int(minute_str) <= 59):
        status_label.config(text="Invalid minute (00-59)", fg="red")
        return

    if use_24h:
        # 24-hour INPUT mode: hour must be 0–23
        if not hour_str.isdigit() or not (0 <= int(hour_str) <= 23):
            status_label.config(text="Invalid hour (0-23 in 24h mode)", fg="red")
            return

        h24 = int(hour_str)

        # convert 24h → 12h + AM/PM for internal alarm_time
        if h24 == 0:
            h12 = 12
            am_pm = "AM"
        elif 1 <= h24 <= 11:
            h12 = h24
            am_pm = "AM"
        elif h24 == 12:
            h12 = 12
            am_pm = "PM"
        else:  # 13–23
            h12 = h24 - 12
            am_pm = "PM"

        minute_str = minute_str.zfill(2)
        alarm_time = f"{h12}:{minute_str} {am_pm}"

        # show the user the 24h time they typed
        status_label.config(
            text=f"Alarm set for: {h24:02d}:{minute_str}",
            fg=current_theme_fg,
        )

    else:
        # 12-hour INPUT mode: 1–12 + AM/PM from combobox
        am_pm = am_pm_entry.get().strip()

        if not hour_str.isdigit() or not (1 <= int(hour_str) <= 12):
            status_label.config(text="Invalid hour (1-12)", fg="red")
            return

        if am_pm not in ["AM", "PM"]:
            status_label.config(text="Select AM or PM", fg="red")
            return

        minute_str = minute_str.zfill(2)
        alarm_time = f"{int(hour_str)}:{minute_str} {am_pm}"

        status_label.config(
            text=f"Alarm set for: {alarm_time}",
            fg=current_theme_fg,
        )

    # common button states
    cancel_button.config(state="normal")
    dismiss_button.config(state="disabled")
    snooze_button.config(state="disabled")


def flash_alarm():
    if not alarm_active:
        return

    flash_bg = "red"
    restore_bg = current_theme_bg

    current_color = root.cget("bg")
    new_bg = flash_bg if current_color != flash_bg else restore_bg

    for widget in flashing_widgets:
        try:
            widget.configure(bg=new_bg)
        except Exception:
            pass

    root.configure(bg=new_bg)

    style.configure(
        "Alarm.TCombobox",
        fieldbackground=new_bg,
        background=new_bg,
    )
    
    style.map(
        "Alarm.TCombobox",
        fieldbackground=[("readonly", new_bg)],
        selectbackground=[("readonly", new_bg)],
        selectforeground=[("readonly", current_theme_fg)],
        foreground=[("readonly", current_theme_fg)],
    )

    root.after(500, flash_alarm)


def _restore_theme_after_alarm():
    apply_theme(current_theme)

def dismiss_alarm(event=None):
    global alarm_active, alarm_time
    alarm_active = False
    alarm_time = None

    winsound.PlaySound(None, winsound.SND_PURGE)
    status_label.config(text="Alarm dismissed", fg=current_theme_fg)
    root.after(5000, lambda: status_label.config(text=""))

    _restore_theme_after_alarm()

    cancel_button.config(state="disabled")
    dismiss_button.config(state="disabled")
    snooze_button.config(state="disabled")


def cancel_alarm(event=None):
    global alarm_time, alarm_active
    alarm_time = None
    alarm_active = False

    winsound.PlaySound(None, winsound.SND_PURGE)
    status_label.config(text="Alarm cancelled", fg=current_theme_fg)
    root.after(5000, lambda: status_label.config(text=""))

    _restore_theme_after_alarm()

    cancel_button.config(state="disabled")
    dismiss_button.config(state="disabled")
    snooze_button.config(state="disabled")


def snooze_alarm(event=None):
    global alarm_active, alarm_time
    alarm_active = False

    winsound.PlaySound(None, winsound.SND_PURGE)

    now = dt.datetime.now()
    new_time = now + dt.timedelta(minutes=5)
    alarm_time = new_time.strftime("%I:%M %p").lstrip("0")

    status_label.config(text=f"Snoozed until: {alarm_time}", fg=current_theme_fg)
    root.after(5000, lambda: status_label.config(text=""))

    _restore_theme_after_alarm()

    cancel_button.config(state="normal")
    dismiss_button.config(state="disabled")
    snooze_button.config(state="disabled")


def update_time():
    global alarm_active

    now = dt.datetime.now()
    date_label.config(text=now.strftime("%A, %B %d, %Y"))
    
    if use_24h:
        clock_part = now.strftime("%H:%M:%S")
        ampm_part = ""
        time_label.config(text=clock_part)
    else:
        full_time = now.strftime("%I:%M:%S %p")
        clock_part = full_time[:-3]
        ampm_part = full_time[-2:]
        time_label.config(text=clock_part.lstrip("0"))

    ampm_label.config(text=ampm_part)

    current_str = now.strftime("%I:%M %p").lstrip("0")

    if alarm_time == current_str and not alarm_active:
        alarm_active = True
        flash_alarm()
        winsound.PlaySound(
            sound_path,
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP,
        )
        cancel_button.config(state="disabled")
        dismiss_button.config(state="normal")
        snooze_button.config(state="normal")

    root.after(1000, update_time)


def on_theme_change(event=None):
    apply_theme(theme_var.get())


def on_focus_in(event):
    event.widget.config(highlightbackground=current_theme_fg, highlightcolor=current_theme_fg)


def on_focus_out(event):
    event.widget.config(highlightbackground=current_theme_bg, highlightcolor=current_theme_bg)

def toggle_24h():
    global use_24h
    use_24h = not use_24h

    if use_24h:
        am_pm_entry.config(state="disabled")
        use_24h_button.config(text="Use 12 hour")
    else:
        am_pm_entry.config(state="readonly")
        use_24h_button.config(text="Use 24 hour")


date_label = tk.Label(root, font=("Arial", 18), foreground="#00ff2b", background="black")
date_label.pack(pady=(5, 0))

time_frame = tk.Frame(root, bg="black")
time_frame.pack(pady=(0, 10))

time_label = tk.Label(
    time_frame,
    font=("Digital-7", 64),
    foreground="#00ff2b",
    background="black"
)
time_label.pack(side="left")

ampm_label = tk.Label(
    time_frame,
    font=("Digital-7", 24),
    foreground="#00ff2b",
    background="black"
)
ampm_label.pack(side="left", padx=(5, 0))

status_label = tk.Label(
    root, text="",
    font=("Arial", 12),
    fg="#00ff2b",
    bg="black"
)
status_label.pack(pady=(5, 0))

top_controls = tk.Frame(root, bg="black")  # bg will get themed later
top_controls.pack(pady=(0, 10))


theme_var = tk.StringVar(value="Default")
theme_dropdown = ttk.Combobox(
    top_controls,
    textvariable=theme_var,
    values=list(themes.keys()),
    width=12,
    state="readonly",
    style="Alarm.TCombobox",
)
theme_dropdown.pack(side="left", padx=5)
theme_dropdown.bind("<<ComboboxSelected>>", on_theme_change)

use_24h_button= tk.Button(
    top_controls,
    text="Use 24 hour",
    command=toggle_24h,
    **button_style
)
use_24h_button.pack(side="left", padx=5)    

alarm_frame = tk.Frame(root, bg="black")
alarm_frame.pack(pady=(0, 10))

hour_label = tk.Label(
    alarm_frame, text="Hour", font=("Arial", 10), foreground="#00ff2b", background="black"
)
hour_label.pack(side="left", padx=2)

hour_entry = tk.Entry(alarm_frame, width=2, bg="black", fg="#00ff2b", bd=2, highlightthickness=0)
hour_entry.config(insertbackground="#00ff2b")
hour_entry.pack(side="left", padx=2)

minute_label = tk.Label(
    alarm_frame, text="Min", font=("Arial", 10), foreground="#00ff2b", background="black"
)
minute_label.pack(side="left", padx=2)

minute_entry = tk.Entry(alarm_frame, width=2, bg="black", fg="#00ff2b")
minute_entry.config(insertbackground="#00ff2b")
minute_entry.pack(side="left", padx=2)

am_pm_entry = ttk.Combobox(
    alarm_frame,
    values=["AM", "PM"],
    width=3,
    state="readonly",
    style="Alarm.TCombobox",
)
am_pm_entry.pack(side="left", padx=2)

buttons_frame = tk.Frame(root, bg="black")
buttons_frame.pack()

set_alarm_button = tk.Button(buttons_frame, text="Set Alarm", command=set_alarm, **button_style)
set_alarm_button.pack(side="left", padx=10)

cancel_button = tk.Button(buttons_frame, text="Cancel Alarm", command=cancel_alarm, **button_style)
cancel_button.pack(side="left", padx=10)
cancel_button.config(state="disabled")

dismiss_button = tk.Button(
    buttons_frame, text="Dismiss Alarm", command=dismiss_alarm, **button_style
)
dismiss_button.pack(side="left", padx=10)
dismiss_button.config(state="disabled")

snooze_button = tk.Button(buttons_frame, text="Snooze", command=snooze_alarm, **button_style)
snooze_button.pack(side="left", padx=10)
snooze_button.config(state="disabled")

hour_entry.bind("<FocusIn>", on_focus_in)
hour_entry.bind("<FocusOut>", on_focus_out)
minute_entry.bind("<FocusIn>", on_focus_in)
minute_entry.bind("<FocusOut>", on_focus_out)

root.bind("<Return>", set_alarm)
root.bind("<Escape>", cancel_alarm)
root.bind("<Control-d>", dismiss_alarm)
root.bind("<Control-s>", snooze_alarm)

flashing_widgets = [
    date_label,
    time_frame,
    time_label,
    ampm_label,
    status_label,
    top_controls,
    alarm_frame,
    buttons_frame,
    hour_label,
    minute_label,
    hour_entry,
    minute_entry,
    theme_dropdown,
    am_pm_entry,
    set_alarm_button,
    cancel_button,
    dismiss_button,
    snooze_button,
    use_24h_button,
]


apply_theme("Default")
update_time()
root.mainloop()

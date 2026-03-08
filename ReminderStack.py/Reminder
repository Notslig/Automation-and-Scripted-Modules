import tkinter as tk
import time
import sqlite3

conn = sqlite3.connect("reminders.db")
cursor = conn.cursor()
#cursor.execute("""DROP TABLE IF EXISTS reminders""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders(
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    time TEXT
)
""")

selected_id = None
selected_card = None


root = tk.Tk()
root.title("Reminder System")
root.state("zoomed")
root.configure(bg="#a79a9a")

root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)





# LEFT PANEL
left_panel = tk.Frame(root, bg="#f5f5f5")
left_panel.grid(row=0, column=0, sticky="nsew")
canvas = tk.Canvas(left_panel, bg="#f5f5f5", highlightthickness=0)
scrollbar = tk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def resize_canvas(event):
    canvas.itemconfig(canvas_window, width=event.width)

canvas.bind("<Configure>", resize_canvas)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# RIGHT PANEL
right_panel = tk.Frame(root, bg="#e2e2e2")
right_panel.grid(row=0, column=1, sticky="nsew")

# Inside right panel
control_frame = tk.Frame(right_panel, bg="#e2e2e2")
control_frame.pack(fill="x", padx=15, pady=10)

list_frame = tk.Frame(right_panel, bg="white", height=600)
list_frame.pack(fill="x", padx=15, pady=20)
list_frame.pack_propagate(False)

list_title = tk.Label(
    list_frame,
    text="Current Reminder",
    font=("Segoe UI", 14, "bold"),
    bg="white"
)
list_title.pack(anchor="w", padx=10, pady=(10,5))



clock_frame = tk.Frame(right_panel, bg="#e2e2e2", height=300)
clock_frame.pack(fill="both", expand=True, padx=20, pady=20)

clock_label = tk.Label(
    clock_frame,
    font=("Segoe UI", 36, "bold"),
    bg="#e2e2e2"
)

clock_label.pack(side="bottom", pady=30)

def on_enter(e):
    card = e.widget
    while not isinstance(card, tk.Frame):
        card = card.master
    card.configure(bg="#eaf4ff")
    for child in card.winfo_children():
        child.configure(bg="#eaf4ff")

def on_leave(e):
    card = e.widget
    while not isinstance(card, tk.Frame):
        card = card.master
    card.configure(bg="white")
    for child in card.winfo_children():
        child.configure(bg="white")

def get_remaining_time(time_set):

    try:
        now = time.localtime()

        current_minutes = now.tm_hour * 60 + now.tm_min

        hour, minute = map(int, time_set.split(":"))
        reminder_minutes = hour * 60 + minute

        diff = reminder_minutes - current_minutes

        if diff <= 0:
            return "Expired"

        hours = diff // 60
        minutes = diff % 60

        return f"{hours}h {minutes}m"

    except:
        return "--"

def create_reminder(parent, reminder_id, title, time_set, description=""):
    card = tk.Frame(
        parent,
        bg="white",
        height=130,
        relief="ridge",
        bd=1,
        highlightbackground="#d0d0d0",
        highlightthickness=1
    )

    card.pack(fill="x", padx=20, pady=12)
    card.pack_propagate(False)

    # LEFT SIDE CONTENT
    content = tk.Frame(card, bg="white")
    content.pack(side="left", padx=20, pady=10, anchor="w")

    # TITLE
    title_label = tk.Label(
        content,
        text=title,
        font=("Segoe UI", 16, "bold"),
        bg="white"
    )
    title_label.pack(anchor="w")

    # DESCRIPTION
    desc_label = tk.Label(
        content,
        text=description,
        font=("Segoe UI", 10),
        fg="#777777",
        bg="white"
    )
    desc_label.pack(anchor="w")

    # RIGHT SIDE TIME AREA
    time_area = tk.Frame(card, bg="white")
    time_area.pack(side="right", padx=20, pady=10)

    # TIME LEFT
    time_left = tk.Label(
        time_area,
        text=get_remaining_time(time_set),
        font=("Segoe UI", 14, "bold"),
        bg="white"
    )
    time_left.pack()

    # SET TIME
    set_time = tk.Label(
        time_area,
        text=time_set,
        font=("Segoe UI", 10),
        fg="#555555",
        bg="white"
    )
    set_time.pack(pady=(5,0))

    # Hover bindings
    for widget in [card, title_label, desc_label, time_left, set_time]:
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        
    
    def select_card(event):
        
        global selected_card, selected_id

        if selected_card:
            selected_card.configure(highlightbackground="#d0d0d0")

        selected_card = card
        selected_id = reminder_id

        card.configure(highlightbackground="#0078D7")
    
    card.bind("<Button-1>", select_card)

    return card



def add_reminder():

    popup = tk.Toplevel(root)
    popup.title("New Reminder")
    popup.geometry("350x300")
    popup.configure(bg="white")

    tk.Label(popup, text="Title").pack(pady=5)
    title_entry = tk.Entry(popup, width=30)
    title_entry.pack()

    tk.Label(popup, text="Description").pack(pady=5)
    desc_entry = tk.Entry(popup, width=30)
    desc_entry.pack()

    tk.Label(popup, text="Time (HH:MM) 24-hr format").pack(pady=5)
    time_entry = tk.Entry(popup, width=30)
    time_entry.pack()

    def save_reminder():

        title = title_entry.get()
        description = desc_entry.get()
        time_set = time_entry.get()
        
        if not title or not time_set:
            return

        cursor.execute(
            "INSERT INTO reminders (title, description, time) VALUES (?, ?, ?)",
            (title, description, time_set)
        )

        
        conn.commit()

        popup.destroy()

        load_reminders()

    tk.Button(
        popup,
        text="Save Reminder",
        bg="#28a745",
        fg="white",
        command=save_reminder
    ).pack(pady=20)


def create_list_row(parent, title, time_set):

    row = tk.Frame(parent, bg="white")
    row.pack(fill="x", padx=10, pady=5)

    title_label = tk.Label(
        row,
        text=title,
        font=("Segoe UI", 11),
        bg="white"
    )
    title_label.pack(side="left")

    time_label = tk.Label(
        row,
        text=time_set,
        font=("Segoe UI", 10, "bold"),
        fg="#444444",
        bg="white"
    )
    time_label.pack(side="right")

    divider = tk.Frame(parent, height=1, bg="#e6e6e6")
    divider.pack(fill="x", padx=10)
    
    
def load_reminders():

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for widget in list_frame.winfo_children():
        widget.destroy()

    list_title = tk.Label(
        list_frame,
        text="Upcoming Reminders",
        font=("Segoe UI", 14, "bold"),
        bg="white"
)
    list_title.pack(anchor="w", padx=10, pady=(10,5))

    cursor.execute("SELECT id, title, description, time FROM reminders")

    for row in cursor.fetchall():

        reminder_id, title, description, time_set = row

        create_reminder(scrollable_frame, reminder_id, title, time_set, description)

        create_list_row(list_frame, title, time_set)
    

add_btn = tk.Button(
    control_frame,
    text="Add Reminder",
    bg="#28a745",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    width=18,
    height=2,
    command=add_reminder
)

#add_btn.pack(anchor="w", padx=20, pady=15)
add_btn.pack(fill="x", pady=10)

def remove_reminder():

    global selected_id, selected_card

    if selected_id is None:
        return

    cursor.execute("DELETE FROM reminders WHERE id=?", (selected_id,))
    conn.commit()

    selected_id = None
    selected_card = None

    load_reminders()
    
    
remove_btn = tk.Button(
    control_frame,
    text="Remove Reminder",
    bg="#dc3545",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    width=18,
    height=2,
    command=lambda: remove_reminder()
)

remove_btn.pack(fill="x", pady=10)



def update_clock():
    clock_label.config(text=time.strftime("%H:%M:%S"))
    root.after(1000, update_clock)

update_clock()

def refresh_reminder_times():
    load_reminders()
    root.after(60000, refresh_reminder_times)



def on_close():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)


refresh_reminder_times()
load_reminders()
root.mainloop()
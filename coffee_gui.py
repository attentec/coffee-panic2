import tkinter as tk
import time, datetime
from scale import Scale
from api_service import ApiService

USE_FULLSCREEN = False

PUBLISH_WEIGHT_INTERVAL_MS = 20_000 # 20 seconds
READ_WEIGHT_INTERVAL_MS = 1_000 # 1 second
KEEP_ALIVE_INTERVAL_MS = 120_000 # 120 seconds

def exit():
    root.destroy()

def retry():
    global in_error_state
    if in_error_state:
        scale_state_variable.set("Ansluter till våg...")
        begin_reading()

def set_error_state(new_state):
    global in_error_state
    in_error_state = new_state
    if in_error_state:
        scale_state_variable.set("Tappat anslutning till våg")
        btn_retry.place(x=48,y=90)
    else:
        btn_retry.place_forget()

def begin_reading():
    global dymo_scale
    try:
        dymo_scale = Scale(external_keep_alive=True)
        root.after(READ_WEIGHT_INTERVAL_MS, read_scale)
        root.after(KEEP_ALIVE_INTERVAL_MS, keep_scale_alive)
        root.after(PUBLISH_WEIGHT_INTERVAL_MS, publish_weight)
        set_error_state(False)
    except:
        set_error_state(True)

def read_scale():
    global scale_state, in_error_state
    if not in_error_state:
        try:
            weight = dymo_scale.read_scale()["weight"]
            scale_state = {"weight": weight, "timestamp": int(time.time()) }
            scale_state_variable.set(f'{str(round(weight))} ml')
            root.after(READ_WEIGHT_INTERVAL_MS, read_scale)
        except:
            set_error_state(True)

def keep_scale_alive():
    global in_error_state
    if not in_error_state:
        dymo_scale.keep_alive()
        root.after(KEEP_ALIVE_INTERVAL_MS, keep_scale_alive)

def publish_weight():
    global scale_state, in_error_state
    if not in_error_state:
        response_code = api_service.post_state(scale_state)
        if response_code in range(200, 299):
            published_variable.set(f'Molnstatus: OK')
        else:
            published_variable.set(f'Molnstatus: Fel ({response_code})')

        weight = str(round(scale_state['weight']))
        date = datetime.datetime.fromtimestamp(scale_state["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
        published_data_variable.set(
            f'{date} ({weight} ml)'
        )
        root.after(PUBLISH_WEIGHT_INTERVAL_MS, publish_weight)

# Initialize things needed for tkinter
root = tk.Tk()
if (USE_FULLSCREEN):
    root.attributes('-fullscreen', True)

frame = tk.Frame(root, width=480, height=320, bg="black")
published_frame = tk.Frame(root, bg="black")

scale_state_variable = tk.StringVar(root, "Ansluter till våg...")
published_variable = tk.StringVar(published_frame, "Molnstatus: Okänt")
published_data_variable = tk.StringVar(published_frame, "Inget skickat än")

# Initialize other things
in_error_state = False
api_service = ApiService()

# Define UI elements
lbl_coffee_info = tk.Label(
    master=frame,
    textvariable=scale_state_variable,
    font=("arial", 28),
    bg="black",
    fg="white"
)

lbl_publish_title = tk.Label(
    master=published_frame,
    textvariable=published_variable,
    bg="black",
    fg="white"
)

lbl_publish_value = tk.Label(
    master=published_frame,
    textvariable=published_data_variable,
    bg="black",
    fg="white"
)

btn_retry = tk.Button(
    master=frame,
    command=retry,
    text="Anslut",
    bg="black",
    fg="white",
    width=8,
    height=3,
    font=("arial", 18),
)

btn_exit = tk.Button(
    master=frame,
    command=exit,
    text="Avsluta",
    bg="black",
    fg="white",
    font=("arial", 16),
)

# Place UI elements
lbl_coffee_info.place(x=32,y=32)
btn_exit.place(x=372,y=270)

lbl_publish_title.pack(anchor="w")
lbl_publish_value.pack(anchor="w")
published_frame.place(x=32,y=250)

frame.pack(fill='both')

# Start reading and launch UI
begin_reading()
root.mainloop()
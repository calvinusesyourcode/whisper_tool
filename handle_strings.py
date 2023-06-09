import datetime, time
import tkinter as tk
import pyperclip

def to_time(seconds):
    """Convert seconds to hh:mm:ss string, for use with ffmpeg."""
    return str(datetime.timedelta(seconds=seconds))

def get_clipboard():
    clipboard_text = pyperclip.paste()
    return clipboard_text

import tkinter as tk
import time

def show_message(message):
    # Create a new Tkinter window
    window = tk.Tk()
    window.configure(bg='black')
    window.overrideredirect(True)

    # Create a label with your message
    message_label = tk.Label(window, text=message, font=("TkFixedFont", 12), fg="white", bg="black")

    message_label.pack()
    window.update()

    window_width = message_label.winfo_reqwidth()
    window_height = message_label.winfo_reqheight()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    window.update()

    time.sleep(estimate_reading_time(message))
    window.destroy()


def estimate_reading_time(text):
    words_per_minute = 200
    words = text.split()
    num_words = len(words)
    minutes = num_words / words_per_minute
    # convert reading time to seconds
    seconds = minutes * 60
    return seconds

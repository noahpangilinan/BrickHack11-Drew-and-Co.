import tkinter as tk
from pathlib import Path
from tkinter import scrolledtext
import threading
import queue
global text_display
global script_text
def createGUI(file):
    root = tk.Tk()
    root.title("Live Speech Tracker")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window size
    window_width = 600
    window_height = 400

    # Set position for right side of the screen
    position_top_right = (screen_width - window_width),(screen_height - window_height) // 2  # Right side, center vertically

    # Set the window geometry
    root.geometry(f"{window_width}x{window_height + position_top_right[1]}")

    # Scrolled Text widget to display speech script
    text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 14))
    text_display.pack(padx=10, pady=10)

    # Load the script into the text box
    script_path = Path(file)
    with open(script_path, "r") as f:
        script_text = f.read()

    text_display.insert(tk.END, script_text)
    words = script_text.split()
    root.mainloop()

    # Queue for thread communication
highlight_queue = queue.Queue()

# Function to highlight words
def highlight_word(word):
    """Highlight a word in the Text widget."""
    start_index = f"1.0+{script_text.find(word)}c"
    end_index = f"1.0+{script_text.find(word) + len(word)}c"
    text_display.tag_add("highlight", start_index, end_index)
    text_display.tag_configure("highlight", background="yellow")

# Worker thread function
def highlight_thread(file):
    """Thread that waits for a word to highlight."""
    createGUI(file)
    while True:
        word = highlight_queue.get()  # Block until a word is provided
        if word:
            highlight_word(word)
            # Optionally, this can loop back and continue highlighting other words

# Function to trigger highlighting (can be called from main thread)
def trigger_highlight(word):
    """Place the word into the queue to be highlighted."""
    highlight_queue.put(word)

# Start the thread

# Example of triggering the highlight
trigger_highlight("example")  # Call this with the word you want to highlight


import tkinter as tk
from pathlib import Path
from tkinter import scrolledtext
import threading
import queue
global text_display
global script_text
global script_path
def createGUI(file):
    root = tk.Tk()
    root.title("Live Speech Tracker")

    # Set window size
    window_width = 700  # Adjust as needed
    window_height = 850  # Adjust as needed

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    position_x = screen_width - window_width  # 50px margin from the right
    position_y = (screen_height - window_height) // 2  # Center vertically

    global script_text
    global script_path
    global text_display

    # Set window geometry
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Scrolled Text widget to display speech script
    text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 14))
    text_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Load the script into the text box
    script_path = Path(file)

    with open(script_path, "r") as f:
        script_text = f.read()

    text_display.insert(tk.END, script_text)
    # text_display.pack()


    words = script_text.split()
    root.mainloop()

    # Queue for thread communication
highlight_queue = queue.Queue()


def highlight_word(word, occurrence):
    """Find and highlight the nth occurrence of a word in the text display."""

    start_index = "1.0"  # Start searching from the beginning
    count = 0  # Track occurrences of the word

    while True:
        # Find the next occurrence of the word
        start_index = text_display.search(word, start_index, stopindex=tk.END, nocase=True)

        if not start_index:  # No more occurrences found
            print(f"No valid occurrence #{occurrence} of '{word}' found.")
            return

        count += 1  # Increment occurrence count

        if count < occurrence:
            # If we haven't reached the desired occurrence, continue searching
            start_index = f"{start_index} + {len(word)}c"
            continue

        # Calculate end index
        line, char = map(int, start_index.split("."))
        end_index = f"{line}.{char + len(word)}"

        # Check if this word is already highlighted 
        highlighted_ranges = text_display.tag_ranges("highlight")
        is_highlighted = any(
            text_display.compare(start_index, ">=", highlighted_ranges[i]) and
            text_display.compare(end_index, "<=", highlighted_ranges[i + 1])
            for i in range(0, len(highlighted_ranges), 2)
        )

        if is_highlighted:
            print(f"Skipping '{word}' at {start_index} (already highlighted).")
            return

        # Highlight the found word
        text_display.tag_config("highlight", background="yellow", foreground="black")
        text_display.tag_add("highlight", start_index, end_index)
        print(f"Highlighted occurrence #{occurrence} of '{word}' at {start_index}")
        return  # Stop after highlighting the correct word


# Worker thread function
def highlight_thread(file):
    """Thread that waits for a word to highlight."""
    createGUI(file)
    while True:
        word = highlight_queue.get()  # Block until a word is provided
        print(word)
        if word:
            print("here")
            highlight_word(word)
            # Optionally, this can loop back and continue highlighting other words

# Function to trigger highlighting (can be called from main thread)
def trigger_highlight(word, index):
    """Place the word into the queue to be highlighted."""
    highlight_queue.put(word)
    highlight_word(word, index)




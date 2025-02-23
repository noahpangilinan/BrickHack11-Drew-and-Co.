import re
import tkinter as tk
from pathlib import Path
from tkinter import scrolledtext
import threading
import queue
global text_display
global script_text
global script_path
exit_program = False
global root
def on_key_press(event):
    """Function to handle key press events."""
    global exit_program
    if event.char == 'q':  # Check if 'q' is pressed
        print("Exiting program...")
        exit_program = True
        root.quit()  # Quit the Tkinter main loop
        root.destroy()  # Destroy the Tkinter window

def createGUI(file):
    global root
    root = tk.Tk()
    root.title("Live Speech Tracker")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    global script_text
    global script_path
    global text_display

    # Set window size
    window_width = screen_width
    window_height = screen_height

    # Set position for right side of the screen
    position_top_right = (screen_width),(screen_height) // 2  # Right side, center vertically

    # Set the window geometry
    root.geometry(f"{window_width}x{window_height + position_top_right[1]}")
    root.bind('<KeyPress>', on_key_press)

    # Scrolled Text widget to display speech script
    text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=60, font=("Arial", 14))
    text_display.pack(padx=10, pady=10)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the window geometry to the left half of the screen
    root.geometry(f"{screen_width // 2}x{screen_height-50}")

    # Optionally, remove window decorations for a cleaner look
    root.overrideredirect(True)
    # Load the script into the text box
    script_path = Path(file)

    with open(script_path, "r") as f:
        script_text = f.read()
        script_text = re.sub(r"[^\w\s.]", "", script_text)

    text_display.insert(tk.END, script_text)
    # text_display.pack()


    words = script_text.split()
    root.mainloop()

    # Queue for thread communication
highlight_queue = queue.Queue()

def highlight_word(word):
    """Find and highlight the first unhighlighted occurrence of a word,
    only if the character before it is highlighted, and highlight the space after."""

    start_index = "1.0"  # Start searching from the beginning
    while True:
        # Find the next occurrence of the word
        start_index = text_display.search(word, start_index, stopindex=tk.END, nocase=True)

        if not start_index:  # No more occurrences
            print(f"No unhighlighted occurrences of '{word}' found.")
            return

        # Calculate end index based on word length
        line, char = map(int, start_index.split("."))
        end_index = f"{line}.{char + len(word)}"

        # Check if the word is at the start of the file
        is_at_start_of_file = char == 0

        # Get the character before the word (if not at the start of the file)
        char_before_index = f"{line}.{char - 1}" if char > 0 else None

        # Get all highlighted ranges
        highlighted_ranges = text_display.tag_ranges("highlight")

        # Check if the character before the word is highlighted (if not at the start of the file)
        is_char_before_highlighted = (
            char_before_index is not None and
            any(
                text_display.compare(char_before_index, ">=", highlighted_ranges[i]) and
                text_display.compare(char_before_index, "<=", highlighted_ranges[i + 1])
                for i in range(0, len(highlighted_ranges), 2)
            )
        )

        # Check if this word is already highlighted
        is_word_highlighted = any(
            text_display.compare(start_index, ">=", highlighted_ranges[i]) and
            text_display.compare(end_index, "<=", highlighted_ranges[i + 1])
            for i in range(0, len(highlighted_ranges), 2)
        )

        # Highlight if:
        # 1. The word is at the start of the file, OR
        # 2. The character before the word is highlighted
        if (is_at_start_of_file or is_char_before_highlighted) and not is_word_highlighted:
            # Highlight the word and the space after it
            space_after_index = f"{line}.{char + len(word) + 1}"
            print(f"Highlighting '{word}' at {start_index} to {space_after_index}")
            text_display.tag_config("highlight", background="yellow", foreground="black")
            text_display.tag_add("highlight", start_index, space_after_index)
            return  # Stop after highlighting the first unhighlighted occurrence

        # Move to the next occurrence
        start_index = end_index
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
def trigger_highlight(word):
    """Place the word into the queue to be highlighted."""
    print(f"trigger highlight {word}")
    highlight_queue.put(word)
    highlight_word(word)




import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox

outScript = "speech.txt"

def readSpeech():
    clearFileOutput()
    createUI()

def clearFileOutput():
    try:
      with open(outScript, 'w') as file:
        pass
        print(f"Contents of '{outScript}' have been erased.")
    except Exception as e:
        print(f"An error occurred: {e}")

def on_drop(event):
    # This updates the entry with the dropped file path
    inScript.set(event.data)
    open_file()

def open_file():
    try:
        # Get the file path from the entry widget
        file_path = inScript.get()
        
        with open(file_path, "r") as file:    # Open and read input file
            content = file.read()
            content = content.lower()        # Convert to lowercase

        with open(outScript, 'w') as file:   # Open output text file and copy input text
            file.write(content)

        with open(outScript, 'r') as file:   # Print output text file to check it was done correctly
            copy = file.read()
            print(copy)

    except FileNotFoundError:
        print("Error: File not found. Please try again.")
    except IsADirectoryError:
        print("Error: The provided path is a directory. Please enter a valid file path.")
    except PermissionError:
        print("Error: Permission denied. You don't have access to this file. Please try a different file.")
    except Exception as e:
        print(f"An error occurred: {e}")


def createUI():
    # Set up the main Tkinter window
    root = TkinterDnD.Tk()
    root.title("File Reader")
    root.geometry("600x300")

    # Create a Label and Entry to enter file path
    label = tk.Label(root, text="Enter file path or drag a file here:")
    label.pack(pady=10)

    # Initialize inScript as a StringVar to hold the file path
    global inScript
    inScript = tk.StringVar()

    file_entry = tk.Entry(root, textvariable=inScript, width=60)
    file_entry.pack(pady=10)

    # Create a LabelFrame for drag-and-drop area
    drag_drop_frame = tk.LabelFrame(root, text="Drag and Drop Here", width=500, height=80)
    drag_drop_frame.pack(pady=10)

    # Enable drag-and-drop for the LabelFrame
    drag_drop_frame.drop_target_register(DND_FILES)
    drag_drop_frame.dnd_bind('<<Drop>>', on_drop)

    # Create a button to open the file
    open_button = tk.Button(root, text="Open File", command=open_file)
    open_button.pack(pady=40)

    # Start the main event loop
    root.mainloop()

readSpeech()


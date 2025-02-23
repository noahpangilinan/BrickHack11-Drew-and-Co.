import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog

outScript = "speech.txt"
fileOpened = False

def readSpeech():
    clearFileOutput()
    createUI()
    return fileOpened

def fileExplorerInput():
    # Open the file explorer to save a file
    selectedFile = filedialog.askopenfilename(title="Select a file")   
    return selectedFile
    

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

def open_file():
    try:
        global fileOpened
        # Get the file path from the entry widget
        file_path = inScript.get()

        if not file_path:
            file_path = fileExplorerInput()
            fileOpened = (file_path != "")
        else:
            fileOpened = True
        
        with open(file_path, "r") as file:    # Open and read input file
            content = file.read()
            content = content.lower()        # Convert to lowercase

        with open(outScript, 'w') as file:   # Open output text file and copy input text
            file.write(content)

        #with open(outScript, 'r') as file:   # Print output text file to check it was done correctly
        #    copy = file.read()
        #    print(copy)

    except FileNotFoundError:
        print("Error: File not found. Please try again.")
    except IsADirectoryError:
        print("Error: The provided path is a directory. Please enter a valid file path.")
    except PermissionError:
        print("Error: Permission denied. You don't have access to this file. Please try a different file.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Close UI
    if (file_path != ""):
      root.destroy()


def createUI():
    # Set up the main Tkinter window
    global root
    root = TkinterDnD.Tk()
    root.title("File Reader")
    root.geometry("500x300")

    # Create a Label and Entry to enter file path
    label = tk.Label(root, text="Enter file path or select open file")
    label.pack(pady=10)

    # Initialize inScript as a StringVar to hold the file path
    global inScript
    inScript = tk.StringVar()

    file_entry = tk.Entry(root, textvariable=inScript, width=60)
    file_entry.pack(pady=20)

    # Create a button to open the file
    open_button = tk.Button(root, text="Open File", width=15, height=1, 
                            font=("Helvetica", 16), command=open_file)
    open_button.pack(pady=40)

    # Start the main event loop
    root.mainloop()



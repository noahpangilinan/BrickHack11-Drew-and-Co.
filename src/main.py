import queue
import time
from tkinter import scrolledtext
import tkinter as tk

import videomodule.camera as camera
import threading

from audiomodule.autoscroller.autoscroller import highlight_thread, trigger_highlight
from audiomodule.speechToText.speechToText import start_audio_detection
from audiomodule.speechToText.speechScript import readSpeech
from pathlib import Path


print("my glorious king drew")
fileOpened = readSpeech()




def main():
    # Start the body tracker in a separate thread
    tracker_thread = threading.Thread(target=camera.body_tracker)
    speech_thread = threading.Thread(target=start_audio_detection, args=[(Path("speech.txt"))], daemon=True)
    highlight_thread_instance = threading.Thread(target=highlight_thread, args=[(Path("speech.txt"))], daemon=True)

    tracker_thread.start()
    speech_thread.start()
    if (fileOpened):
      highlight_thread_instance.start()

    time.sleep(3)

    tracker_thread.join()
    speech_thread.join()

if __name__ == "__main__":
    main()

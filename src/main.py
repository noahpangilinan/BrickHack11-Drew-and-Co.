import time
import videomodule.camera as camera
import threading
from audiomodule.speechToText.speechToText import start_audio_detection
from audiomodule.speechToText.speechScript import readSpeech
from pathlib import Path


def main():
    # Start the body tracker in a separate thread
    tracker_thread = threading.Thread(target=camera.body_tracker)
    tracker_thread.start()

    time.sleep(3)
    # Add messages in the main thread

    # Wait for the tracker thread to finish (optional)
    tracker_thread.join()

if __name__ == "__main__":
    main()

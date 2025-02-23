import time
import videomodule.camera as camera
import threading
from audiomodule.speechToText.speechToText import start_audio_detection
from audiomodule.speechToText.speechScript import readSpeech
from pathlib import Path



print("my glorious king drew")
readSpeech()

def main():
    # Start the body tracker in a separate thread
    tracker_thread = threading.Thread(target=camera.body_tracker)
    speech_thread = threading.Thread(target=start_audio_detection, args=[(Path("speech.txt"))])

    tracker_thread.start()
    speech_thread.start()

    time.sleep(3)

    # Wait for the tracker thread to finish (optional)
    tracker_thread.join()
    speech_thread.join()

if __name__ == "__main__":
    main()

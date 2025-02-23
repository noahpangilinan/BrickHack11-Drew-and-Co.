import time
import videomodule.camera as camera
import threading
from audiomodule.speechToText.speechToText import start_audio_detection
from audiomodule.speechToText.speechScript import readSpeech
from pathlib import Path


print("my glorious king drew")
# readSpeech()

def run_message_loop():
    for i in range(5):  # For example, 5 messages
        camera.display_message(f"Message {i + 1}")
        time.sleep(2)  # Wait for 1 second before adding the next message


def main():
    # Start the body tracker in a separate thread
    tracker_thread = threading.Thread(target=camera.body_tracker)
    speech_thread = threading.Thread(target=start_audio_detection, args=[(Path("speech.txt"))])
    message_thread = threading.Thread(target=run_message_loop)

    tracker_thread.start()
    speech_thread.start()

    time.sleep(3)
    # Add messages in the main thread
    # run_message_loop()

    # Wait for the tracker thread to finish (optional)
    tracker_thread.join()
    speech_thread.join()
    message_thread.join()

if __name__ == "__main__":
    main()

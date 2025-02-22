import time
import videomodule.camera as camera
import threading

def run_message_loop():
    for i in range(5):  # For example, 5 messages
        camera.display_message(f"Message {i + 1}")
        time.sleep(2)  # Wait for 1 second before adding the next message


def main():
    # Start the body tracker in a separate thread
    tracker_thread = threading.Thread(target=camera.body_tracker)
    tracker_thread.start()

    time.sleep(3)
    # Add messages in the main thread
    run_message_loop()

    # Wait for the tracker thread to finish (optional)
    tracker_thread.join()

if __name__ == "__main__":
    main()

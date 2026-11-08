# BrickHack 11: Drew & Co.

A live public-speaking coach built at BrickHack 11 (RIT, February 2025). Load the script of your talk, start
speaking, and it follows along and gives you feedback in real time:

- **Teleprompter.** Your script opens in a window and each word is highlighted as you say it, using
  offline speech recognition ([Vosk](https://alphacephei.com/vosk/), small English model, bundled).
- **Delivery checks.** If too few of your words are being recognised, it tells you to **enunciate**.
- **Body language.** Your webcam feed runs through MediaPipe pose tracking, with on-screen prompts to
  **move your hands** when you've been still too long and to **look forward** when you turn away from the camera.

Built by Noah Pangilinan, Drew Ryczek and Ryan Miner.

## Running it

Needs Python 3.11 or 3.12, a webcam and a microphone.

```sh
python -m venv venv
venv\Scripts\activate             # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
pip install pyaudio tkinterdnd2   # not yet in requirements.txt
python src/main.py
```

Run it from the repository root. A window asks for your speech script (drag a `.txt` file onto it or
browse for one), then the camera feed and the teleprompter open. Press `q` in the teleprompter to quit.

## Layout

```
src/main.py                         starts the camera, speech and highlighting threads
src/videomodule/camera.py           MediaPipe pose tracking and on-screen messages
src/audiomodule/speechToText/       script picker and Vosk speech recognition
src/audiomodule/autoscroller/       teleprompter window that highlights spoken words
src/audiomodule/VOSKmodel/          vosk-model-small-en-us-0.15
test/                               sample speeches
```

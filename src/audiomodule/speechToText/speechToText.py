import json

from vosk import Model, KaldiRecognizer
import pyaudio
from pathlib import Path
model_path = Path(__file__).parent.parent
model = Model(str(model_path) + "/VOSKmodel/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()


def start_audio_detection():

    print("Start speaking...")

    with open("audioToText.txt", "a") as f:
        while True:
            data = stream.read(8192)

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_json = json.loads(result)
                text = result_json.get('text', '')

                if text:
                    print(f"Recognized: {text}")
                    f.write(text + "\n")
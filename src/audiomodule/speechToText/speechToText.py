import json
from os.path import isfile

from vosk import Model, KaldiRecognizer
import pyaudio
from pathlib import Path
model_path = Path(__file__).parent.parent
model = Model(str(model_path) + "/VOSKmodel/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()


def start_audio_detection(file = ""):
    data = []
    annunciation_count = 0
    if isfile(file):
        with open(file, "r") as file:  # Open and read input file
            content = file.read()
            data = content.split()
    print(data)
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
                    for i in text.split():
                        for j in range(0, 5):
                            if data[j] == i:
                                data = data[j:]
                            elif (data[j] != i):
                                annunciation_count += 1
                                print(annunciation_count)
                    print(data[:10])


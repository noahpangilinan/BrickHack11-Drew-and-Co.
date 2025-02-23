import json
from os.path import isfile
from videomodule.camera import display_message

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
    speechdata = []
    enunciated_count = 0
    new_words = 0
    if isfile(file):
        with open(file, "r") as file:  # Open and read input file
            content = file.read()
            speechdata = content.split()
    with open("audioToText.txt", "w") as f:
        while True:
            data = stream.read(8192)

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_json = json.loads(result)
                text = result_json.get('text', '')

                if text:
                    print(f"Recognized: {text}")
                    print(f"Next words in speech: {speechdata[0:5]}")

                    f.write(text + "\n")
                    new_words = len(text.split())
                    display_message(text)

                    print("new words:" + str(new_words))
                    for i in text.split():

                        for j in range(0, 5):
                            if speechdata[j] == i:
                                speechdata = speechdata[j:]
                                break

                            elif not (speechdata[j] == i) and (new_words > 0):
                                enunciated_count += 1
                                display_message("Non-enunciated words: " + str(enunciated_count))
                                new_words -= 1


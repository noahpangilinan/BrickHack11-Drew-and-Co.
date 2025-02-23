import json
from os.path import isfile
from tkinter import scrolledtext
import tkinter as tk

from audiomodule.autoscroller.autoscroller import highlight_word, trigger_highlight
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


def start_audio_detection(file = "", callback=None):
    speechdata = []
    enunciated_count = 0
    new_words = 0
    if isfile(file):
        with open(file, "r") as file:  # Open and read input file
            content = file.read()
            speechdata = content.split()
    with open("audioToText.txt", "w") as f:
        display_message("START SPEECH")

        while True:

            data = stream.read(2048, exception_on_overflow=False)
            text = None
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_json = json.loads(result)

                text = result_json.get('text', '')

            else:
                result = recognizer.PartialResult()  # Get partial results more frequently
                result_json = json.loads(result)

                text = result_json.get('partial', '')
                trigger_highlight(text)


            if text:
                # print(f"Recognized: {text}")
                if callback:
                    callback(text)
                f.write(text + "\n")
                new_words = len(text.split())
                counter = len(text.split())
                sentence = ""
                # display_message(text)
                lastmissheardword = ""
                # print("new words:" + str(new_words))
                for i in text.split():

                    if not (i in speechdata[:counter]):

                        enunciated_count += 1

                        # print(f"Misheard word: {i}")
                    for j in range(0, counter):
                        # print(speechdata)
                        if speechdata[j] == i and j < 5:

                            speechdata = speechdata[j + 1:]
                            sentence += ("---- " * j)

                            sentence += f"{i} "

                            enunciated_count -= .5

                            break
                # print(f"Next words in speech: {speechdata[0:len(text.split())]}")
                if enunciated_count > 10:
                    display_message("ENUNCIATE!!!")
                # print(f"enunciated_count : {enunciated_count}")
                print(sentence)

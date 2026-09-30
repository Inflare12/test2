import os
import json
import time
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

audio_queue = queue.Queue()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "vosk-model-small-en-us-0.15"
)
SAMPLE_RATE = 16000
print("Loading Voice Model...")
model = Model(MODEL_PATH)
print("Voice Model Loaded")

WAKE_WORDS = {
    "fox",
    "rox fox",
    "roux fox",
    "rocks fox"
}


def callback(indata, frames, time_info, status):
    audio_queue.put(bytes(indata))

def clear_queue():

    while not audio_queue.empty():

        try:
            audio_queue.get_nowait()

        except:
            break

def listen():

    recognizer = KaldiRecognizer(
        model,
        SAMPLE_RATE
    )

    result_queue = queue.Queue()

    def callback(
        indata,
        frames,
        time_info,
        status
    ):

        try:

            data = bytes(indata)

            if recognizer.AcceptWaveform(data):

                result = json.loads(
                    recognizer.Result()
                )

                text = (
                    result.get("text", "")
                    .lower()
                    .strip()
                )

                if text:

                    print("Heard:", text)

                    result_queue.put(text)

        except Exception as e:

            print(
                "Recognizer Error:",
                repr(e)
            )

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=4000,
        dtype="int16",
        channels=1,
        callback=callback
    ):

        while True:

            try:

                command = result_queue.get(
                    timeout=0.1
                )

                return command

            except queue.Empty:

                pass
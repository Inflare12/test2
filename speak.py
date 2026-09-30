from piper.voice import PiperVoice
import winsound
import wave
import os
import uuid
import gc
import time
import re

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

VOICE_PATH = os.path.join(
    BASE_DIR,
    "voices",
    "en_US-lessac-medium.onnx"
)

print("Loading Voice Model...")

voice = PiperVoice.load(
    VOICE_PATH
)

print("Voice Model Loaded")




def speak(text):

    if not text:
        return

    text = str(text).strip()

    text = text.replace("Roux", "Rox")
    text = text.replace("roux", "rox")

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        output_path = os.path.join(
            BASE_DIR,
            f"tts_{uuid.uuid4().hex}.wav"
        )

        try:

            with wave.open(output_path, "wb") as wav_file:

                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(22050)

                voice.synthesize_wav(
                    sentence,
                    wav_file
                )

            winsound.PlaySound(
                output_path,
                winsound.SND_FILENAME
            )

        except Exception as e:

            print("Speech Error:", e)

        finally:

            gc.collect()

            try:
                os.remove(output_path)
            except:
                pass
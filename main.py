import os
import random
import string

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

NATO_PHONETIC_ALPHABET = {
    "A": "Alfa",
    "B": "Bravo",
    "C": "Charlie",
    "D": "Delta",
    "E": "Echo",
    "F": "Foxtrot",
    "G": "Golf",
    "H": "Hotel",
    "I": "India",
    "J": "Juliett",
    "K": "Kilo",
    "L": "Lima",
    "M": "Mike",
    "N": "November",
    "O": "Oscar",
    "P": "Papa",
    "Q": "Quebec",
    "R": "Romeo",
    "S": "Sierra",
    "T": "Tango",
    "U": "Uniform",
    "V": "Victor",
    "W": "Whiskey",
    "X": "X-ray",
    "Y": "Yankee",
    "Z": "Zulu",
}

speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)

speech_config.speech_synthesis_voice_name="en-US-EricNeural"
speech_config.speech_recognition_language="en-US"

audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output_config)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

def get_prompt(length=3):
    return [random.choice(string.ascii_uppercase) for _ in range(length)]

def speak_prompt(prompt):
    print(f"Say the following letters using the NATO phonetic alphabet: {' '.join(prompt)}")
    speech_synthesizer.speak_text_async("Say the following letters using the NATO phonetic alphabet").get()
    speech_synthesizer.speak_text_async("\n".join([letter for letter in prompt])).get()

def clean_spoken_prompt(prompt):
    if prompt.isupper():
        return prompt
    else:
        return "".join([word[0] for word in prompt.split(" ")])

def recognize_prompt(prompt):
    speech_recognizer_result = speech_recognizer.recognize_once_async().get()

    if speech_recognizer_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        spoken_prompt = clean_spoken_prompt(speech_recognizer_result.text[:-1])
        if "".join(prompt) == spoken_prompt:
            print("Correct!")
            speech_synthesizer.speak_text_async("Correct!").get()
        else:
            nato_prompt = " ".join([NATO_PHONETIC_ALPHABET[letter] for letter in prompt])
            nato_spoken_prompt = " ".join([NATO_PHONETIC_ALPHABET[letter] for letter in spoken_prompt])
            print(f"Incorrect!  I expected {nato_prompt} but heard {nato_spoken_prompt}")

            nato_prompt = "\n".join([NATO_PHONETIC_ALPHABET[letter] for letter in prompt])
            nato_spoken_prompt = "\n".join([NATO_PHONETIC_ALPHABET[letter] for letter in spoken_prompt])
            speech_synthesizer.speak_text_async(f"Incorrect! I expected {nato_prompt} but heard {nato_spoken_prompt}").get()

if __name__ == "__main__":
    prompt = get_prompt()
    speak_prompt(prompt)
    recognize_prompt(prompt)
import os
import time
import wave
import json
import queue
import threading
import subprocess
import pyaudio
from gtts import gTTS
from vosk import Model, KaldiRecognizer
import eye

is_running = True
is_speaking = False
is_thinking = False

def get_robot_status():
    global is_running, is_speaking, is_thinking
    return is_running, is_speaking, is_thinking

MODEL_PATH = "vosk-model-small-tr-0.3"
if not os.path.exists(MODEL_PATH):
    print(f"Hata: '{MODEL_PATH}' klasörü bulunamadı!")
    exit(1)

print("Vosk modeli yükleniyor...")
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
print("Model yüklendi, sistem hazır.")

INPUT_INDEX = 1
OUTPUT_INDEX = 0
INPUT_RATE = 44100
OUTPUT_RATE = 48000

def record_and_recognize():
    global is_thinking, is_speaking
    p = pyaudio.PyAudio()
    
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=INPUT_RATE,
        input=True,
        input_device_index=INPUT_INDEX,
        frames_per_buffer=2048
    )
    stream.start_stream()
    print("\nDinleniyor... Konuşabilirsiniz.")

    while is_running:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip()
            if text:
                print(Algılanan: "{text}")
                is_thinking = True
                handle_command(text)
                is_thinking = False

def handle_command(text):
    global is_speaking
    response_text = f"\"{text}\" dediniz. Sizi duyuyorum."
    
    is_speaking = True
    speak_text(response_text)
    is_speaking = False

def speak_text(text):
    print(f"Cezeri diyor ki: {text}")
    mp3_path = "speech_output.mp3"
    wav_path = "speech_output.wav"

    tts = gTTS(text=text, lang='tr')
    tts.save(mp3_path)

    subprocess.run(
        ["ffmpeg", "-y", "-i", mp3_path, "-ac", "1", "-ar", str(OUTPUT_RATE), wav_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if os.path.exists(wav_path):
        wf = wave.open(wav_path, 'rb')
        p = pyaudio.PyAudio()
        
        output_stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=OUTPUT_RATE,
            output=True,
            output_device_index=OUTPUT_INDEX
        )

        data = wf.readframes(1024)
        while data:
            output_stream.write(data)
            data = wf.readframes(1024)

        output_stream.stop_stream()
        output_stream.close()
        p.terminate()
        wf.close()

if __name__ == "__main__":
    eye_thread = threading.Thread(target=EyeMovement.eyes_idle_loop, args=(get_robot_status,))
    eye_thread.daemon = True
    eye_thread.start()
    try:
        record_and_recognize()
    except KeyboardInterrupt:
        print("\nSistem kapatılıyor...")
        is_running = False
        eye_thread.join()
        print("Güvenli çıkış yapıldı.")
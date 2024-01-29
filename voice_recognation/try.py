import openai
import numpy as np
import pyaudio
import wave

# Set the path to the downloaded Whisper Tiny model file
whisper_tiny_model_path = 'path/to/whisper-tiny-model.onnx'

# Function to record speech
def record_speech(duration, filename):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 16000

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    print("Recording...")
    for i in range(int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function for offline voice recognition using OpenAI Whisper Tiny model
def offline_voice_recognition(audio_path):
    whisper_tiny = openai.Transcription.create(model="whisper-tiny", language="en")

    with open(audio_path, 'rb') as f:
        audio_content = f.read()

    response = whisper_tiny.transcribe(audio_content)

    # Extract transcribed text
    transcribed_text = response['text']
    print("Transcribed text:", transcribed_text)

# Replace 'path/to/whisper-tiny-model.onnx' with the actual path to your Whisper Tiny model file
whisper_tiny_model_path = 'path/to/whisper-tiny-model.onnx'
audio_filename = 'recorded_speech.wav'
record_speech(duration=5, filename=audio_filename)
offline_voice_recognition(audio_path=audio_filename)

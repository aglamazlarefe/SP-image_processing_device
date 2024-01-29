import pyaudio
from vosk import Model, KaldiRecognizer
import json
import wave

# Initialize PyAudio
p = pyaudio.PyAudio()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Create a list to store audio frames
frames = []

def record_callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return None, pyaudio.paContinue

# Open a stream with the callback function
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=1024,
                stream_callback=record_callback,
                input=True)

print("Recording...")

# Start the stream
stream.start_stream()

# Record for RECORD_SECONDS
for i in range(int(RATE / 1024 * RECORD_SECONDS)):
    pass

# Stop the stream
stream.stop_stream()
stream.close()

# Save the recorded audio to a WAV file
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

# Prepare VOSK model
path_to_model = r"C:\Users\aglam\Documents\python_projeleri\SP-image_processing_device\voice_recognation\vosk-model-small-tr-0.3"
model = Model(path_to_model)

# Initialize recognizer
recognizer = KaldiRecognizer(model, RATE)

# Feed raw audio data to the recognizer
with open(WAVE_OUTPUT_FILENAME, 'rb') as wf:
    data = wf.read()
    recognizer.AcceptWaveform(data)

# Retrieve the recognized text
result = recognizer.FinalResult()
parsed_result = json.loads(result)
text = parsed_result['text']

print("Recognized text: ", text)

p.terminate()

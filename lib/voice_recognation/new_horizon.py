import speech_recognition as sr
import vosk
import json

vosk.SetLogLevel(-1)
def transcribe_audio():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Initialize the microphone
    with sr.Microphone() as source:
        print("Say something...")
        # Capture audio data in a format compatible with Vosk
        audio_data = recognizer.listen(source)

    try:
        # Use Vosk to transcribe the speech
        model = vosk.Model("voice_recognation/vosk-model-small-tr-0.3")
        recognizer_vosk = vosk.KaldiRecognizer(model, 16000)

        # Get raw audio data from SpeechRecognition and pass it to Vosk
        audio_data_vosk = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
        recognizer_vosk.AcceptWaveform(audio_data_vosk)

        # Get the transcription result from Vosk
        result_json = json.loads(recognizer_vosk.Result())
        
        # Extract and print the recognized text
        transcription = result_json.get("text", "")
        print("Transcription:", transcription)

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return transcription



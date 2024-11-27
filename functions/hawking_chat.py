import pyttsx3

def synthesize_voice(text):
    engine = pyttsx3.init()
    engine.setProperty("voice", "english+f4")  # Use a similar voice
    audio_file = "response.mp3"
    engine.save_to_file(text, audio_file)
    engine.runAndWait()
    return audio_file

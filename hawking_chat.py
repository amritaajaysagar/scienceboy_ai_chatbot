import pyttsx3

def hawking_voice(text):
    engine = pyttsx3.init()
    engine.setProperty("voice", "english+f4")  # Use a similar voice
    audio_file = "response.mp3"
    engine.save_to_file(text, audio_file)
    engine.runAndWait()
    return audio_file 

""" def hawking_voice(text, audio_path):
    engine = pyttsx3.init()
    engine.setProperty("voice", "english+f4")  # Use a similar voice
    
    # Save the audio file to the specified path
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    
    return audio_path  """
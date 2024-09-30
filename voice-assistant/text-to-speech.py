import pyttsx3

def text_to_speech(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    
    # Get and print the current voice properties
    voices = engine.getProperty('voices')
    print(f"Available voices: {[voice.name for voice in voices]}")
    
    # Set the voice property (optional)
    # engine.setProperty('voice', voices[0].id)  # Change index to switch voices

    # Set the speech rate (optional)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)  # Speed of speech

    # Convert text to speech
    engine.say(text)
    
    # Wait for the speech to finish
    engine.runAndWait()

# Example usage
text_to_speech("Hello, how are you today? This is a text to speech conversion example.")

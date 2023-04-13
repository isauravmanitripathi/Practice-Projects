import pyttsx3 # This line imports the pyttsx3 library, which is a text-to-speech conversion library in Python.

voiceoverDir = "Voiceovers" #  This line defines a global variable voiceoverDir, which stores the name of the directory where the voiceover audio files will be saved.

def create_voice_over(fileName, text): # This line defines the create_voice_over function, which takes two parameters: fileName (a string representing the name of the voiceover file without the extension) and text (a string containing the text that will be converted to speech).
    filePath = f"{voiceoverDir}/{fileName}.mp3" # This line creates a formatted string that combines the voiceoverDir variable, the fileName parameter, and the ".mp3" extension. The resulting file path is assigned to the filePath variable.
    engine = pyttsx3.init() # This line initializes the pyttsx3 text-to-speech engine and assigns the resulting engine object to the engine variable.
    engine.save_to_file(text, filePath) # This line calls the save_to_file method of the engine object, passing the text and filePath variables as arguments. This method generates the voiceover audio file for the given text and saves it to the specified file path.
    engine.runAndWait() # This line calls the runAndWait method of the engine object, which blocks the execution of the script until the voiceover generation and saving process is complete.
    return filePath # This line returns the filePath variable, which represents the file path of the generated voiceover audio file.s
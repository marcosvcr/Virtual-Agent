import speech_recognition as sr

class VoiceRecognition:
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
                 
    def listen(self):

        with sr.Microphone(chunk_size = 1024, sample_rate = 44100) as source: 
            
            self.recognizer.adjust_for_ambient_noise(source)
                 
            audio = self.recognizer.listen(source, phrase_time_limit=5)

            try:
                transcription = self.recognizer.recognize_google(audio,language="pt-BR")
            except sr.UnknownValueError:
                transcription = 1
            except sr.RequestError:
                transcription = 400

        return transcription
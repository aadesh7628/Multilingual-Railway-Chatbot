import os
import tempfile
from typing import Tuple
from enum import Enum
from pydub import AudioSegment
from google.cloud import speech

class SpeechModel(Enum):
    nano = "nano"
    best = "best"

class AudioHandler:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Path to your key path"
        self.temp_dir = tempfile.mkdtemp()
        self.language_mapping = {
            'en': 'en-US',  # English (United States)
            'hi': 'hi-IN',  # Hindi (India)
            'bn': 'bn-IN',  # Bengali (India)
            'te': 'te-IN',  # Telugu (India)
            'mr': 'mr-IN',  # Marathi (India)
            'ta': 'ta-IN',  # Tamil (India)
            'ur': 'ur-IN',  # Urdu (India)
            'gu': 'gu-IN',  # Gujarati (India)
            'kn': 'kn-IN',  # Kannada (India)
            'ml': 'ml-IN',  # Malayalam (India)
            # 'pa': 'pa-IN',  # Punjabi (India)
            # 'as': 'as-IN',  # Assamese (India)
            'fr': 'fr-FR',  # French (France)
            'es': 'es-ES',  # Spanish (Spain)
            'de': 'de-DE',  # German (Germany)
            'it': 'it-IT',  # Italian (Italy)
            'pt': 'pt-PT',  # Portuguese (Portugal)
            'ru': 'ru-RU',  # Russian (Russia)
            'ja': 'ja-JP',  # Japanese (Japan)
            'ko': 'ko-KR',  # Korean (Korea)
            'zh': 'zh-CN',  # Chinese (Simplified, China)
            'ar': 'ar-SA',  # Arabic (Saudi Arabia)
        }

    def process_audio(self, audio_data, lang: str) -> Tuple[bool, str, str]:
        """Process audio and convert it to 16-bit PCM if needed."""
        try:
            lang = self.language_mapping.get(lang, 'en-US')
            if lang not in self.language_mapping.values():
                raise ValueError(f"Unsupported language code: {lang}")

            # Save the uploaded audio to a temporary file
            temp_path = os.path.join(self.temp_dir, "temp_audio.wav")
            with open(temp_path, "wb") as f:
                for chunk in audio_data.chunks():
                    f.write(chunk)

            # Convert the audio to 16-bit PCM format
            audio = AudioSegment.from_file(temp_path)
            audio = audio.set_frame_rate(16000).set_sample_width(2).set_channels(1)  # 2 bytes = 16-bit
            audio.export(temp_path, format="wav")

            # Initialize Google Cloud Speech client
            client = speech.SpeechClient()

            # Read the processed audio file
            with open(temp_path, "rb") as audio_file:
                content = audio_file.read()

            # Configure recognition settings
            recognition_audio = speech.RecognitionAudio(content=content)
            recognition_config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=lang,
            )

            # Transcribe the audio
            response = client.recognize(config=recognition_config, audio=recognition_audio)

            if not response.results:
                return False, "No transcription results", lang

            transcript = response.results[0].alternatives[0].transcript
            return True, transcript, lang

        except Exception as e:
            return False, str(e), lang

        finally:
            self.cleanup_audio_files()

    def cleanup_audio_files(self):
        """Clean up temporary audio files."""
        for file in os.listdir(self.temp_dir):
            try:
                os.remove(os.path.join(self.temp_dir, file))
            except Exception:
                pass
    





# import os
# import tempfile
# from typing import Tuple
# from enum import Enum
# from pydub import AudioSegment
# import assemblyai as aai

# class SpeechModel(Enum):
#     nano = "nano"
#     best = "best"

# class AudioHandler:
#     def __init__(self):
#         aai.settings.api_key = "6cc7ebf069e7414c990739c60c04da58"
#         self.temp_dir = tempfile.mkdtemp()
#         self.language_mapping = {
#             'en': 'en',
#             'hi': 'hi',
#             'bn': 'bn', 
#             'te': 'te',
#             'mr': 'mr',
#             'ta': 'ta',
#             'ur': 'ur',
#             'gu': 'gu',
#             'kn': 'kn',
#             'ml': 'ml',
#             'pa': 'pa',
#             'as': 'as',
#             'fr': 'fr',
#             'es': 'es',
#             'de': 'de',
#             'it': 'it',
#             'pt': 'pt',
#             'ru': 'ru',
#             'ja': 'ja',
#             'ko': 'ko',
#             'zh': 'zh',
#             'ar': 'ar',
#         }

#     def process_audio(self, audio_data, lang: str) -> Tuple[bool, str, str]:
#         try:
#             lang = self.language_mapping.get(lang, 'en')
#             if lang not in self.language_mapping.values():
#                 raise ValueError(f"Unsupported language code: {lang}")

#             # Debug: Check selected language and model
#             print(f"Language Code: {lang}")
            
#             temp_path = os.path.join(self.temp_dir, "temp_audio.wav")
#             with open(temp_path, "wb") as f:
#                 for chunk in audio_data.chunks():
#                     f.write(chunk)

#             audio = AudioSegment.from_file(temp_path)
#             audio.export(temp_path, format="wav")

#             # Select speech model
#             speech_model = SpeechModel.nano.value if lang != "en" else SpeechModel.best.value
#             print(f"Using Speech Model: {speech_model}")

#             # Transcription Config
#             config = aai.TranscriptionConfig(
#                 language_code=lang,
#                 speech_model=speech_model,
#                 punctuate=True,
#                 format_text=True
#             )
#             transcriber = aai.Transcriber(config=config)
#             transcript = transcriber.transcribe(temp_path)

#             # Debug: Check transcription result
#             print(f"Transcript Error: {transcript.error}")
#             print(f"Transcription Text: {transcript.text if not transcript.error else 'N/A'}")

#             if transcript.error:
#                 return False, str(transcript.error), lang

#             return True, transcript.text, lang
#         except Exception as e:
#             return False, str(e), lang
#         finally:
#             self.cleanup_audio_files()

    
#     def cleanup_audio_files(self):
#         """Clean up temporary audio files."""
#         for file in os.listdir(self.temp_dir):
#             try:
#                 os.remove(os.path.join(self.temp_dir, file))
#             except Exception:
#                 pass



















# import os
# import tempfile
# from typing import Tuple
# import torch
# from transformers import WhisperProcessor, WhisperForConditionalGeneration
# from pydub import AudioSegment

# class AudioHandler:
#     def __init__(self):
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         # Use smaller Whisper model
#         self.processor = WhisperProcessor.from_pretrained("openai/whisper-small")
#         self.model = WhisperForConditionalGeneration.from_pretrained(
#             "openai/whisper-small",
#             torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
#         ).to(self.device)
#         self.temp_dir = tempfile.mkdtemp()

#     def process_audio(self, audio_data, lang: str) -> Tuple[bool, str, str]:
#         try:
#             temp_path = os.path.join(self.temp_dir, "temp_audio.wav")
#             with open(temp_path, "wb") as f:
#                 for chunk in audio_data.chunks():
#                     f.write(chunk)

#             audio = AudioSegment.from_file(temp_path)
#             audio = audio.set_frame_rate(16000)
#             audio.export(temp_path, format="wav")

#             with open(temp_path, "rb") as f:
#                 input_features = self.processor(
#                     audio=f.read(),
#                     sampling_rate=16000,
#                     return_tensors="pt"
#                 ).input_features.to(self.device)

#             # Force decode in specified language
#             predicted_ids = self.model.generate(
#                 input_features,
#                 language=lang,
#                 task="transcribe"
#             )
#             transcribed_text = self.processor.batch_decode(
#                 predicted_ids, 
#                 skip_special_tokens=True
#             )[0]

#             return True, transcribed_text, lang

#         except Exception as e:
#             return False, str(e), lang

#         finally:
#             self.cleanup_audio_files()

#     def cleanup_audio_files(self):
#         for file in os.listdir(self.temp_dir):
#             try:
#                 os.remove(os.path.join(self.temp_dir, file))
#             except:
#                 pass







# from django.core.files.uploadedfile import InMemoryUploadedFile
# import speech_recognition as sr
# from pydub import AudioSegment
# from typing import Tuple, Optional
# import os

# class AudioHandler:
#     def __init__(self, audio_dir: str = 'chatRailways/static/audio'):
#         self.audio_dir = audio_dir
#         self.recognizer = sr.Recognizer()

#     def save_audio(self, audio_data: InMemoryUploadedFile, filename: str = 'voice_input.wav') -> str:
#         filepath = os.path.join(self.audio_dir, filename)
#         with open(filepath, 'wb+') as destination:
#             for chunk in audio_data.chunks():
#                 destination.write(chunk)
#         return filepath

#     def process_audio(self, audio_data: InMemoryUploadedFile, lang: str) -> Tuple[bool, str, str]:
#         try:
#             filepath = self.save_audio(audio_data)
#             sound = AudioSegment.from_file(filepath)
#             sound.export(filepath, format="wav")
            
#             with sr.AudioFile(filepath) as source:
#                 self.recognizer.adjust_for_ambient_noise(source, duration=1)
#                 audio = self.recognizer.record(source)
            
#             # Use language-specific recognition
#             if lang == "kn":
#                 text_result = self.recognizer.recognize_google(audio, language="kn-IN")
#             elif lang == "hi":
#                 text_result = self.recognizer.recognize_google(audio, language="hi-IN")
#             elif lang == "ta":
#                 text_result = self.recognizer.recognize_google(audio, language="ta-IN")
#             else:
#                 text_result = self.recognizer.recognize_google(audio, language=f"{lang}-IN")
            
#             return True, text_result, lang
                
#         except Exception as e:
#             return False, str(e), lang













# from django.core.files.uploadedfile import InMemoryUploadedFile
# import speech_recognition as sr
# from pydub import AudioSegment
# from typing import Tuple, Optional
# import os

# class AudioHandler:
#     def __init__(self, audio_dir: str = 'chatRailways/static/audio'):
#         self.audio_dir = audio_dir
#         self.recognizer = sr.Recognizer()

#     def save_audio(self, audio_data: InMemoryUploadedFile, filename: str = 'voice_input.wav') -> str:
#         filepath = os.path.join(self.audio_dir, filename)
#         with open(filepath, 'wb+') as destination:
#             for chunk in audio_data.chunks():
#                 destination.write(chunk)
#         return filepath
    
#     def process_audio(self, audio_data: InMemoryUploadedFile, lang: str) -> Tuple[bool, str, str]:
#         try:
#             filepath = self.save_audio(audio_data)
#             sound = AudioSegment.from_file(filepath)
#             sound.export(filepath, format="wav")

#             with sr.AudioFile(filepath) as source:
#                 self.recognizer.adjust_for_ambient_noise(source, duration=1)
#                 audio = self.recognizer.record(source)

#             text_result = self.recognizer.recognize_google(audio, language=f"{lang}")
#             return True, text_result, lang

#         except Exception as e:
#             return False, str(e), lang

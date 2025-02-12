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
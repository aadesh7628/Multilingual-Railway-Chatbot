from deep_translator import GoogleTranslator
from typing import Dict

class TextTranslator:
    def __init__(self):
        self.supported_languages = self._get_supported_languages()

    def trans(self, text: str, target_lang: str) -> str:
        """Translate text to target language."""
        if not text or not target_lang:
            raise ValueError("Both text and target language are required")

        if target_lang not in self.supported_languages:
            raise ValueError(f"Unsupported language code: {target_lang}")
        if target_lang == 'zh':
            translator = GoogleTranslator(source='auto', target='zh-CN')
        else:
            translator = GoogleTranslator(source='auto', target=target_lang)

        return translator.translate(text)

    def _get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported languages."""
        return {
            'en': 'English',
            'hi': 'Hindi',
            'bn': 'Bengali',
            'te': 'Telugu',
            'ta': 'Tamil',
            'mr': 'Marathi',
            'ur': 'Urdu',
            'gu': 'Gujarati',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            # 'pa': 'Punjabi',
            # 'as': 'Assamese',
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
        }
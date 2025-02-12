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










# from deep_translator import GoogleTranslator
# import time

# class TextTranslator:
#     def __init__(self):
#         self.supported_languages = {
#             'en': 'english', 'hi': 'hindi', 'bn': 'bengali', 'te': 'telugu',
#             'mr': 'marathi', 'ta': 'tamil', 'ur': 'urdu', 'gu': 'gujarati',
#             'kn': 'kannada', 'ml': 'malayalam', 'pa': 'punjabi', 'as': 'assamese',
#             'fr': 'french', 'es': 'spanish', 'de': 'german', 'it': 'italian',
#             'pt': 'portuguese', 'ru': 'russian', 'ja': 'japanese', 'ko': 'korean',
#             'zh': 'chinese', 'ar': 'arabic'
#         }

#     def trans(self, input_text: str, trans_lang: str) -> str:
#         """Translates text to the specified language with error handling and retries"""
#         if not input_text or not isinstance(input_text, str):
#             return ""
        
#         if not trans_lang or trans_lang not in self.supported_languages:
#             return input_text

#         max_retries = 3
#         retry_delay = 2  # seconds

#         for attempt in range(max_retries):
#             try:
#                 translator = GoogleTranslator(source='auto', target=trans_lang)
#                 translated_text = translator.translate(input_text)
#                 return translated_text if translated_text else input_text
            
#             except Exception as e:
#                 print(f"Translation attempt {attempt + 1} failed: {str(e)}")
#                 if attempt < max_retries - 1:
#                     time.sleep(retry_delay)
#                     continue
#                 return input_text

#     def get_supported_languages(self):
#         """Returns the list of supported languages"""
#         return self.supported_languages









# from deep_translator import GoogleTranslator

# class TextTranslator:
#     def trans(self, inputText: str, transLang: str) -> str:
#         '''Translates text in the given translation language code 
#         Look up codes by this URL "https://developers.google.com/admin-sdk/directory/v1/languages"'''

#         if not inputText:
#             raise ValueError("Input text must be a string and should be passed")
#         if not transLang:
#             raise ValueError("TransLang code must be a string and should be passed")

#         # Using GoogleTranslator from deep_translator to perform translation
#         translator = GoogleTranslator(source="auto", target=transLang)
#         return translator.translate(inputText)

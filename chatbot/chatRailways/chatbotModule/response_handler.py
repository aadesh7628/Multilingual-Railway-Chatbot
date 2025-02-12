from typing import Dict
from django.http import JsonResponse
from .textTranslator import TextTranslator
from .chatbot import Bot

class ResponseHandler:
    def __init__(self, bot: Bot, translator: TextTranslator):
        self.bot = bot
        self.translator = translator

    def handle_audio_response(self, success: bool, text: str, lang_code: str) -> JsonResponse:
        if success:
            # Debug transcription output
            print(f"Original Transcription: {text}")

            # Translate transcription to English
            if lang_code != 'en':
                text = self.translator.trans(text, 'en')
                print(f"Translated to English: {text}")

            # Get chatbot response
            response = self.bot.chat(text)
            print(f"Chatbot Response (English): {response}")

            # Translate response back to the original language
            if lang_code != 'en':
                response = self.translator.trans(response, lang_code)
                print(f"Translated to {lang_code}: {response}")

            return JsonResponse({
                'success': True,
                'text': text,
                'response': response,
                'langCode': lang_code
            })

        return JsonResponse({'success': False, 'error': text})
    
    def handle_chat_response(self, query: str, language: str) -> JsonResponse:
        """Handle chatbot text input and response translation."""
        try:
            if language != 'en':
                query = self.translator.trans(query, 'en')

            response = self.bot.chat(query)

            if language != 'en':
                response = self.translator.trans(response, language)

            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)})
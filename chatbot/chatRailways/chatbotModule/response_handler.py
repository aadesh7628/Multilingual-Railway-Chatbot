# from typing import Dict, Any, Optional
# from django.http import JsonResponse
# from .chatbot import Bot
# from .textTranslator import TextTranslator

# class ResponseHandler:
#     def __init__(self, bot: Bot, translator: TextTranslator):
#         self.bot = bot
#         self.translator = translator

#     def handle_audio_response(self, success: bool, text: str, lang_code: str) -> JsonResponse:
#         """Handle response for audio processing."""
#         if success:
#             # Translate transcribed text to English for processing
#             if lang_code != 'en':
#                 text = self.translator.trans(text, 'en')
            
#             # Get chatbot response
#             response = self.bot.chat(text)
            
#             # Translate response back to original language
#             if lang_code != 'en':
#                 response = self.translator.trans(response, lang_code)
            
#             return JsonResponse({
#                 'success': True,
#                 'text': text,
#                 'response': response,
#                 'langCode': lang_code
#             })
        
#         return JsonResponse({
#             'success': False,
#             'error': text
#         })

#     def handle_chat_response(self, query: str, language: str) -> JsonResponse:
#         """Handle chatbot response and translation."""
#         try:
#             # Translate query to English if needed
#             if language != 'en':
#                 query = self.translator.trans(query, 'en')
            
#             # Get response from chatbot
#             response = self.bot.chat(query)
            
#             # Translate response if needed
#             if language != 'en':
#                 response = self.translator.trans(response, language)
            
#             return JsonResponse({'response': response})
            
#         except Exception as e:
#             return JsonResponse({
#                 'error': str(e),
#                 'response': "Sorry, I couldn't process your request."
#             })




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






















# from typing import Dict, Any, Optional
# from django.http import JsonResponse
# from .chatbot import Bot
# from .textTranslator import TextTranslator

# class ResponseHandler:
#     def __init__(self, bot: Bot, translator: TextTranslator):
#         self.bot = bot
#         self.translator = translator

#     def handle_audio_response(self, success: bool, text: str, lang_code: str) -> JsonResponse:
#         """Handle response for audio processing."""
#         if success:
#             return JsonResponse({
#                 'success': True,
#                 'text': text,
#                 'langCode': lang_code
#             })
#         return JsonResponse({
#             'success': False,
#             'error': text
#         })

#     def handle_chat_response(self, query: str, language: str) -> JsonResponse:
#         """Handle chatbot response and translation."""
#         try:
#             # Get response from chatbot
#             response = self.bot.chat(query)
            
#             # Translate if not in English
#             if language != 'en':
#                 response = self.translator.trans(response, language)
            
#             return JsonResponse({'response': response})
            
#         except Exception as e:
#             return JsonResponse({
#                 'error': str(e),
#                 'response': "Sorry, I couldn't process your request."
#             })














# from typing import Dict, Any, Optional, Tuple
# from django.http import JsonResponse
# from .chatbot import Bot
# from .textTranslator import TextTranslator
# import json

# class ResponseHandler:
#     def __init__(self, bot: Bot, translator: TextTranslator):
#         self.bot = bot
#         self.translator = translator
#         self.error_messages = {
#             'en': {
#                 'processing_error': "Sorry, I couldn't process your request.",
#                 'audio_error': "There was an error processing your voice input.",
#                 'translation_error': "Sorry, I couldn't translate the response.",
#                 'invalid_query': "Please provide a valid query.",
#                 'service_unavailable': "The service is temporarily unavailable."
#             }
#         }

#     def get_error_message(self, key: str, lang: str = 'en') -> str:
#         """Get localized error message."""
#         lang_errors = self.error_messages.get(lang, self.error_messages['en'])
#         return lang_errors.get(key, lang_errors['processing_error'])

#     def format_response(self, response: str, query_type: Optional[str] = None) -> str:
#         """Format the response based on query type and content."""
#         if not response:
#             return self.get_error_message('processing_error')

#         # Add appropriate prefixes based on query type
#         if query_type == 'schedule':
#             response = f"Schedule Information: {response}"
#         elif query_type == 'platform':
#             response = f"Platform Details: {response}"
#         elif query_type == 'price':
#             response = f"Ticket Price: {response}"
        
#         return response

#     def handle_audio_response(self, success: bool, text: str, lang_code: str) -> JsonResponse:
#         """Handle response for audio processing."""
#         if success:
#             return JsonResponse({
#                 'success': True,
#                 'text': text,
#                 'langCode': lang_code,
#                 'confidence': 1.0  # Add confidence score if available
#             })
        
#         error_message = self.get_error_message('audio_error', lang_code)
#         return JsonResponse({
#             'success': False,
#             'error': error_message,
#             'details': text
#         })

#     def handle_chat_response(self, query: str, language: str) -> JsonResponse:
#         """Handle chatbot response and translation."""
#         try:
#             if not query.strip():
#                 return JsonResponse({
#                     'error': self.get_error_message('invalid_query', language)
#                 })

#             # Translate query to English if needed
#             eng_query = query
#             if language != 'en':
#                 eng_query = self.translator.trans(query, 'en')

#             # Get response from chatbot
#             response = self.bot.chat(eng_query)
            
#             # Determine query type for formatting
#             query_type = self._determine_query_type(eng_query.lower())
#             formatted_response = self.format_response(response, query_type)

#             # Translate response if needed
#             if language != 'en':
#                 formatted_response = self.translator.trans(formatted_response, language)

#             return JsonResponse({
#                 'response': formatted_response,
#                 'original_query': query,
#                 'detected_language': language
#             })

#         except Exception as e:
#             return JsonResponse({
#                 'error': self.get_error_message('processing_error', language),
#                 'details': str(e)
#             })

#     def _determine_query_type(self, query: str) -> Optional[str]:
#         """Determine the type of query for response formatting."""
#         if any(word in query for word in ['schedule', 'time', 'arrival', 'departure']):
#             return 'schedule'
#         elif any(word in query for word in ['platform', 'track', 'terminal']):
#             return 'platform'
#         elif any(word in query for word in ['price', 'fare', 'cost', 'ticket']):
#             return 'price'
#         return None

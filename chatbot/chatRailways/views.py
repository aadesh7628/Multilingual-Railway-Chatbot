from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbotModule.chatbot import Bot
from .chatbotModule.textTranslator import TextTranslator
from .chatbotModule.audio_handler import AudioHandler
from .chatbotModule.response_handler import ResponseHandler
from gtts import gTTS
import os
import json
from bs4 import BeautifulSoup
import re


bot = Bot(api_token="Enter your api token") #google gemini
translator = TextTranslator()
audio_handler = AudioHandler()
response_handler = ResponseHandler(bot, translator)

def render_webpage(request):
    """Render the chatbot interface."""
    return render(request, 'chatbotUI.html')

@csrf_exempt
def receive_audio(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

    audio_data = request.FILES.get('audio')
    if not audio_data:
        return JsonResponse({'success': False, 'error': 'No audio data received.'})

    # Get the selected language from the request
    lang = request.POST.get('lang', 'en-US')  # Default to English

    # Use AudioHandler to process the audio
    success, text, lang_code = audio_handler.process_audio(audio_data, lang)

    if success:
        return JsonResponse({
            'success': True,
            'text': text,
            'langCode': lang_code
        })

    return JsonResponse({'success': False, 'error': text})


def extract_plain_text(html_content: str) -> str:
    """Extract plain text from HTML and retain essential formatting."""
    # Use BeautifulSoup to strip HTML tags
    soup = BeautifulSoup(html_content, 'html.parser')
    plain_text = soup.get_text(separator=' ')

    # Improve regex to retain essential punctuation for formatting
    # Keeps text, numbers, commas, periods, colons, INR symbol, and arrows
    plain_text = re.sub(r'[^\w\s,.₹:→\-]', '', plain_text)  
    
    # Ensure multiple spaces are collapsed into one
    plain_text = re.sub(r'\s+', ' ', plain_text).strip()

    return plain_text

@csrf_exempt
def text_to_speech(request):
    """Handle text-to-speech conversion."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'})
    
    text = request.POST.get('text')
    lang = request.POST.get('lang', 'en')
    
    if not text:
        return JsonResponse({'error': 'No text provided'})
    
    # Process text to ensure plain text
    plain_text = extract_plain_text(text)
    
    try:
        # Create gTTS object and save to file
        tts = gTTS(text=plain_text, lang=lang, slow=False)
        audio_path = os.path.join('chatRailways', 'static', 'audio', 'response.mp3')
        tts.save(audio_path)
        
        # Return the audio file
        return FileResponse(open(audio_path, 'rb'), content_type='audio/mpeg')
    except Exception as e:
        return JsonResponse({'error': str(e)})

@csrf_exempt
def chatbot(request):
    """Handle chatbot interactions."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'})
    
    try:
        data = json.loads(request.body)
        query = data.get('userQuery', '')
        language = data.get('selectedLanguage', 'en')
        
        # First, translate the query to English if it's not in English
        if language != 'en':
            query = translator.trans(query, 'en')
        
        # Get response in English
        response = bot.chat(query)
        
        # Translate response back to the selected language if needed
        if language != 'en':
            response = translator.trans(response, language)
        
        return JsonResponse({'response': response})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'})
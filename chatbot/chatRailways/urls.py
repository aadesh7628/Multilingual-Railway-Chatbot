# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.render_webpage, name='chatbot'),
#     path('speech/', views.receive_audio, name='speech'),
#     path('text-to-speech/', views.text_to_speech, name='text_to_speech'),
#     path('chatbot/', views.chatbot_response, name='chatbot_response'),
# ]






from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_webpage, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('speech/', views.receive_audio, name='speech'),
    path('text-to-speech/', views.text_to_speech, name='text-to-speech'),
    # path('format_helpline_response/', views.format_helpline_response, name='format_helpline_response'),
]
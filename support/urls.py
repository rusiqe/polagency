from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.ChatBotView.as_view(), name='chatbot'),
    path('api/chat/', views.ChatAPIView.as_view(), name='chat_api'),
    path('faq/', views.faq_list, name='faq'),
    path('contact/', views.contact_form, name='contact'),
]


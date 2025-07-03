import json
import uuid
import re
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from .models import ChatSession, ChatMessage, FAQ, ContactRequest

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class ChatBotView(View):
    """Main chatbot interface"""
    
    def get(self, request):
        return render(request, 'support/chatbot.html')

@method_decorator(csrf_exempt, name='dispatch')
class ChatAPIView(View):
    """API endpoint for chat functionality"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'start_session':
                return self.start_session(request)
            elif action == 'send_message':
                return self.send_message(request, data)
            elif action == 'connect_to_admin':
                return self.connect_to_admin(request, data)
            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    def start_session(self, request):
        """Start a new chat session"""
        session_id = str(uuid.uuid4())
        user_ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        session = ChatSession.objects.create(
            session_id=session_id,
            user_ip=user_ip,
            user_agent=user_agent
        )
        
        # Send welcome message
        welcome_message = ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content="Hello! I'm here to help you with information about studying in Poland. You can ask me about universities, admission processes, visa requirements, or our services. How can I assist you today?"
        )
        
        return JsonResponse({
            'session_id': session_id,
            'message': {
                'type': 'bot',
                'content': welcome_message.content,
                'timestamp': welcome_message.timestamp.isoformat()
            }
        })
    
    def send_message(self, request, data):
        """Process user message and generate bot response"""
        session_id = data.get('session_id')
        user_message = data.get('message', '').strip()
        
        if not session_id or not user_message:
            return JsonResponse({'error': 'Missing session_id or message'}, status=400)
        
        try:
            session = ChatSession.objects.get(session_id=session_id, is_active=True)
        except ChatSession.DoesNotExist:
            return JsonResponse({'error': 'Invalid session'}, status=404)
        
        # Save user message
        ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=user_message
        )
        
        # Generate bot response
        bot_response = self.generate_bot_response(user_message)
        
        # Save bot response
        bot_message = ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content=bot_response
        )
        
        return JsonResponse({
            'message': {
                'type': 'bot',
                'content': bot_message.content,
                'timestamp': bot_message.timestamp.isoformat()
            }
        })
    
    def generate_bot_response(self, user_message):
        """Generate appropriate bot response based on user message"""
        user_message_lower = user_message.lower()
        
        # Check for FAQ matches
        faqs = FAQ.objects.filter(is_active=True)
        
        for faq in faqs:
            keywords = [kw.strip().lower() for kw in faq.keywords.split(',')]
            if any(keyword in user_message_lower for keyword in keywords):
                return faq.answer
        
        # Keyword-based responses
        if any(word in user_message_lower for word in ['university', 'universities', 'school', 'college']):
            return "I can help you find universities in Poland! We have information about both public and private universities. You can search by city, study area, or language of instruction. Would you like me to help you search for specific universities or programs?"
        
        elif any(word in user_message_lower for word in ['visa', 'permit', 'residence']):
            return "For visa and residence permit information, our consulting service includes complete visa process assistance. This covers document preparation, application submission, and guidance throughout the process. Would you like to know more about our consulting package?"
        
        elif any(word in user_message_lower for word in ['cost', 'price', 'fee', 'money', 'expensive']):
            return "Our comprehensive consulting service package costs $500 USD and includes: personal application assistance, discussions with admissions officers, interview preparation, visa process help, airport pickup, accommodation setup, and integration support. Would you like more details about what's included?"
        
        elif any(word in user_message_lower for word in ['accommodation', 'housing', 'dormitory', 'apartment']):
            return "We help with accommodation as part of our consulting service! This includes finding suitable housing options, dormitory applications, and setting up your accommodation before you arrive. We can assist with both university dormitories and private housing."
        
        elif any(word in user_message_lower for word in ['english', 'language', 'program']):
            return "Many Polish universities offer programs in English! You can filter our university search by language to find English-taught programs. Popular fields include Business, Engineering, Medicine, and Computer Science. Would you like help finding English programs in a specific field?"
        
        elif any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return "Hello! I'm here to help you with studying in Poland. I can provide information about universities, admission processes, visa requirements, and our consulting services. What would you like to know?"
        
        elif any(word in user_message_lower for word in ['help', 'support', 'assistance']):
            return "I'm here to help! I can assist you with:\n• Finding universities and programs\n• Admission requirements\n• Visa and residence permits\n• Our consulting services\n• Accommodation options\n• General information about studying in Poland\n\nWhat specific information do you need?"
        
        elif any(word in user_message_lower for word in ['admin', 'human', 'person', 'agent', 'representative']):
            return "I can connect you with one of our human agents for personalized assistance. Would you like me to create a contact request so our team can reach out to you directly?"
        
        else:
            return "I understand you're looking for information about studying in Poland. While I try to help with common questions, for more specific inquiries, I can connect you with our human support team. Would you like me to create a contact request for you, or would you like to try asking about universities, visa requirements, or our services?"
    
    def connect_to_admin(self, request, data):
        """Create a contact request to connect user with admin"""
        session_id = data.get('session_id')
        contact_info = data.get('contact_info', {})
        
        try:
            session = ChatSession.objects.get(session_id=session_id, is_active=True)
        except ChatSession.DoesNotExist:
            return JsonResponse({'error': 'Invalid session'}, status=404)
        
        # Create contact request
        contact_request = ContactRequest.objects.create(
            name=contact_info.get('name', 'Chat User'),
            email=contact_info.get('email', ''),
            phone=contact_info.get('phone', ''),
            subject=contact_info.get('subject', 'Chat Support Request'),
            message=contact_info.get('message', 'User requested human support from chat'),
            chat_session=session,
            priority='medium'
        )
        
        # Mark session as connected to admin
        session.connected_to_admin = True
        session.save()
        
        # Send confirmation message
        bot_message = ChatMessage.objects.create(
            session=session,
            message_type='system',
            content="Thank you! I've created a support request and our team will contact you soon. Your request ID is: " + str(contact_request.id)
        )
        
        return JsonResponse({
            'message': {
                'type': 'system',
                'content': bot_message.content,
                'timestamp': bot_message.timestamp.isoformat()
            },
            'request_id': contact_request.id
        })

def faq_list(request):
    """Display FAQ page"""
    return render(request, 'support/faq.html')

def contact_form(request):
    """Display and handle contact form"""
    if request.method == 'POST':
        contact_request = ContactRequest.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone', ''),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
            priority=request.POST.get('priority', 'medium')
        )
        
        return render(request, 'support/contact_success.html', {'request': contact_request})
    
    return render(request, 'support/contact_form.html')


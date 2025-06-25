import uuid
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ServicePackage, Order, OrderProgress, Testimonial

def service_packages(request):
    """Display available service packages"""
    packages = ServicePackage.objects.filter(is_active=True).order_by('display_order', 'price_usd')
    featured_package = packages.filter(is_featured=True).first()
    testimonials = Testimonial.objects.filter(is_approved=True, is_featured=True)[:6]
    
    context = {
        'packages': packages,
        'featured_package': featured_package,
        'testimonials': testimonials,
    }
    
    return render(request, 'services/packages.html', context)

def package_detail(request, package_id):
    """Display detailed information about a specific package"""
    package = get_object_or_404(ServicePackage, id=package_id, is_active=True)
    
    # Parse features from JSON
    try:
        features = json.loads(package.features) if package.features else []
    except json.JSONDecodeError:
        features = []
    
    context = {
        'package': package,
        'features': features,
    }
    
    return render(request, 'services/package_detail.html', context)

def order_form(request, package_id):
    """Display order form for a specific package"""
    package = get_object_or_404(ServicePackage, id=package_id, is_active=True)
    
    if request.method == 'POST':
        return process_order(request, package)
    
    context = {
        'package': package,
    }
    
    return render(request, 'services/order_form.html', context)

def process_order(request, package):
    """Process the order form submission"""
    try:
        # Generate unique order number
        order_number = f"PSA{uuid.uuid4().hex[:8].upper()}"
        
        # Create order
        order = Order.objects.create(
            order_number=order_number,
            package=package,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            country=request.POST.get('country'),
            current_education_level=request.POST.get('current_education_level'),
            desired_study_level=request.POST.get('desired_study_level'),
            preferred_field=request.POST.get('preferred_field'),
            preferred_cities=request.POST.get('preferred_cities', ''),
            english_proficiency=request.POST.get('english_proficiency'),
            total_amount=package.price_usd,
            special_requirements=request.POST.get('special_requirements', ''),
        )
        
        # Create initial progress stages
        initial_stages = ['order_received', 'consultant_assigned']
        for stage in initial_stages:
            OrderProgress.objects.create(
                order=order,
                stage=stage,
                completed=(stage == 'order_received')
            )
        
        # Mark first stage as completed
        first_progress = order.progress.filter(stage='order_received').first()
        if first_progress:
            first_progress.completed = True
            first_progress.save()
        
        # Send confirmation email (placeholder - would need email configuration)
        try:
            send_confirmation_email(order)
        except Exception as e:
            # Log error but don't fail the order
            pass
        
        return redirect('services:order_success', order_number=order.order_number)
        
    except Exception as e:
        messages.error(request, 'There was an error processing your order. Please try again.')
        return render(request, 'services/order_form.html', {'package': package})

def order_success(request, order_number):
    """Display order success page"""
    order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order,
    }
    
    return render(request, 'services/order_success.html', context)

def order_tracking(request, order_number):
    """Display order tracking page"""
    order = get_object_or_404(Order, order_number=order_number)
    progress_stages = order.progress.all().order_by('created_at')
    
    context = {
        'order': order,
        'progress_stages': progress_stages,
    }
    
    return render(request, 'services/order_tracking.html', context)

def testimonials(request):
    """Display testimonials page"""
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
    
    context = {
        'testimonials': testimonials,
    }
    
    return render(request, 'services/testimonials.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def payment_webhook(request):
    """Handle payment gateway webhooks (placeholder)"""
    # This would handle webhooks from payment processors like Stripe, PayPal, etc.
    # For now, it's a placeholder that would need to be implemented based on the chosen payment gateway
    
    try:
        # Parse webhook data
        payload = json.loads(request.body)
        
        # Verify webhook signature (implementation depends on payment provider)
        # if not verify_webhook_signature(request):
        #     return JsonResponse({'error': 'Invalid signature'}, status=400)
        
        # Process payment confirmation
        order_number = payload.get('order_number')
        payment_status = payload.get('status')
        payment_id = payload.get('payment_id')
        
        if order_number and payment_status == 'completed':
            try:
                order = Order.objects.get(order_number=order_number)
                order.payment_status = 'completed'
                order.order_status = 'paid'
                order.payment_id = payment_id
                order.save()
                
                # Send payment confirmation email
                send_payment_confirmation_email(order)
                
                return JsonResponse({'status': 'success'})
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order not found'}, status=404)
        
        return JsonResponse({'status': 'ignored'})
        
    except Exception as e:
        return JsonResponse({'error': 'Webhook processing failed'}, status=500)

def send_confirmation_email(order):
    """Send order confirmation email"""
    subject = f"Order Confirmation - {order.order_number}"
    message = f"""
    Dear {order.get_full_name()},
    
    Thank you for your order! We have received your request for our {order.package.name} service.
    
    Order Details:
    - Order Number: {order.order_number}
    - Package: {order.package.name}
    - Total Amount: ${order.total_amount} USD
    
    Our team will contact you within 24 hours to begin the consultation process.
    
    You can track your order progress at: [Order Tracking URL]
    
    Best regards,
    Poland Study Agency Team
    """
    
    # This would need proper email configuration in settings.py
    # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.email])

def send_payment_confirmation_email(order):
    """Send payment confirmation email"""
    subject = f"Payment Confirmed - {order.order_number}"
    message = f"""
    Dear {order.get_full_name()},
    
    Your payment has been successfully processed!
    
    Order Details:
    - Order Number: {order.order_number}
    - Package: {order.package.name}
    - Amount Paid: ${order.total_amount} USD
    
    Our consultant will contact you within 24 hours to schedule your initial consultation.
    
    Best regards,
    Poland Study Agency Team
    """
    
    # This would need proper email configuration in settings.py
    # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.email])


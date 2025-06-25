from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_packages, name='packages'),
    path('package/<int:package_id>/', views.package_detail, name='package_detail'),
    path('order/<int:package_id>/', views.order_form, name='order_form'),
    path('success/<str:order_number>/', views.order_success, name='order_success'),
    path('tracking/<str:order_number>/', views.order_tracking, name='order_tracking'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('webhook/payment/', views.payment_webhook, name='payment_webhook'),
]


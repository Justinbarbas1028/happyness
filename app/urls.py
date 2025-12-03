from django.urls import path
from . import views

urlpatterns = [
    # Public landing page
    path('', views.landing, name='landing'),

    # Authenticated homepage
    path('home/', views.home, name='home'),

    # Simple placeholder pages for navbar
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('faqs/', views.faqs, name='faqs'),
    path('partners/', views.partners, name='partners'),

    # HTMX demo
    path('htmx/greeting/', views.htmx_greeting, name='htmx_greeting'),
    
    # HTMX validation endpoints
    path('validate/username/', views.validate_username, name='validate_username'),
    path('validate/email/', views.validate_email, name='validate_email'),
    path('validate/field/', views.validate_field, name='validate_field'),
]

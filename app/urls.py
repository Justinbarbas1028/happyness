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

    # HTMX demo
    path('htmx/greeting/', views.htmx_greeting, name='htmx_greeting'),
]

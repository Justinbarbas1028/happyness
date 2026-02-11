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
    path('donate/', views.donate, name='donate'),

    # Article URLs (Public)
    path('articles/', views.article_list, name='article_list'),
    path('articles/search/instant/', views.article_search_instant, name='article_search_instant'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('articles/<slug:slug>/like/', views.article_like, name='article_like'),
    path('articles/<slug:slug>/bookmark/', views.article_bookmark, name='article_bookmark'),
    path('articles/<slug:slug>/comment/', views.article_comment, name='article_comment'),

    # HTMX demo
    path('htmx/greeting/', views.htmx_greeting, name='htmx_greeting'),
    
    # HTMX validation endpoints
    path('validate/username/', views.validate_username, name='validate_username'),
    path('validate/email/', views.validate_email, name='validate_email'),
    path('validate/field/', views.validate_field, name='validate_field'),
    
    # Admin Dashboard
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('admin-panel/analytics/', views.admin_analytics, name='admin_analytics'),
    path('admin-panel/settings/', views.admin_settings, name='admin_settings'),
    
    # Admin Article Management
    path('admin-panel/articles/', views.admin_articles, name='admin_articles'),
    path('admin-panel/articles/create/', views.admin_article_create, name='admin_article_create'),
    path('admin-panel/articles/<int:article_id>/edit/', views.admin_article_edit, name='admin_article_edit'),
    path('admin-panel/articles/<int:article_id>/delete/', views.admin_article_delete, name='admin_article_delete'),
    path('admin-panel/articles/<int:article_id>/toggle-status/', views.admin_article_toggle_status, name='admin_article_toggle_status'),
    
    # Admin Category Management
    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
    path('admin-panel/categories/<int:category_id>/delete/', views.admin_category_delete, name='admin_category_delete'),
    
    # Admin Tag Management
    path('admin-panel/tags/', views.admin_tags, name='admin_tags'),
    path('admin-panel/tags/<int:tag_id>/delete/', views.admin_tag_delete, name='admin_tag_delete'),
    path('admin-panel/tags/<int:tag_id>/toggle-predefined/', views.admin_tag_toggle_predefined, name='admin_tag_toggle_predefined'),
    path('admin-panel/tags/create-inline/', views.admin_tag_create_inline, name='admin_tag_create_inline'),
]

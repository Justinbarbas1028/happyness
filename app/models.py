from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug'], name='app_categor_slug_0ace88_idx'),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def article_count(self):
        return self.articles.filter(status='published').count()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    is_predefined = models.BooleanField(default=False, help_text='Predefined tags are curated by admins')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug'], name='app_tag_slug_1b0ea8_idx'),
            models.Index(fields=['is_predefined'], name='app_tag_is_pred_e54117_idx'),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    ARTICLE_TYPE_CHOICES = (
        ('article', 'Article'),
        ('update', 'Project Update'),
        ('event', 'Event'),
        ('news', 'News'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    featured_image = models.ImageField(upload_to='articles/images/', null=True, blank=True, help_text='Featured image for the article')
    excerpt = models.TextField(max_length=300, help_text='Short description for article preview (max 300 characters)')
    content = HTMLField(help_text='Full article content')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', db_index=True)
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPE_CHOICES, default='article', db_index=True, help_text='Type of article content')
    is_featured = models.BooleanField(default=False, db_index=True, help_text='Feature this article on the homepage')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    scheduled_at = models.DateTimeField(null=True, blank=True, help_text='Schedule article for future publication')
    view_count = models.PositiveIntegerField(default=0, db_index=True, help_text='Total number of views')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', help_text='Tags for better discoverability')

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at'], name='app_article_status_21cc67_idx'),
            models.Index(fields=['status', '-view_count'], name='app_article_status_c0cf7f_idx'),
            models.Index(fields=['author', 'status'], name='app_article_author__d8ee75_idx'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    @property
    def reading_time(self):
        # Rough estimate: 200 words per minute
        word_count = len(self.content.split())
        return max(1, word_count // 200)

    @property
    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_comments')
    content = models.TextField(max_length=1000)
    is_approved = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['article', 'is_approved', '-created_at'], name='app_comment_article_d0a177_idx'),
        ]

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'

class ArticleLike(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article', 'user'], name='unique_article_like'),
        ]

    def __str__(self):
        return f'{self.user.username} likes {self.article.title}'

class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='article_views')
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['article', 'session_key', 'viewed_at'], name='app_article_article_98347a_idx'),
        ]

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_user_bookmark'),
        ]
        indexes = [
            models.Index(fields=['user', '-created_at'], name='app_bookmar_user_id_a2e33c_idx'),
        ]

    def __str__(self):
        return f'{self.user.username} bookmarked {self.article.title}'

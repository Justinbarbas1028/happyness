from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Article, Category, Tag, Comment, ArticleLike, ArticleView, Bookmark
from .forms import ArticleForm, CategoryForm, TagForm, CommentForm



def is_admin(user):
	"""Check if user is staff or superuser"""
	return user.is_staff or user.is_superuser


def landing(request):
	return render(request, 'landing.html', {
		'title': 'HappyNess Project',
	})


@login_required
def home(request):
	return render(request, 'home.html', {
		'title': 'Dashboard',
	})


def about(request):
	return render(request, 'about.html', {'title': 'About'})


def products(request):
	return render(request, 'products.html', {'title': 'Products'})


def faqs(request):
	return render(request, 'faqs.html', {'title': 'FAQs'})


def partners(request):
	return render(request, 'partners.html', {'title': 'Our Partners'})


def donate(request):
	return render(request, 'donate.html', {'title': 'Donate'})


def htmx_greeting(request):
	# Return a small partial snippet. HTMX will swap it into the target div.
	return render(request, 'partials/greeting.html', {
		'user': request.user,
	})


# HTMX Validation Views
@require_POST
def validate_username(request):
	"""Real-time username validation for signup form"""
	username = request.POST.get('username', '').strip()
	
	if not username:
		return HttpResponse('')
	
	if len(username) < 3:
		return HttpResponse('Username must be at least 3 characters long')
	
	if User.objects.filter(username=username).exists():
		return HttpResponse('This username is already taken')
	
	# Username is valid
	return HttpResponse('<span class="text-green-400">✓ Username available</span>')


@require_POST
def validate_email(request):
	"""Real-time email validation for signup form"""
	email = request.POST.get('email', '').strip()
	
	if not email:
		return HttpResponse('')
	
	# Basic email format check
	if '@' not in email or '.' not in email.split('@')[-1]:
		return HttpResponse('Please enter a valid email address')
	
	if User.objects.filter(email=email).exists():
		return HttpResponse('An account with this email already exists')
	
	# Email is valid
	return HttpResponse('<span class="text-green-400">✓ Email available</span>')


@require_POST
def validate_field(request):
	"""General field validation for login form"""
	login = request.POST.get('login', '').strip()
	
	if not login:
		return HttpResponse('')
	
	# Just check if field is not empty for login
	return HttpResponse('')


# Admin Dashboard Views
@login_required
@user_passes_test(is_admin, login_url='/home/')
def admin_dashboard(request):
	"""Admin dashboard overview"""
	total_users = User.objects.count()
	active_users = User.objects.filter(is_active=True).count()
	staff_users = User.objects.filter(is_staff=True).count()
	recent_users = User.objects.order_by('-date_joined')[:5]
	
	return render(request, 'admin/dashboard.html', {
		'title': 'Admin Dashboard',
		'total_users': total_users,
		'active_users': active_users,
		'staff_users': staff_users,
		'recent_users': recent_users,
	})


@login_required
@user_passes_test(is_admin, login_url='/home/')
def admin_users(request):
	"""Admin user management"""
	users = User.objects.all().order_by('-date_joined')
	
	# Optimized stats calculation
	total_users = users.count()
	active_users = users.filter(is_active=True).count()
	staff_users = users.filter(is_staff=True).count()
	superuser_count = users.filter(is_superuser=True).count()

	return render(request, 'admin/users.html', {
		'title': 'User Management',
		'users': users,
		'total_users': total_users,
		'active_users': active_users,
		'staff_users': staff_users,
		'superuser_count': superuser_count,
	})


@login_required
@user_passes_test(is_admin, login_url='/home/')
@require_POST
def toggle_user_status(request, user_id):
	"""Toggle user active status via HTMX"""
	user = get_object_or_404(User, id=user_id)
	
	# Prevent modifying self
	if user == request.user:
		return HttpResponse(status=403)
		
	user.is_active = not user.is_active
	user.save()
	
	# Get updated active count for OOB swap
	active_users = User.objects.filter(is_active=True).count()
	
	# Render the status badge
	if user.is_active:
		status_html = '''
		<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
			<span class="w-1.5 h-1.5 bg-green-500 rounded-full mr-1.5"></span>
			Active
		</span>
		'''
	else:
		status_html = '''
		<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
			<span class="w-1.5 h-1.5 bg-red-500 rounded-full mr-1.5"></span>
			Inactive
		</span>
		'''
		
	# Add OOB swap for the counter
	oob_html = f'<span id="active-users-count" hx-swap-oob="true">{active_users}</span>'
	
	return HttpResponse(status_html + oob_html)


@login_required
@user_passes_test(is_admin, login_url='/home/')
def admin_analytics(request):
	"""Admin analytics page"""
	return render(request, 'admin/analytics.html', {
		'title': 'Analytics',
	})


@login_required
@user_passes_test(is_admin, login_url='/home/')
def admin_settings(request):
	"""Admin settings page"""
	return render(request, 'admin/settings.html', {
		'title': 'Settings',
	})


# Article Views
def article_list(request):
	"""Public article list with filtering and search"""
	query = request.GET.get('q', '')
	category_slug = request.GET.get('category', '')
	tag_slug = request.GET.get('tag', '')
	article_type = request.GET.get('type', '')
	
	articles = Article.objects.filter(status='published')
	
	if query:
		articles = articles.filter(
			Q(title__icontains=query) | 
			Q(excerpt__icontains=query) | 
			Q(content__icontains=query)
		)
	
	if category_slug:
		articles = articles.filter(category__slug=category_slug)
		
	if tag_slug:
		articles = articles.filter(tags__slug=tag_slug)
	
	if article_type:
		articles = articles.filter(article_type=article_type)
		
	# Pagination
	paginator = Paginator(articles, 9)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	featured_articles = Article.objects.filter(status='published', is_featured=True)[:3]
	categories = Category.objects.annotate(article_count=Count('articles', filter=Q(articles__status='published')))
	tags = Tag.objects.filter(is_predefined=True)
	
	# Get bookmarked article IDs for the current user
	bookmarked_ids = []
	if request.user.is_authenticated:
		bookmarked_ids = list(Bookmark.objects.filter(user=request.user).values_list('article_id', flat=True))
	
	return render(request, 'articles/article_list.html', {
		'articles': page_obj,
		'featured_articles': featured_articles,
		'categories': categories,
		'tags': tags,
		'search_query': query,
		'current_category': category_slug,
		'current_tag': tag_slug,
		'current_type': article_type,
		'bookmarked_ids': bookmarked_ids,
		'title': 'Articles',
	})


def article_detail(request, slug):
	"""Article detail page with view counting and related articles"""
	article = get_object_or_404(Article, slug=slug, status='published')
	
	# Increment view count (simple version)
	article.view_count += 1
	article.save(update_fields=['view_count'])
	
	# Ensure session exists before accessing session_key
	if not request.session.session_key:
		request.session.create()
	
	# Track detailed view
	ArticleView.objects.create(
		article=article,
		user=request.user if request.user.is_authenticated else None,
		session_key=request.session.session_key or '',
		ip_address=request.META.get('REMOTE_ADDR', ''),
		user_agent=request.META.get('HTTP_USER_AGENT', '')[:500] if request.META.get('HTTP_USER_AGENT') else ''
	)
	
	related_articles = Article.objects.filter(
		status='published', 
		category=article.category
	).exclude(id=article.id)[:3]
	
	comments = article.comments.filter(is_approved=True)
	
	user_has_liked = False
	user_has_bookmarked = False
	if request.user.is_authenticated:
		user_has_liked = ArticleLike.objects.filter(article=article, user=request.user).exists()
		user_has_bookmarked = Bookmark.objects.filter(article=article, user=request.user).exists()
		
	return render(request, 'articles/article_detail.html', {
		'article': article,
		'related_articles': related_articles,
		'comments': comments,
		'user_has_liked': user_has_liked,
		'user_has_bookmarked': user_has_bookmarked,
		'comment_form': CommentForm(),
	})


def article_search_instant(request):
	"""HTMX instant search results"""
	query = request.GET.get('q', '')
	if len(query) < 2:
		return HttpResponse('')
		
	articles = Article.objects.filter(
		status='published'
	).filter(
		Q(title__icontains=query) | Q(excerpt__icontains=query)
	)[:5]
	
	return render(request, 'articles/partials/search_results.html', {
		'articles': articles,
		'query': query,
	})


@login_required
@require_POST
def article_like(request, slug):
	"""Toggle article like via HTMX"""
	article = get_object_or_404(Article, slug=slug)
	like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)
	
	if not created:
		like.delete()
		user_has_liked = False
	else:
		user_has_liked = True
		
	like_count = article.likes.count()
	
	return render(request, 'articles/partials/like_button.html', {
		'article': article,
		'user_has_liked': user_has_liked,
		'like_count': like_count,
	})


@login_required
@require_POST
def article_bookmark(request, slug):
	"""Toggle article bookmark via HTMX"""
	article = get_object_or_404(Article, slug=slug)
	bookmark, created = Bookmark.objects.get_or_create(article=article, user=request.user)
	
	if not created:
		bookmark.delete()
		user_has_bookmarked = False
	else:
		user_has_bookmarked = True
		
	return render(request, 'articles/partials/bookmark_button.html', {
		'article': article,
		'user_has_bookmarked': user_has_bookmarked,
	})


@login_required
@require_POST
def article_comment(request, slug):
	"""Add comment to article via HTMX"""
	article = get_object_or_404(Article, slug=slug)
	form = CommentForm(request.POST)
	
	if form.is_valid():
		comment = form.save(commit=False)
		comment.article = article
		comment.user = request.user
		comment.save()
		
		# Return updated comment list partial
		comments = article.comments.filter(is_approved=True)
		return render(request, 'articles/partials/comment_list.html', {
			'comments': comments,
		})
		
	return HttpResponse('Invalid comment', status=400)


# Admin Article Management Views
@login_required
@user_passes_test(is_admin, login_url='/home/')
def admin_articles(request):
	"""Admin list of all articles"""
	articles = Article.objects.all().order_by('-created_at')
	total_articles = articles.count()
	published_count = articles.filter(status='published').count()
	draft_count = articles.filter(status='draft').count()
	
	return render(request, 'admin/articles.html', {
		'articles': articles,
		'total_articles': total_articles,
		'published_count': published_count,
		'draft_count': draft_count,
		'title': 'Article Management',
	})


@login_required
@user_passes_test(is_admin, login_url='/home/')
def admin_article_create(request):
	"""Create new article"""
	if request.method == 'POST':
		form = ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			article = form.save(commit=False)
			article.author = request.user
			article.save()
			form.save_m2m() # Save tags
			messages.success(request, 'Article created successfully!')
			return redirect('admin_articles')
	else:
		form = ArticleForm()
		
	return render(request, 'admin/article_form.html', {
		'form': form,
		'title': 'Create Article',
		'is_edit': False,
	})


@login_required
@user_passes_test(is_admin, login_url='/home/')
def admin_article_edit(request, article_id):
	"""Edit existing article"""
	article = get_object_or_404(Article, id=article_id)
	if request.method == 'POST':
		form = ArticleForm(request.POST, request.FILES, instance=article)
		if form.is_valid():
			form.save()
			messages.success(request, 'Article updated successfully!')
			return redirect('admin_articles')
	else:
		form = ArticleForm(instance=article)
		
	return render(request, 'admin/article_form.html', {
		'form': form,
		'article': article,
		'title': f'Edit: {article.title}',
		'is_edit': True,
	})


@login_required
@user_passes_test(is_admin, login_url='/home/')
@require_POST
def admin_article_delete(request, article_id):
	"""Delete an article"""
	article = get_object_or_404(Article, id=article_id)
	article.delete()
	messages.success(request, 'Article deleted successfully!')
	return redirect('admin_articles')


@login_required
@user_passes_test(is_admin, login_url='/home/')
@require_POST
def admin_article_toggle_status(request, article_id):
	"""Toggle article status via HTMX"""
	article = get_object_or_404(Article, id=article_id)
	if article.status == 'published':
		article.status = 'draft'
		article.published_at = None
	else:
		article.status = 'published'
		article.published_at = timezone.now()
	article.save()
	
	if article.status == 'published':
		return HttpResponse('''
		<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
			<span class="w-1.5 h-1.5 bg-green-500 rounded-full mr-1.5"></span>Published
		</span>
		''')
	else:
		return HttpResponse('''
		<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
			<span class="w-1.5 h-1.5 bg-yellow-500 rounded-full mr-1.5"></span>Draft
		</span>
		''')


@login_required
@user_passes_test(is_admin, login_url='/home/')
def admin_categories(request):
	"""Admin category management"""
	categories = Category.objects.all().annotate(article_count=Count('articles'))
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Category added successfully!')
			return redirect('admin_categories')
	else:
		form = CategoryForm()
		
	return render(request, 'admin/categories.html', {
		'categories': categories,
		'form': form,
		'title': 'Category Management',
	})


@login_required
@user_passes_test(is_admin, login_url='/home/')
@require_POST
def admin_category_delete(request, category_id):
	"""Delete a category"""
	category = get_object_or_404(Category, id=category_id)
	name = category.name
	category.delete()
	messages.success(request, f'Category "{name}" deleted successfully!')
	return redirect('admin_categories')


# ============================================
# ADMIN TAG VIEWS
# ============================================

@login_required
@user_passes_test(is_admin, login_url='/home/')
def admin_tags(request):
	"""Admin tag management"""
	tags = Tag.objects.annotate(
		article_count=Count('articles')
	).all()
	
	if request.method == 'POST':
		form = TagForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Tag created successfully!')
			return redirect('admin_tags')
	else:
		form = TagForm()
	
	predefined_count = tags.filter(is_predefined=True).count()
	custom_count = tags.filter(is_predefined=False).count()
	
	return render(request, 'admin/tags.html', {
		'title': 'Tags',
		'tags': tags,
		'form': form,
		'predefined_count': predefined_count,
		'custom_count': custom_count,
	})


@login_required
@user_passes_test(is_admin, login_url='/home/')
@require_POST
def admin_tag_delete(request, tag_id):
	"""Delete a tag"""
	tag = get_object_or_404(Tag, id=tag_id)
	name = tag.name
	tag.delete()
	messages.success(request, f'Tag "{name}" deleted successfully!')
	return redirect('admin_tags')


@login_required
@user_passes_test(is_admin, login_url='/home/')
@require_POST
def admin_tag_toggle_predefined(request, tag_id):
	"""Toggle tag predefined status (HTMX)"""
	tag = get_object_or_404(Tag, id=tag_id)
	tag.is_predefined = not tag.is_predefined
	tag.save()
	
	if tag.is_predefined:
		html = '''<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
			Predefined</span>'''
	else:
		html = '''<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
			Custom</span>'''
	return HttpResponse(html)


@login_required
@user_passes_test(is_admin, login_url='/home/')
@require_POST
def admin_tag_create_inline(request):
	"""Create tag via AJAX from article form"""
	name = request.POST.get('name', '').strip()
	if not name:
		return HttpResponse('<span class="text-red-500">Tag name is required</span>')
	
	# Check if tag already exists
	from django.utils.text import slugify
	slug = slugify(name)
	if Tag.objects.filter(slug=slug).exists():
		return HttpResponse('<span class="text-yellow-500">Tag already exists</span>')
	
	tag = Tag.objects.create(name=name, slug=slug, is_predefined=False)
	return HttpResponse(f'<option value="{tag.id}" selected>{tag.name}</option> created')


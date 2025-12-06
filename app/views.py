from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.http import require_POST


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

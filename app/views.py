from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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


def htmx_greeting(request):
	# Return a small partial snippet. HTMX will swap it into the target div.
	return render(request, 'partials/greeting.html', {
		'user': request.user,
	})

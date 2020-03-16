from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.template.loader import get_template
from .forms import ContactForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail, BadHeaderError

def Home_Page(request):
	mytitle = "Welcome to CSP"
	# doc = "<h1>{title}</h1>".format(title=mytitle)
	# rendered_doc = ""<h1>{title}</h1>".format(title=mytitle)"
	return render(request, "home_page.html", {"title": mytitle})

def About_Page(request):
	context = {
		"title": "About us"
	}
	template_name = "about_page.html"
	template_obj = get_template(template_name)
	return HttpResponse(template_obj.render(context))

def Contact_Page(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form = ContactForm()
	mytitle = "Contact us"
	context = {
		"title": mytitle,
		"form": form
	}

	return render(request, "content_page.html", context)

def signup_view(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your blog account.'
			message = render_to_string('acc_active_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token':account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
						mail_subject, message, to=[to_email]
			)
			email.send()
			return render(request, 'confirm_registration.html', { 'form':form })
			# Now, You Signed up :)
			# login(request, user)
	else:
		form = UserRegisterForm()
	return render(request, 'signup.html', { 'form':form })

def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user) # Now, You Logged In :)
			if "next" in request.POST:
				return redirect(request.POST.get("next"))
			else:
				return redirect('/')
	else:
		form = AuthenticationForm()
	if request.user.is_authenticated :
		return redirect('/')
	return render(request, 'login.html', { 'form': form })

def logout_view(request):
	if request.method == "POST":
		logout(request)
		# logged out :)
		return redirect('/')

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		messages.success(request, f'Your account has been created!')
		return redirect('/signup')
	else:
		return HttpResponse('Activation link is invalid!')
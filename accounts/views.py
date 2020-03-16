from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from Blog.forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.

@login_required(login_url="/login")
def profile(request):
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.username = user_form.cleaned_data.get('username')
			user_form.email = user_form.cleaned_data.get('email')
			profile_form.bio = profile_form.cleaned_data.get('bio')
			profile_form.image = profile_form.cleaned_data.get('image')
			user_form.save()
			profile_form.save()
			''' for field in profile_form.changed_data:
				setattr(user.profile, field, profile_form.cleaned_data.get(field))
			user.profile.save() '''
			# user_form.refresh_from_db()  # load the profile instance created by the signal
			# profile_form.refresh_from_db()  # load the profile instance created by the signal
			messages.success(request, 'Your account has been updated!')
			return redirect('profile')
	else:
		user_form = UserUpdateForm(instance=request.user)
		profile_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'user_form': user_form,
		'profile_form': profile_form
	}

	return render(request, 'profile.html', context)

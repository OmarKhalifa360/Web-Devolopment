from django import forms
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
	full_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	content = forms.CharField(widget=forms.Textarea, required=True)

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.fields['full_name'].label = "Your name:"
		self.fields['email'].label = "Your email:"
		self.fields['content'].label = "What do you want to say?"


class UserRegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(required=True, help_text='Required, enter a valid email address.')

	def clean(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
			raise ValidationError('Email exists!')
		return self.cleaned_data

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

		
class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username']
		

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = [ 'bio', 'image']
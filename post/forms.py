from django import forms
from .models import BlogPost, Comment
from django.core.exceptions import ValidationError

class BlogPostForm(forms.Form):
	title = forms.CharField()
	slug = forms.SlugField()
	content = forms.CharField(widget=forms.Textarea)

class BlogPostModelForm(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = ['title', 'slug', 'content', 'image']

	def clean_title(self, *args, **kwargs):
		instance = self.instance
		title = self.cleaned_data.get('title')
		qs = BlogPost.objects.filter(title__iexact=title)
		if instance is not None:
			qs = qs.exclude(pk=instance.pk)
		if qs.exists():
			raise ValidationError("This title is already exists")
		return title

class CommentsForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content',]
		labels = {'content': ''}
		widgets = {'content': forms.Textarea(attrs={'rows':5,
                                                    'cols':140,
                                                    'style':'resize:none;'})}

	# def __init__(self, *args, **kwargs):
	#	super(CommentsForm, self).__init__(*args, **kwargs)

class CommentsReplies(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['reply',]
		labels = {'reply': ''}
		widgets = {'reply': forms.Textarea(attrs={'rows':5,
                                                    'cols':80,
                                                    'style':'resize:none;'})}
			
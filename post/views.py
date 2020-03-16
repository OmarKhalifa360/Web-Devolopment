from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import UpdateView, DeleteView, RedirectView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, render_to_response, get_object_or_404, redirect, reverse
from .models import BlogPost, Comment
from .forms import BlogPostModelForm, CommentsForm, CommentsReplies
from django.template import RequestContext

# Create your views here.

def detail_page(request, slug):
#	try:
#		obj = BlogPost.objects.get(slug=slug)
#	except:
#		raise Http404 
#	obj = BlogPost.objects.filter(post, slug=slug) # Get -----> 1 object | Filter ------> [] objects
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = "post/detail.html"
	comments = obj.comments.filter(approved_comment=True)
	# replies = obj.comments.replies.filter(approved_comment=True)
	new_comment = None
	'''initial_data = {
			"author": obj.author,
			"content": obj.content,
			"created_date": obj.created_date,
	}'''
	if request.method == "POST":
		comment_form = CommentsForm(data=request.POST)
		reply = CommentsReplies(data=request.POST)
		#userpreference = int(userpreference)
		if comment_form.is_valid():
			content = comment_form.cleaned_data['content']
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.author = request.user
			new_comment.post = obj
			# Save the comment to the database
			new_comment.save()
			# return redirect('/blog/<str:slug>', slug=BlogPost.slug)
		'''if userpreference == 1:
			obj.likes += 1
		elif userpreference == 2:
			obj.dislikes += 1'''
	else:
		comment_form = CommentsForm()
	template_name = "post/detail.html"
	context = {
		"object": obj,
		'new_comment': new_comment,
		"comment_form": comment_form,
		"comments": comments
	}
	return render(request, template_name, context)

class BlogPostLikeRedirect(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		obj = get_object_or_404(BlogPost, slug=slug)
		url_ = obj.get_absolute_url()
		user = self.request.user
		if user in obj.likes.all():
			obj.likes.remove(user)
		else:
			obj.likes.add(user)
			obj.dislikes.remove(user)
		return url_

class BlogPostDislikeRedirect(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		obj = get_object_or_404(BlogPost, slug=slug)
		url_ = obj.get_absolute_url()
		user = self.request.user
		if user in obj.dislikes.all():
			obj.dislikes.remove(user)
		else:
			obj.dislikes.add(user)
			obj.likes.remove(user)
		return url_

class CommentLikeRedirect(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		obj = get_object_or_404(BlogPost, slug=slug)
		comments = obj.comments.filter(approved_comment=True)
		url_ = obj.get_absolute_url()
		user = self.request.user
		if user in comments.likes.all():
			comments.likes.remove(user)
		else:
			comments.likes.add(user)
			comments.dislikes.remove(user)
		return url_

class CommentDislikeRedirect(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		obj = get_object_or_404(BlogPost, slug=slug)
		comments = obj.comments.filter(approved_comment=True)
		url_ = obj.get_absolute_url()
		user = self.request.user
		if user in comments.dislikes.all():
			comments.dislikes.remove(user)
		else:
			comments.dislikes.add(user)
			comments.likes.remove(user)
		return url_

#CRUD ---> (Create - Retrieve - Update - Delete) --> (list = a version of retrieve)

# GET ---> Retrieve - List
# POST ---> Create - Update - Delete

# @staff_member_required
@login_required(login_url="/login")
def create_view(request):
	form = BlogPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.user = request.user
		obj.save()
		form = BlogPostModelForm()
		messages.success(request, 'Your post has been created successfully!')
	template_name = "post/create.html"
	context = {
		"form": form
	}
	return render(request, template_name, context)

def detail_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	comments = obj.comments.filter(approved_comment=True)
	new_comment = None
	'''initial_data = {
			"author": obj.author,
			"content": obj.content,
			"created_date": obj.created_date,
	}'''
	if request.method == "POST":
		comment_form = CommentsForm(data=request.POST)
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.author = request.user
			new_comment.post = obj
			# Save the comment to the database
			new_comment.save()
			# return redirect('post_detail', slug=BlogPost.slug)
	else:
		comment_form = CommentsForm()
	template_name = "post/detail.html"
	context = {
		"object": obj,
		'new_comment': new_comment,
		"comment_form": comment_form,
		"comments": comments
	}
	return render(request, template_name, context)


def list_view(request):
	# BlogPost.objects.all()
	qs = BlogPost.objects.all().published() # we can use filter()
	if request.user.is_authenticated:
		my_qs = BlogPost.objects.filter(user=request.user)
		qs = (qs | my_qs).distinct()
	template_name = "post/list.html"
	context = {
		"object_list": qs
	}
	return render(request, template_name, context)


'''def test_func(self):
	BlogPost = self.get_object()
	if self.request.user == BlogPost.author:
		return True
	else:
		return False'''

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = BlogPost
	template_name = 'post/update.html'
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		BlogPost = self.get_object()
		if self.request.user == BlogPost.user:
			return True
		return False


# @staff_member_required
# @login_required
# @user_passes_test(test_func)
'''def update_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	form = BlogPostModelForm(request.POST or None, request.FILES or None, instance=obj)
	if form.is_valid():
		form.save()
	template_name = "post/update.html"
	context = {
		"object": obj,
		"form": form
	}
	return render(request, template_name, context)'''

'''def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

def test_func(self):
	BlogPost = self.get_object()
	if self.request.user == BlogPost.user:
		return True
	return False '''
# @staff_member_required
#@login_required
#@user_passes_test(test_func)
'''def delete_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = "post/delete.html"
	if request.method == "POST":
		obj.delete()
		return redirect("/blog")
	context = {
		"object": obj ,
		"form": ""
	}
	return render(request, template_name, context) '''

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = BlogPost
	success_url = '/blog'

	def test_func(self):
		BlogPost = self.get_object()
		if self.request.user == BlogPost.user:
			return True
		return False

'''def add_comment_to_post(request, slug):
	post = get_object_or_404(BlogPost, slug=slug)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail', slug=BlogPost.slug)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})'''
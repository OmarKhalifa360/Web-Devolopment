from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone

# Create your models here.

User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
	def published(self):
		now = timezone.now()
		return self.filter(publish_date__lte=now)

	def search(self, query):
		lookup = (Q(title__icontains=query) | 
				  Q(content__icontains=query) |
				  Q(slug__icontains=query) |
				  Q(user__first_name__icontains=query) |
				  Q(user__last_name__icontains=query) |
				  Q(user__username__icontains=query) )
		
		return self.filter(lookup)


class BlogPostManager(models.Manager):
	def get_queryset(self):
		return BlogPostQuerySet(self.model, using=self._db)

	def published(self):
		return self.get_queryset().published()

	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().published().search(query)


class BlogPost(models.Model): # blogpost_set ---> queryset
	user = models.ForeignKey(User, default=1, null=True , on_delete="None")
	title = models.CharField(max_length=50)
	slug = models.SlugField(null=True , unique=True)
	content = models.TextField(null=True, blank=True)
	likes= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like')
	dislikes= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dislike')
	image = models.ImageField(upload_to="images/", blank=True, null=True)
	publish_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	objects = BlogPostManager()

	class Meta:
		ordering = ["-publish_date", "-updated", "-timestamp"]

	def get_absolute_url(self):
		return f"/blog/{self.slug}"

	def get_edit_url(self):
		return f"/blog/{self.slug}/edit"

	def get_delete_url(self):
		return f"/blog/{self.slug}/delete"

class Comment(models.Model):
	post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	reply = models.CharField(max_length=150, blank=True)
	likes= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comment_like')
	dislikes= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comment_dislike')
	created_date = models.DateField(auto_now_add=True)
	approved_comment = models.BooleanField(default=True)

	class Meta:
		ordering = ['-created_date']

	'''def approve(self):
		self.approved_comment = True
		self.save()'''

	def __str__(self):
		return 'Comment: {} by {}'.format(self.content, self.author)

'''class CommentReply(models.Model):
	post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
	content = models.TextField()
'''
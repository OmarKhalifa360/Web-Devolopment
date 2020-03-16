from django.urls import path
from django.conf.urls import url
from . import views
from .views import (
	create_view,
	detail_page,
	list_view,
	PostUpdateView,
	PostDeleteView,
	BlogPostLikeRedirect,
	CommentLikeRedirect,
	BlogPostDislikeRedirect,
	CommentDislikeRedirect,
	#add_comment_to_post
	)

urlpatterns = [
    path('<str:slug>', detail_page, name='post_detail'),
    path('<str:slug>/like/', BlogPostLikeRedirect.as_view(), name='like'),
    path('<str:slug>/dislike/', BlogPostDislikeRedirect.as_view(), name='dislike'),
    path('<str:slug>/comment/like/', CommentLikeRedirect.as_view(), name='comment_like'),
    path('<str:slug>/comment/dislike/', CommentDislikeRedirect.as_view(), name='comment_dislike'),
    path('<str:slug>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('<str:slug>/delete/', PostDeleteView.as_view(template_name='post/delete.html'), name='post-delete'),
    #path('<str:slug>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('', list_view),
    # path('blog/', detail_page),
]

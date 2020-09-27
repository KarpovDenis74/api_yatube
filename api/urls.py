from django.urls import path
from rest_framework.authtoken import views
from .views import PostViewSet, CommentViewSet


urlpatterns = [
        path('api/v1/api-token-auth/', views.obtain_auth_token,
            name='create_token'),
        path('api/v1/posts/<int:post_id>/comments/<int:comment_id>/',
            CommentViewSet.as_view(
                actions={
                    'delete': 'delete_comment',
                    'get': 'view_comment',
                    'patch': 'patch_comment'}),
            name='current_comment'),
        path('api/v1/posts/<int:post_id>/comments/', CommentViewSet.as_view(
            actions={'get': 'list_comments', 'post': 'create'}),
            name='comments'),
        path('api/v1/posts/<int:post_id>/', PostViewSet.as_view(
            actions={
            'delete': 'delete_post',
            'get': 'view_post',
            'patch': 'patch_post'}),
            name='current_post'),
        path('api/v1/posts/', PostViewSet.as_view(
            actions={'get': 'list_posts', 'post': 'create'}),
            name='posts'),
    ]

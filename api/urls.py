from django.urls import path, include
from rest_framework.authtoken import views
from .views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet, basename='api_posts')
router.register(r'posts',
    PostViewSet, basename='api_comments')

urlpatterns = [
    path(r'v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]

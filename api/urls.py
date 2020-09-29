from django.urls import path, include
from rest_framework.authtoken import views
from .views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'v1/posts/(?P<post_id>\d+)/comments',
    CommentViewSet)
router.register(r'v1/posts',
    PostViewSet)

urlpatterns = [
    path(r'v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]

from posts.models import Post, Comment
from .serializer import PostSerializer, CommentSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .permissions import OnlyCreatorPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [OnlyCreatorPermission]

    def qet_queryset(self):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request):
        if request.user.is_authenticated:
            return Response(PostSerializer(
                self.queryset, many=True).data,
                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self,  request, *args, **kwargs):
        instance = self.qet_queryset()
        if request.user == instance.author:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.qet_queryset()
        if request.user == instance.author:
            return self.update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [OnlyCreatorPermission]

    def qet_queryset(self, *args, **kwargs):
        return get_object_or_404(Comment, pk=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        posts = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        self.queryset = posts.comments.all()
        if request.user.is_authenticated:
            comments = self.get_queryset()
            return Response(CommentSerializer(
                comments, many=True).data,
                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.qet_queryset()
        if request.user == instance.author:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.qet_queryset()
        if request.user == instance.author:
            return self.update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

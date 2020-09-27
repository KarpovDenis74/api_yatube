from posts.models import Post, Comment
from .serializer import PostSerializer, CommentSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404


class OnlyCreatorPermission(BasePermission):
    massage = "Нет прав на данное действие"

    def has_object_permission(self, request, view, obj):
        if request.metod in ('DELETE', 'PUT', 'PATCH'):
            return request.user == obj.author
        return True


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [OnlyCreatorPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['GET'], detail=True)
    def list_posts(self, request):
        if request.user.is_authenticated:
            self.queryset = Post.objects.all()
            return Response(PostSerializer(
                self.queryset, many=True).data,
                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['DELETE'], detail=False)
    def delete_post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if request.user == post.author:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['GET'], detail=False)
    def view_post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        return Response(PostSerializer(
            post, many=False).data,
            status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=False)
    def patch_post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if request.user == post.author:
            serializer = self.get_serializer(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=request.user)
            return Response(PostSerializer(
                post, many=False).data,
                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [OnlyCreatorPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['GET'], detail=True)
    def list_comments(self, request, post_id):
        if request.user.is_authenticated:
            post = Post.objects.filter(pk=post_id).first()
            comments = Comment.objects.filter(post=post)
            return Response(CommentSerializer(
                comments, many=True).data,
                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['GET'], detail=True)
    def view_comment(self, request, post_id, comment_id):
        if request.user.is_authenticated:
            comment = get_object_or_404(Comment, pk=comment_id)
            return Response(CommentSerializer(
                comment, many=False).data,
                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['DELETE'], detail=False)
    def delete_comment(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.author:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['PATCH'], detail=False)
    def patch_comment(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        self.queryset = comment
        if request.user == comment.author:
            serializer = self.get_serializer(
                comment, data=request.data,
                partial='partial')
            serializer.is_valid(raise_exception=True)
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

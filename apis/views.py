""" Rest framework API views """
from rest_framework import viewsets

from blogs.models import Post, PostEval, PostHit, Comment
from .serializers import PostSerializer, PostEvalSerializer, PostHitSerializer, CommentSerializer


class PostAPIView(viewsets.ModelViewSet):
    """ Post API view """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostEvalAPIView(viewsets.ModelViewSet):
    """ Post evaluation API view """
    queryset = PostEval.objects.all()
    serializer_class = PostEvalSerializer
    filter_fields = ('post', 'user', 'good', 'bad')


class PostHitAPIView(viewsets.ModelViewSet):
    """ Post hit API view """
    queryset = PostHit.objects.all()
    serializer_class = PostHitSerializer
    filter_fields = ('post', 'user', 'hit')


class CommentAPIView(viewsets.ModelViewSet):
    """ Comment API view """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_fileds = ('post', 'user', 'text', 'updated_date', 'was_updated')

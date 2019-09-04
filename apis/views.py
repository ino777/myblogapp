""" Rest framework API views """
from rest_framework import viewsets

from blogs.models import Post, PostEval
from .serializers import PostSerializer, PostEvalSerializer


class PostAPIView(viewsets.ModelViewSet):
    """ Post API view """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostEvalAPIView(viewsets.ModelViewSet):
    """ Post evaluation API view """
    queryset = PostEval.objects.all()
    serializer_class = PostEvalSerializer
    filter_fields = ('post', 'user', 'good', 'bad')

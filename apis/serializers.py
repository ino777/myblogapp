""" Serializers """
from django.contrib.auth import get_user_model
from rest_framework import serializers


from blogs.models import Post, PostEval, PostHit


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """ Post serializer """
    class Meta:
        model = Post
        fields = '__all__'


class PostEvalSerializer(serializers.ModelSerializer):
    """ Post evaluation serializer """
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PostEval
        fields = '__all__'


class PostHitSerializer(serializers.ModelSerializer):
    """ Post Hit serializer """
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PostHit
        fields = '__all__'
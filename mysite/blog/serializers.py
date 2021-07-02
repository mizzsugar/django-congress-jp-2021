from rest_framework import serializers

from blog.models import User, Post, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username'
        )


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'text',
            'published_date'
        )


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'comment',
            'birthday',
        )

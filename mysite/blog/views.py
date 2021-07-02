from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from rest_framework.response import Response

from blog.models import Post, Profile, User
from blog.serializers import PostSerializer, ProfileSerializer


@api_view(['GET'])
def published_blogs(request):
    posts = Post.objects.published()
    return Response(PostSerializer(post, many=True).data)

@api_view(['GET'])
@login_required
def my_profile(request):
    try:
        profile = Profile.get_user_profile(request.user)
        return Response(ProfileSerializer(profile).data)
    except User.profile.RelatedObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

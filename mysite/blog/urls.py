from django.urls import path

from blog.views import published_blogs, my_profile


urlpatterns = [
    path('my_profile', my_profile),
    path('published_posts', published_blogs)
]
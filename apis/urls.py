""" Rest framework API URL settings """
from django.urls import path, include
from rest_framework import routers


from .views import PostAPIView, PostEvalAPIView, PostHitAPIView


router = routers.DefaultRouter()

router.register(r'posts', PostAPIView)
router.register(r'post_evals', PostEvalAPIView)
router.register(r'post_hits', PostHitAPIView)


app_name = 'apis'
urlpatterns = [
    path(r'', include(router.urls))
]


"""
Url pattern name is the lower case of queryset object in the viewset

The example of url patterns
    View: queryset=User.objects.all()
        URL pattern: ^users/$ , Name: 'user-list'
        URL pattern: ^users/{pk}/$ , Name: 'user-detail'

When referencing ^users/{pk}, write {% url 'apis:user-detail' user.pk %} in your templates

"""

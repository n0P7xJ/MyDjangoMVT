from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicViewSet, CommunityViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'communities', CommunityViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

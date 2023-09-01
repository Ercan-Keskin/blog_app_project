from django.urls import path, include


from .views import BlogViewSet,CommentDetailView, CategoryViewSet, LikesView, PostViewsSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('detay', BlogViewSet)
router.register('categories', CategoryViewSet)
router.register('likes', LikesView)
router.register('comments', CommentDetailView)
router.register('post_view', PostViewsSet)



urlpatterns = [
   path("", include(router.urls)),
   
] 



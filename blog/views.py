from django.shortcuts import render


from .models import Category, Blog, Comment, Likes, PostViews
from .serializers import CategorySerializer, BlogSerializer, CommentSerializer, LikesSerializer, PostViewsSerializer, UserBlogSerializer
from .permissions import IsStaffOrReadOnly, IsOwnerOrReadOnly, IsOwnerOrReadOnlyComment

from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]

class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = UserBlogSerializer 
    permission_classes = [IsOwnerOrReadOnly]
    

    #! Blog sayfasına gelindiğinde kullanıcı create edebilir:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        view_query = PostViews.objects.filter(user = request.user, blog = instance)
       
        if not view_query.exists():  # ---daha önce detayı inceleyen kullanıcı yok ise create işlemi yapılacak---
            PostViews.objects.create(user = request.user, blog = instance, post_views = True)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    #Eğer kişi blogun sahibi ise ve admin ise bloğu d yani yayınlamasa bile görüntüleyebilir düzeltebilir.
    def get_queryset(self):
        if self.request.user.is_staff:
            return Blog.objects.all()  # Tüm yazıları yöneticilere göster
        else:
            return Blog.objects.filter(Q(status='p') | Q(user=self.request.user))  # Kullanıcının yazılarını ve yayınlanmış yazıları göster
        
    #! kullanıcının yetkisine göre userblogserializer veya blogserializer kullanılsın
    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.request.user.is_staff:
            return BlogSerializer
        return serializer

class CommentDetailView(ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes=[IsOwnerOrReadOnlyComment]


class LikesView(ModelViewSet):
    queryset = Likes.objects.all() 
    serializer_class = LikesSerializer
    
    
class PostViewsSet(ModelViewSet):
    queryset = PostViews.objects.all()
    serializer_class = PostViewsSerializer
    

    
    

